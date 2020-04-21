---
layout: post
title: 你所不知道的Python | 函数参数的演进之路
date: 2018-07-10 10:08
comments: true
categories: Python
---

![](/upload/20180710_01.png)

函数参数处理机制是Python中一个非常重要的知识点，随着Python的演进，参数处理机制的灵活性和丰富性也在不断增加，使得我们不仅可以写出简化的代码，也能处理复杂的调用。

# 关键字参数

**调用时指定参数的名称，且与函数声明时的参数名称一致。**

关键字参数是Python函数中最基础也最常见的，我们写一个记账的函数，参数是需要记录的时间和金额。

```python
def add_record(date, amount):
	print('date:', date, 'amount:', amount)
```

这里的amount参数就是一个关键字参数，关键字参数支持两种调用方式：

- **位置调用**
- **关键字调用**

位置调用，就是按参数的位置进行调用，例如传入两个参数，第一个是字符串2018-07-06，第二个是整数10，那么这两个参数会被分别赋予date和amount变量，如果顺序反过来，则这两个参数分别赋予amount和date变量。

```python
add_record('2018-07-06', 10)  # 输出date: 2018-07-06 amount: 10
add_record(10, '2018-07-06')  # 输出date: 10 amount: 2018-07-06
```

关键字调用，可以忽略参数顺序，直接指定参数。

```python
add_record(amount=10, date='2018-07-06')  # 虽然参数顺序反了，但是使用了关键字调用，所以依然输出date: 2018-07-06 amount: 10
```

# 仅限关键字参数

我们定义一个Person类，并实现它的`__init__`方法

```python
class Person(object):
	def __init__(self, name, age,  gender, height, weight):
		self._name = name
		self._age = age
		self._gender = gender
		self._height = height
		self._weight = weight
```

当初始化这个类的时候，我们可以使用关键字调用，也可以使用位置调用。

```python
Person('Wendy', 24, 'female', 160, 48)
Person('John', age=27, gender='male', height=170, weight=52)
```

对比上面两种方式，我们会发现参数多的时候通过关键字指定参数不仅更加清晰，也更具有可读性。如果我们希望函数只允许关键字调用，该如何做呢？Python 3.0中，引入了一种新的仅限关键字参数，能实现我们的需求。

下面将age以后的参数修改为只允许关键字调用，定义函数时想指定仅限关键字参数，要把它们放到前面有星号的参数后面，在Python中有星号的参数是可变参数的意思，如果不想支持可变参数，可以在参数中放一个星号作为分割。

```python
class Person(object):
        # 参数中的星号作为关键字参数和仅限关键字参数的分割
	def __init__(self, name, *, age='22', gender='female', height=160, weight=50):
		self._name = name
		self._age = age
		self._gender = gender
		self._height = height
		self._weight = weight

Person('Wendy', 24, 'female', 160, 48)  # 报错，age以后参数不允许位置调用
Person('John', age=27, gender='male', height=170, weight=52)  # 正常执行
```

普通参数和仅限关键字参数中间由一个星号隔离开，星号以后的都是仅限关键字参数，只可以通过关键字指定，而不能通过位置指定。

# 参数默认值

**在函数声明时，指定参数默认值，调用时不传入参数则使用默认值，相当于可选参数。**

```python
def add_record(date, amount=0):
	print('date:', date, 'amount:', amount)

add_record('2018-07-06')  # 输出date: 2018-07-06 amount: 0
```

上面代码中没有传入amount参数，所以amount直接被置为默认值0。有一点需要注意的是，**默认参数需要设置在必选参数后面**，并且默认参数既可以通过位置调用，也可以通过关键字调用。

```python
add_record('2018-07-06', 10)  # 通过位置指定参数
add_record('2018-07-06', amount=10)  # 通过位置指定参数
add_record(amount=10, '2018-07-06')  # 报错，默认参数必须在必选参数后面
```

参数默认值既支持关键字参数，也支持仅限关键字参数。

# 可变长参数

**“可变长”顾名思义是允许在调用时传入多个参数，可变长参数适用于参数数量不确定的场景，可变参数有两种，一种是关键字可变长参数，另一种是非关键字可变长参数。**

非关键字可变长参数的写法是在参数名前加一个星号，Python会将这些多出来的参数的值放入一个元组中，由于元组中只有参数值而没有参数名称，所以是关键字参数。

```python
def print_args(*args):
	print(args)

print_args(1, 2, 3, 4, 5)  # 输出元组(1, 2, 3, 4, 5)

a = [1, 2, 3, 4, 5]
print_args(a)  # 直接传入时，列表a会被当作一个元素，所以输出([1, 2, 3, 4, 5],)
print_args(*a)  # 在传参时加星号可以将可迭代参数解包，所以列表a中每一个元素都被当作一个参数传入，输出(1, 2, 3, 4, 5)
```

关键字可变长参数的写法是在参数名前加两个星号，Python会将这些多出来的参数的值放入一个字典中，由于字典中只有参数值而没有参数名称，所以是非关键字参数。

```python
def print_kwargs(**kw_args):
	print(kw_args)

a = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print_kwargs(**a)  # 使用关键字可变参数时， {'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4}
```

# 函数注解

Python 3中为函数定义增加的另一个新功能是函数注解，所谓函数注解，就是可以在函数参数和返回值上添加任意的元数据。

```python
def create_person(name: str, age: int, gender: str = 'female', height: int = 160)  -> bool:
	return True
```

用create_person方法举例，可以看到在每个参数后面都跟了一个参数类型，在函数后面则是返回值类型，函数注解可以用在文档编写、类型检查中，在支持函数注解的IDE中，如果传入参数和返回的类型不符合函数注解中的类型，IDE会提示错误。

但是函数注解只是一个元数据，Python解释器执行时候并不会去检查类型，所以下面这种情况也是合法的。

```python
Person(name=123, age='John')  # 并不会报错
```

# 总结

Python有着非常好入门的特点，但是随着语言本身的演进，很多高级功能也在持续加入，用好这些功能可以使我们的Python代码拥有更高的可读性，适应更加复杂的应用场景。
