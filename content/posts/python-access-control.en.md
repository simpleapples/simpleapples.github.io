---
date: "2018-03-30T17:54:00+00:00"
title: "Chatting with the Interviewer | Python Object-Oriented Access Control"
categories:
  - Python
---

Python was designed as an object-oriented language from the start, and the first element of object-oriented thinking is encapsulation. Simply put, encapsulation means that the attributes and methods within a class are divided into public and private; public ones can be accessed externally, while private ones cannot. This is the most crucial concept in encapsulation—access control.

![Object-Oriented Programming](/images/20180330_01.jpg)

There are three levels of access control: Private, Protected, and Public.

Private: Accessible only within the class itself.  
Protected: Accessible within the class itself and its subclasses.  
Public: Accessible by any class.

Since Python, unlike Java, does not have access control modifiers (private/public/protected), access control in Python is often overlooked or misunderstood by job applicants.

# Public

In Python classes, attributes defined by default are public.

```python
class Foo(object):
    bar = 123

    def __init__(self, bob):
        self.bob = bob

print(Foo.bar)  # 123

foo = Foo(456)
print(foo.bob)  # 456
```

In the class `Foo`, the `bar` attribute is a class attribute, and `bob` defined in the `__init__` method is an instance attribute. Both `bar` and `bob` are public attributes and can be accessed externally. The values of `bar` in the class and `bob` in the instance are printed, showing the corresponding values.

# Protected

To define a protected attribute in Python, simply prefix its name with an underscore `_`. Let's modify the `bob` and `bar` in the `Foo` method to `_bob` and `_bar`, making them protected attributes, as shown in the code below:

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

We define a class `Son` that inherits from `Foo`. Since protected objects can only be accessed within the class and its subclasses, you cannot directly call `print(Son._bar)` or `print(son._bob)` to output these attributes' values. Therefore, we define `print_bar` and `print_bob` methods to output them in the subclass, and this code correctly outputs the values of `_bar` and `_bob`.

Next, let's try to verify in reverse whether these attributes can be accessed externally by modifying the output part of the above code as follows:

```python
print(Son._bar)  # 123

son = Son(456)
print(son._bob)  # 456
```

(Surprisingly) we find that no error is reported, and the correct values are output.

In Python, using an underscore to define protected variables is a convention, not a language-level implementation of access control. Therefore, our protected variables can still be accessed externally (this is a feature, not a bug).

# Private

To define private attributes in Python, prefix the attribute name with two underscores `__`. Modify the above code and run it to find that any `print` in the following code will result in an error.

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

## Delving Deeper—Can Private Attributes Really Not Be Accessed?

To understand whether private attributes can truly not be accessed, we need to look at how Python implements private attributes. In CPython, double underscore attributes are transformed into the form `_ClassName__PropertyName`. Here's a demonstration with code:

```python
class Foo(object):
    __bar = 123


print(Foo._Foo__bar)  # 123
```

Running this code shows that the value of `__bar` is output correctly, but accessing private attributes this way is not recommended because different Python interpreters handle private attributes differently.

## Special Case

When using double underscores to define private attributes, there is a special case where if the attribute also ends with two underscores, it will be treated as a magic method by the Python interpreter and not handled as a private attribute.

```python
class Foo(object):
    __bar__ = 123


print(Foo.__bar__)  # 123
```

The code above outputs 123, proving that the Python interpreter does not treat `__bar__` as a private attribute. When defining private attributes, note that the name can have at most one trailing underscore.

## Another Special Case

What if the attribute name is just `__`? Let's try it directly:

```python
class Foo(object):
    __ = 123


print(Foo.__)  # 123
```

We find that an attribute named `__` is also not considered a private attribute, and attributes with multiple underscores (e.g., `_______`) are not private attributes either.

# Access Control for Functions

The above mainly introduced access control for attributes. In Python, functions are first-class citizens, meaning they can be used like variables. Therefore, access control for functions follows the same rules as for attributes.