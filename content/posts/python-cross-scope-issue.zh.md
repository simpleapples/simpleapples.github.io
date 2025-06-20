---
date: "2021-11-06T08:25:00+00:00"
title: "Python跨服务传递作用域的坑"
categories:
  - Python
---

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

第一段用户代码定义了函数，第二段用户代码执行函数（不要问为什么这么做，因为用户永远是正确的）。第一个代码段执行后，func_a 和 global_a 都会被加入作用域 scope，由于第二个代码段也使用同一个 scope，所以第二个代码段调用 func_a 是可以正确输出 123 的。

但是使用 exec 执行用户代码毕竟不优雅，也很危险，于是把 exec 函数封装在了一个 Python 沙箱环境中（简单理解就是另一个 Python 服务，将 code 和 scope 传给这个服务后，服务会在沙箱环境调用 exec(code,scope)执行代码），相当于每一次对 exec 调用都替换成了对沙箱服务的 RPC 请求。

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

由于多次 RPC 调用需要使用同一个作用域，所以沙箱服务返回了新的 scope，以保证下次调用时作用域不会丢失。但是执行代码会发现第二次 call_sandbox 调用时候，会返回错误：

global name 'global_a' is not defined

首先怀疑第一次调用后 scope 没有更新，但是如果 scope 没有更新，应该会报找不到 func_a 才对，这个报错说明，第二次调用时候，作用域里的 func_a 是存在的，但是 func_a 找不到变量 global_a。通过输出第二次 call_sandbox 前的 scope，会发现 global_a 和 func_a 都是存在的：

```python
print(scope.keys())
# ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__',
# '__builtins__', 'global_a', 'func_a']
call_sandbox("func_a()", scope)
```

证明在第二次 call_sandbox 时，scope 被正确的传入了，没有报找不到 func_a 也印证了这个结论。在 func_a 里获取并输出一下 globals()和 locals()：

```python
def func_a():
    inner_scope = dict(globals(), **locals()
    print(inner_scope.keys())
    # ['__builtins__']
```

可以看到在 func_a 外作用域是正常的，但是 func_a 内的作用域就只有**builtins**了，相当于作用域被清空了。猜测是函数的 caller 指向的是沙箱环境内的作用域，当 scope 回传回来后，caller 没有更新，所以在函数内找不到函数外的作用域，查看一下 Python 函数的魔术方法：

![](/images/20211106_01.png)

发现有一个**globals**变量，指向的就是所在作用域，相当于函数的 caller，通过如下代码验证调用沙箱服务后的 scope 里的 func_a 的**globals**是否和当前作用域的一样：

```python
scope["func_a"].__globals__ == globals()  # False
```

确实不一样，接下来试试把 scope["func_a"].**globals**置为 globals()，应该就可以跑通了。

# 优化作用域更新逻辑

到这里问题的根源已经搞清了：

- 第一个 exec 语句和第二个 exec 语句分别在 Python 服务 A 和 B 中执行，第一个 exec 语句中定义的 func_a 所在的作用域是服务 A（func_a.**globals** == A）
- 在 scope 回传到服务 B 后，global_a 和 func_a 被拷贝到了服务 B 所在作用域，但是 func_a.**globals**还是指向服务 A 的作用域，所以出现可以调用到 func_a 但在 func_a 里找不到 global_a
- 将 func_a.**globals**置为 B，就可以使代码在服务 B 正确执行

如文档所述，函数**globals**是一个只读变量，所以不能直接赋值，需要通过拷贝函数的方式实现，定义一个拷贝函数的方法：

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

更新调用沙箱后回传的 scope，如果 scope 中的 value 是一个 function，就通过复制的方式更新它的**globals**为 scope：

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

重新运行，两个 call_sandbox 都可以正常执行，问题解决。

# 参考文档

[https://docs.python.org/3/reference/datamodel.html](https://docs.python.org/3/reference/datamodel.html)

[https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module](https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module)

[https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec/2906198](https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec/2906198)
