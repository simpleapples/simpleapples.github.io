---
layout: post
title: 你真的会正确使用断言吗？
date: 2018-05-07 16:12
comments: true
categories: Python
---

![](/upload/20180507_01.jpg)

# 什么是断言

断言是作为一种调试工具被发明出来的，用来检查那些“代码写对了就肯定成立”的条件。例如我们要断言一个变量a必须要大于2，就可以这样写：

```python
assert a > 2
```

当条件不满足时，就会抛出AssertionError异常，等同于如下代码：

```python
if not assert_condition:
    raise AssertionError
```

由于断言是一个debug工具，Python的实现也符合这个设计哲学，在Python中assert语句的执行是依赖于`__debug__`变量的，当`__debug__`为true时，assert语句才会被执行。

```python
if __debug__ and not assert_condition:
    raise AssertionError
```

默认情况下，当我们执行一个Python文件时，`__debug__`是会被设置为True的，只有加参数-O或-OO时，`__debug__`才会被设置为False。

新建一个assert.py文件，写下如下代码：

```python
print(__debug__)
assert 2 > 5
```

当使用python assert.py运行时，`__debug__`会输出True，assert 2 > 5语句会抛出AssertionError异常。

当使用python -O assert.py运行时，`__debug__`会输出False，assert 2 > 5语句由于没有执行不会报任何异常。

# 断言 or 异常

我们思考这几个问题：断言应该用在哪些情境下？异常和断言的区别是什么？

用一句话来概括断言的使用场景和与异常的区别：

>检查先验条件使用断言，检查后验条件使用异常

我们定义一个read_file函数：

```python
def read_file(file_path):
    pass
```

read_file函数要求在开始执行的时候满足一定条件：file_path必须是str类型，这个条件就是先验条件，如果不满足，就不能调用这个函数，如果真的出现了不满足条件的情况，证明代码中出现了bug，这时候我们就可以使用assert语句来对file_path的类型进行推断，提醒程序员修改代码，这样的推断在生产环境中是不需要的，也可以使用if + raise语句来实现assert，但是要繁琐很多。

```python
def read_file(file_path):
    assert is_instance(file_path, str)
```

read_file函数在被调用执行后，依然需要满足一定条件，比如file_path所指定的文件需要是存在的，并且当前用户有权限读取该文件，这些条件称为后验条件，对于后验条件的检查，我们需要使用异常来处理。

```python
def read_file(file_path):
    assert is_instance(file_path, str)
    if not check_exist(file_path):
        raise NotFoundError()
    if not has_privilege(file_path):
        raise PermissionError()
```

文件不存在和没有权限，这两种情况并不属于代码bug，是代码逻辑的一部分，上层代码捕获异常后可能会执行其他逻辑，因此我们不能接受这部分代码在生产环境中被忽略。并且，相比于assert语句只能抛出AssertionError，使用异常可以抛出更细致的错误，方便上层代码针对不同错误执行不同的逻辑。

# 关注Python私房菜

![](/upload/wechat-qrcode.jpg)
