---
layout: post
title: "与面试官谈笑风生 | Python面向对象之访问控制"
date: 2018-03-30 17:54
comments: true
categories: Python
---

Python从设计之初就是一门面向对象的语言，面向对象思想的第一个要素就是封装。所谓封装，通俗的讲就是类中的属性和方法，分为公有和私有，公有可以被外界访问，私有不能被外界访问，这就是封装中最关键的概念——访问控制。

![面向对象编程](/upload/20180330_01.jpg)

访问控制有三种级别：私有、受保护、公有

私有（Private）：只有类自身可以访问
受保护（Protected）：只有类自身和子类可以访问
公有（Public）：任何类都可以访问

由于Python不像Java，有访问控制符（private / public / protected），所以Python的访问控制也是容易被应聘者忽视和搞错的。

# 公有（Public）

在Python的类中，默认情况下定义的属性都是公有的。

```python
class Foo(object):
	bar = 123

	def __init__(self, bob):
		self.bob = bob

print(Foo.bar)  # 123

foo = Foo(456)
print(foo.bob)  # 456
```

上面类`Foo`中的`bar`属性就是类属性，`__init__`方法中定义的bob是实例属性，`bar`和`bob`都是公有的属性，外部可以访问，分别print类中的`bar`和实例中的`bob`，输出了对应的值。

# 受保护（Protected）

在Python中定义一个受保护的属性，只需要在其名字前加一个下划线`_`，我们将Foo方法中的`bob`和`bar`改为`_bob`和`_bar`，他们就变成了受保护的属性了，代码如下：

```python
class Foo(object):
	_bar = 123

	def __init__(self, bob):
		self._bob = bob


class Son(Foo):

	def print_bob(self):
		print(self._bob)

	@classmethod
	def print_bar(cls):
		print(cls._bar)


Son.print_bar()  # 123

son = Son(456)
son.print_bob()  # 456
```

定义一个类`Son`继承自`Foo`，由于受保护的对象只能在类的内部和子类中被访问，不能直接调用`print(Son._bar)`或`print(son._bob)`来输出这两个属性的值，所以定义了`print_bar`和`print_bob`方法，实现在子类中输出，这段代码也正常的输出了`_bar`和`_bob`的值。

接下来，试着反向验证一下，在类的外部，能不能访问其属性，将上面代码的输出部分修改如下：

```python
print(Son._bar)  # 123

son = Son(456)
print(son._bob)  # 456
```

（假装）惊讶的发现，竟然没有报错，也输出了正确的值。

Python中用加下划线来定义受保护变量，是一种约定的规范，而不是语言层面真的实现了访问控制，所以，我们定义的保护变量，依然可以在外部被访问到（这是个feature，不是bug）。

# 私有（private）

Python定义私有属性，需要在属性名前加两个下划线`__`，把上面的代码修改一下，运行一下会发现下面的代码中的任何一个print都会报错的。

```python
class Foo(object):
	__bar = 123

	def __init__(self, bob):
		self.__bob = bob


class Son(Foo):

	def print_bob(self):
		print(self.__bob)  # Error

	@classmethod
	def print_bar(cls):
		print(cls.__bar)  # Error


print(Son.__bar)  # Error

son = Son(456)
print(son._bob)  # Error
```

## 深入一下——私有属性真的就访问不到了吗？

要了解私有属性是否真的访问不到，需要从Python是如何实现私有属性入手。CPython中，会把双下划线的属性变为`_ClassName__PropertyName`的形式，用代码演示一下：

```python
class Foo(object):
	__bar = 123


print(Foo._Foo__bar)  # 123
```

运行一下可以知道，正常输出了`__bar`的值，但是不推荐这样去访问私有属性，因为不同的Python解释器对于私有属性的处理不一样。

## 特例

使用双下划线定义私有属性，有一种特殊情况，当属性后也有两个下划线的时候，这个属性会被Python解释器当做魔术方法，从而不做私有处理。

```python
class Foo(object):
	__bar__ = 123


print(Foo.__bar__)  # 123
```

上面代码输出了123，证明Python解释器并没有把`__bar__`当做私有属性。当定义私有属性时，需要注意名字最后最多只能有一个下划线。

## 另一个特例

假如定义的属性名就叫`__`呢？不妨直接试一下：

```python
class Foo(object):
	__ = 123


print(Foo.__)  # 123
```

可以发现名字叫`__`的属性也不会被认为是私有属性，名字是多个下划线的属性也不是私有属性（比如`_______`）。

# 函数的访问控制

前面主要介绍了属性的访问控制，在Python中函数是一等公民，所谓一等公民，就是函数可以像变量一样使用，所以函数的访问控制和属性一样，一样应用上面的规则。
