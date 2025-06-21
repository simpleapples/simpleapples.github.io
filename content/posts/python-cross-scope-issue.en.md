---
date: "2021-11-06T08:25:00+00:00"
title: "Pitfalls of Passing Scope Across Services in Python"
categories:
  - Python
---

# Background

In an old system, there is a piece of code like this:

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

The first segment of user code defines a function, and the second segment executes the function (don't ask why this is done, because the user is always right). After executing the first code block, `func_a` and `global_a` are added to the scope. Since the second code block uses the same scope, calling `func_a` in the second block correctly outputs 123.

However, using `exec` to execute user code is neither elegant nor safe, so the `exec` function was encapsulated in a Python sandbox environment (simply put, another Python service that receives the code and scope, and executes `exec(code, scope)` in the sandbox environment). Essentially, each call to `exec` was replaced with an RPC request to the sandbox service.

The code then becomes:

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

# Issue with Passing Scope Across Services

Since multiple RPC calls need to use the same scope, the sandbox service returns a new scope to ensure the scope isn't lost on subsequent calls. However, when executing the code, you'll find that the second `call_sandbox` call returns an error:

global name 'global_a' is not defined

Initially, it was suspected that the scope wasn't updated after the first call. However, if the scope wasn't updated, it should have reported that `func_a` couldn't be found. This error indicates that during the second call, `func_a` exists in the scope, but `func_a` can't find the variable `global_a`. By printing the scope before the second `call_sandbox`, you'll find that both `global_a` and `func_a` exist:

```python
print(scope.keys())
# ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__',
# '__builtins__', 'global_a', 'func_a']
call_sandbox("func_a()", scope)
```

This proves that during the second `call_sandbox`, the scope was correctly passed in, and the absence of an error about `func_a` confirms this. By retrieving and printing `globals()` and `locals()` inside `func_a`:

```python
def func_a():
    inner_scope = dict(globals(), **locals())
    print(inner_scope.keys())
    # ['__builtins__']
```

You can see that the outer scope of `func_a` is normal, but inside `func_a`, the scope only contains **builtins**, effectively clearing the scope. It's suspected that the function's caller points to the sandbox environment's scope, and when the scope is returned, the caller isn't updated, so the function can't find the outer scope. Checking Python function magic methods:

![](/images/20211106_01.png)

Reveals a **globals** variable pointing to the current scope, essentially the function's caller. Verify whether the **globals** of `func_a` in the scope returned by the sandbox service matches the current scope:

```python
scope["func_a"].__globals__ == globals()  # False
```

Indeed, they are different. Next, try setting `scope["func_a"].__globals__` to `globals()`, which should resolve the issue.

# Optimizing Scope Update Logic

The root cause of the issue is now clear:

- The first `exec` statement and the second `exec` statement are executed in Python services A and B, respectively. The scope of `func_a` defined in the first `exec` statement is service A (`func_a.__globals__ == A`).
- When the scope is returned to service B, `global_a` and `func_a` are copied to service B's scope, but `func_a.__globals__` still points to service A's scope, resulting in `func_a` being callable but unable to find `global_a` within `func_a`.
- Setting `func_a.__globals__` to B allows the code to execute correctly in service B.

As documented, the function **globals** is a read-only variable, so it can't be directly assigned. Instead, a function copying method is needed:

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

Update the scope returned by the sandbox call. If a value in the scope is a function, update its **globals** to the scope using the copying method:

```python
scope = dict(globals(), **locals())
scope = call_sandbox(
"""
global_a = 123
def func_a():
    print(global_a)
"""
, scope)
for k, v in scope.items():
    if isinstance(v, types.FunctionType):
        scope[k] = copy_func(v, scope, __name__)
call_sandbox("func_a()", scope)
```

Re-run the code, and both `call_sandbox` calls execute correctly, resolving the issue.

# References

[https://docs.python.org/3/reference/datamodel.html](https://docs.python.org/3/reference/datamodel.html)

[https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module](https://stackoverflow.com/questions/49076566/override-globals-in-function-imported-from-another-module)

[https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec/2906198](https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec/2906198)