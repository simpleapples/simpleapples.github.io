# 背景

在一个古老的系统中，有这样一段代码：

```python
scope = dict(globals(), **locals())
exec(
"""
global_a = 123
def func_a():
    print(global_a)
"""
, scope)
exec("func_a()", scope)
```

第一段用户代码定义了函数，第二段用户代码执行函数（不要问为什么这么做，因为用户永远是正确的）。第一个代码段执行后，func_a和global_a都会被加入作用域scope，由于第二个代码段也使用同一个scope，所以第二个代码段调用func_a是可以正确输出123的。

但是使用exec执行用户代码毕竟不优雅，也很危险，于是把exec函数封装在了一个Python沙箱环境中（简单理解就是另一个Python服务，将code和scope传给这个服务后，服务会在沙箱环境调用exec(code,scope)执行代码），相当于每一次对exec调用都替换成了对沙箱服务的RPC请求。

于是代码变成了这个样子：

```python
scope = dict(globals(), **locals())
scope = call_sandbox(
"""
global_a = 123
def func_a():
    print(global_a)
"""
, scope)
call_sandbox("func_a()", scope)
```

# 作用域跨服务传递问题

由于多次RPC调用需要使用同一个作用域，所以沙箱服务返回了新的scope，以保证下次调用时作用域不会丢失。但是执行代码会发现第二次call_sandbox调用时候，会返回错误：

global name 'global_a' is not defined

首先怀疑第一次调用后scope没有更新，但是如果scope没有更新，应该会报找不到func_a才对，这个报错说明，第二次调用时候，作用域里的func_a是存在的，但是func_a找不到变量global_a。通过输出第二次call_sandbox前的scope，会发现global_a和func_a都是存在的：

```python
print(scope.keys())
# ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__', 
# '__builtins__', 'global_a', 'func_a']
call_sandbox("func_a()", scope)
```

证明在第二次call_sandbox时，scope被正确的传入了，没有报找不到func_a也印证了这个结论。在func_a里获取并输出一下globals()和locals()：

```python
def func_a():
    inner_scope = dict(globals(), **locals()
    print(inner_scope.keys())
    # ['__builtins__']
```

可以看到在func_a外作用域是正常的，但是func_a内的作用域就只有__builtins__了，相当于作用域被清空了。猜测是函数的caller指向的是沙箱环境内的作用域，当scope回传回来后，caller没有更新，所以在函数内找不到函数外的作用域，查看一下Python函数的魔术方法：

![](/upload/20211106_01.png)   

发现有一个__globals__变量，指向的就是所在作用域，相当于函数的caller，通过如下代码验证调用沙箱服务后的scope里的func_a的__globals__是否和当前作用域的一样：

```python
scope["func_a"].__globals__ == globals()  # False
```

确实不一样，接下来试试把scope["func_a"].__globals__置为globals()，应该就可以跑通了。

# 优化作用域更新逻辑

到这里问题的根源已经搞清了：

- 第一个exec语句和第二个exec语句分别在Python服务A和B中执行，第一个exec语句中定义的func_a所在的作用域是服务A（func_a.__globals__ == A）
- 在scope回传到服务B后，global_a和func_a被拷贝到了服务B所在作用域，但是func_a.__globals__还是指向服务A的作用域，所以出现可以调用到func_a但在func_a里找不到global_a
- 将func_a.__globals__置为B，就可以使代码在服务B正确执行

如文档所述，函数__globals__是一个只读变量，所以不能直接赋值，需要通过拷贝函数的方式实现，定义一个拷贝函数的方法：

```python
import copy
import types
import functools
def copy_func(f, globals=None, module=None):
    if globals is None:
        globals = f.__globals__
    g = types.FunctionType(f.__code__, globals, name=f.__name__,
                           argdefs=f.__defaults__, closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    if module is not None:
        g.__module__ = module
    return g
```

更新调用沙箱后回传的scope，如果scope中的value是一个function，就通过复制的方式更新它的__globals__为scope：

```python
scope = dict(globals(), **locals())
scope = call_sandbox(
"""
global_a = 123
def func_a():
    print(global_a)
"""
, scope)
for k, v in scope:
    if isinstance(v, types.FunctionType):
        scope[k] = copy_func(v, scope, __name__)
call_sandbox("func_a()", scope)
```

重新运行，两个call_sandbox都可以正常执行，问题解决。

# 参考文档

[https://docs.python.org/3/reference/datamodel.html](https://docs.python.org/3/reference/datamodel.html)

[https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module](https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module)

[https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec/2906198](https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec/2906198)