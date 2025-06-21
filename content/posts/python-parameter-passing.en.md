---
date: "2018-04-22T14:38:00+00:00"
title: "Python Parameter Passing: Neither Pass-by-Value Nor Pass-by-Reference"
categories:
  - Python
---

![](/images/20180422_01.png)

Have you ever been asked in an interview whether Python passes parameters by reference or by value? Have you heard the notion that Python parameter passing is neither pass-by-value nor pass-by-reference? Even a small default parameter value can sometimes cause bugs that are hard to trace?

If you've encountered any of these issues, let's delve into the various aspects of Python function parameter passing.

# Everything is an Object

In Python, there's a crucial concept: everything is an object. Whether it's a number, a string, an array, or a dictionary, in Python, they all exist as objects.

```python
a = 123
```

For the above line of code, Python interprets it as creating a PyObject with the value 123, and then defining a pointer `a` that points to this PyObject.

# Mutable and Immutable Objects

Python objects are divided into two types: mutable and immutable. Immutable objects include types like `tuple`, `str`, `int`, etc., while mutable objects include types like `dict`, `list`, custom objects, etc. Let's use some code to illustrate their differences.

```python
a = [1, 2, 3]
print(id(a))  # 2587116690248
a += [4]
print(id(a)) # 2587116690248

b = 1
print(id(b)) # 2006430784
b += 1
print(id(b)) # 2006430816
```

In the code above, we define a mutable object and an immutable object, modify them, and print their identifiers before and after modification. We find that modifying a mutable object does not change the variable's reference, while modifying an immutable object does change the variable's reference.

![Reference of a Mutable Object](/images/20180422_02.png)

The image above shows a mutable object. When modifying the object, such as removing an element from an array, the object itself does not change its identifier.

![Reference of an Immutable Object](/images/20180422_03.png)

When changing an immutable object, such as adding 2 to an `int`, syntactically it looks like the object `i` is directly modified. However, as mentioned earlier, `i` is just a variable pointing to the object 73. Python will create a new object after adding 2 to the object `i` points to, and then point `i` to this new object.

# Behavior During Parameter Passing

With an understanding of object principles, we can attempt to understand their different behaviors during parameter passing.

```python
a = [1, 2, 3]
print(id(a))  # 1437494204232
def mutable(a):
	print(id(a))  # 1437494204232
	a += [4]
	print(id(a))  # 1437494204232
mutable(a)

b = 1
print(id(b))  # 2006430784
def immutable(b):
	print(id(b))  # 2006430784
	b += 1
	print(id(b))  # 2006430816
immutable(b)
```

From the code above, we can see that modifying a passed mutable parameter affects the external object, while modifying an immutable parameter does not.

**In summary, Python parameter passing is neither pass-by-object nor pass-by-reference. The differences arise from Python's object mechanism, where parameter passing simply binds a new variable to the object (essentially passing a pointer in C).**

# Pitfalls of Parameter Passing

Understanding the logic of parameter passing, we need to be aware of potential issues this logic might cause.

```python
def test(b=[]):
	b += [1]
	print(b)

test()  # [1]
test()  # [1, 1]
test()  # [1, 1, 1]
```

The output of the code above, according to the logic of mutable object parameter passing, should be `[1]` each time it's called. However, the actual output seems like the default parameter only took effect once. The reason is that Python functions are also objects (everything is an object), and this object is initialized only once. Since the parameter is a mutable object, each call modifies the same object.

To solve this issue, it's recommended to set the default value to `None` when passing mutable objects as parameters, and then assign a default value inside the function after checking for `None`.

```python
def test(b=None):
	b = b or []
	b += [1]
	print(b)

test()  # [1]
test()  # [1]
test()  # [1]
```

Let's look at another piece of code.

```python
i = 1
def test(a=i):
	print(a)

i = 2
test()  # 1
```

Since the default parameter value is determined at the time of function definition, not at the time of function execution, the default value of the `test` method's parameter is 1, not 2.