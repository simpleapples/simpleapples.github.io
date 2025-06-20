---
date: "2018-05-07T16:12:00+00:00"
title: "你真的会正确使用断言吗？"
categories:
  - Python
---

![](/images/20180507_01.jpg)

# 什么是断言

断言是作为一种调试工具被发明出来的，用来检查那些“代码写对了就肯定成立”的条件。例如我们要断言一个变量 a 必须要大于 2，就可以这样写：

```python
assert a > 2
```

当条件不满足时，就会抛出 AssertionError 异常，等同于如下代码：

```python
if not assert_condition:
    raise AssertionError
```

由于断言是一个 debug 工具，Python 的实现也符合这个设计哲学，在 Python 中 assert 语句的执行是依赖于`__debug__`变量的，当`__debug__`为 true 时，assert 语句才会被执行。

```python
if __debug__ and not assert_condition:
    raise AssertionError
```

默认情况下，当我们执行一个 Python 文件时，`__debug__`是会被设置为 True 的，只有加参数-O 或-OO 时，`__debug__`才会被设置为 False。

新建一个 assert.py 文件，写下如下代码：

```python
print(__debug__)
assert 2 > 5
```

当使用 python assert.py 运行时，`__debug__`会输出 True，assert 2 > 5 语句会抛出 AssertionError 异常。

当使用 python -O assert.py 运行时，`__debug__`会输出 False，assert 2 > 5 语句由于没有执行不会报任何异常。

# 断言 or 异常

我们思考这几个问题：断言应该用在哪些情境下？异常和断言的区别是什么？

用一句话来概括断言的使用场景和与异常的区别：

> 检查先验条件使用断言，检查后验条件使用异常

我们定义一个 read_file 函数：

```python
def read_file(file_path):
    pass
```

read_file 函数要求在开始执行的时候满足一定条件：file_path 必须是 str 类型，这个条件就是先验条件，如果不满足，就不能调用这个函数，如果真的出现了不满足条件的情况，证明代码中出现了 bug，这时候我们就可以使用 assert 语句来对 file_path 的类型进行推断，提醒程序员修改代码，这样的推断在生产环境中是不需要的，也可以使用 if + raise 语句来实现 assert，但是要繁琐很多。

```python
def read_file(file_path):
    assert is_instance(file_path, str)
```

read_file 函数在被调用执行后，依然需要满足一定条件，比如 file_path 所指定的文件需要是存在的，并且当前用户有权限读取该文件，这些条件称为后验条件，对于后验条件的检查，我们需要使用异常来处理。

```python
def read_file(file_path):
    assert is_instance(file_path, str)
    if not check_exist(file_path):
        raise NotFoundError()
    if not has_privilege(file_path):
        raise PermissionError()
```

文件不存在和没有权限，这两种情况并不属于代码 bug，是代码逻辑的一部分，上层代码捕获异常后可能会执行其他逻辑，因此我们不能接受这部分代码在生产环境中被忽略。并且，相比于 assert 语句只能抛出 AssertionError，使用异常可以抛出更细致的错误，方便上层代码针对不同错误执行不同的逻辑。
