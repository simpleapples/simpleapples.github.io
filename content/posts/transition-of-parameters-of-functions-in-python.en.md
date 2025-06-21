---
date: "2018-07-10T10:08:00+00:00"
title: "The Evolution of Python Function Parameters You Didn't Know About"
categories:
  - Python
---

![](/images/20180710_01.png)

The mechanism for handling function parameters is a crucial aspect of Python. As Python has evolved, the flexibility and richness of parameter handling have continuously increased, allowing us to write simplified code and handle complex calls.

# Keyword Arguments

**Specify the parameter's name when calling, matching the parameter name in the function declaration.**

Keyword arguments are the most basic and common in Python functions. Let's write a bookkeeping function with parameters for the date and amount to be recorded.

```python
def add_record(date, amount):
	print('date:', date, 'amount:', amount)
```

Here, the `amount` parameter is a keyword argument, which supports two calling methods:

- **Positional Call**
- **Keyword Call**

A positional call is made by the order of parameters. For example, if you pass in two parameters, the first being the string '2018-07-06' and the second an integer 10, these parameters will be assigned to the `date` and `amount` variables respectively. If the order is reversed, the parameters will be assigned to `amount` and `date`.

```python
add_record('2018-07-06', 10)  # Output: date: 2018-07-06 amount: 10
add_record(10, '2018-07-06')  # Output: date: 10 amount: 2018-07-06
```

A keyword call allows you to ignore the parameter order and directly specify the parameters.

```python
add_record(amount=10, date='2018-07-06')  # Although the parameter order is reversed, using a keyword call still outputs: date: 2018-07-06 amount: 10
```

# Keyword-Only Arguments

Let's define a `Person` class and implement its `__init__` method.

```python
class Person(object):
	def __init__(self, name, age, gender, height, weight):
		self._name = name
		self._age = age
		self._gender = gender
		self._height = height
		self._weight = weight
```

When initializing this class, you can use either keyword or positional calls.

```python
Person('Wendy', 24, 'female', 160, 48)
Person('John', age=27, gender='male', height=170, weight=52)
```

Comparing the two methods above, you'll find that specifying parameters using keywords is not only clearer but also more readable when there are many parameters. If we want the function to only allow keyword calls, how can we achieve this? In Python 3.0, a new keyword-only parameter feature was introduced to meet this need.

To modify parameters after `age` to only allow keyword calls, you need to place them after a parameter with an asterisk in the function definition. In Python, an asterisk indicates a variable-length parameter. If you don't want to support variable-length parameters, you can use an asterisk as a separator in the parameters.

```python
class Person(object):
        # The asterisk in the parameters acts as a separator between keyword and keyword-only parameters
	def __init__(self, name, *, age='22', gender='female', height=160, weight=50):
		self._name = name
		self._age = age
		self._gender = gender
		self._height = height
		self._weight = weight

Person('Wendy', 24, 'female', 160, 48)  # Error, parameters after age do not allow positional calls
Person('John', age=27, gender='male', height=170, weight=52)  # Executes normally
```

Ordinary parameters and keyword-only parameters are separated by an asterisk. Parameters after the asterisk are keyword-only and can only be specified by keywords, not by position.

# Default Parameter Values

**Specify default values for parameters in the function declaration. If no arguments are passed during the call, the default values are used, making them optional parameters.**

```python
def add_record(date, amount=0):
	print('date:', date, 'amount:', amount)

add_record('2018-07-06')  # Output: date: 2018-07-06 amount: 0
```

In the code above, the `amount` parameter was not passed, so it defaults to 0. Note that **default parameters must be set after required parameters** and can be specified by either position or keyword.

```python
add_record('2018-07-06', 10)  # Specify parameters by position
add_record('2018-07-06', amount=10)  # Specify parameters by keyword
add_record(amount=10, '2018-07-06')  # Error, default parameters must follow required parameters
```

Default parameter values support both keyword and keyword-only parameters.

# Variable-Length Parameters

**"Variable-length" implies allowing multiple parameters during the call. Variable-length parameters are suitable for scenarios with an uncertain number of parameters. There are two types: keyword variable-length parameters and non-keyword variable-length parameters.**

Non-keyword variable-length parameters are written by prefixing the parameter name with an asterisk. Python will place these extra parameter values into a tuple, as the tuple contains only parameter values and no parameter names, making them keyword parameters.

```python
def print_args(*args):
	print(args)

print_args(1, 2, 3, 4, 5)  # Outputs tuple (1, 2, 3, 4, 5)

a = [1, 2, 3, 4, 5]
print_args(a)  # When passed directly, list a is treated as a single element, so the output is ([1, 2, 3, 4, 5],)
print_args(*a)  # Adding an asterisk during passing unpacks iterable parameters, so each element in list a is treated as a parameter, outputting (1, 2, 3, 4, 5)
```

Keyword variable-length parameters are written by prefixing the parameter name with two asterisks. Python will place these extra parameter values into a dictionary, as the dictionary contains only parameter values and no parameter names, making them non-keyword parameters.

```python
def print_kwargs(**kw_args):
	print(kw_args)

a = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print_kwargs(**a)  # Using keyword variable parameters results in {'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4}
```

# Function Annotations

Python 3 introduced another new feature for function definitions: function annotations. Function annotations allow you to add arbitrary metadata to function parameters and return values.

```python
def create_person(name: str, age: int, gender: str = 'female', height: int = 160) -> bool:
	return True
```

In the `create_person` method example, you can see that each parameter is followed by a type, and the function is followed by a return type. Function annotations can be used in documentation and type checking. In IDEs that support function annotations, if the passed parameters and return types don't match the function annotations, the IDE will show an error.

However, function annotations are just metadata. The Python interpreter does not check types during execution, so the following is also valid:

```python
Person(name=123, age='John')  # No error
```

# Summary

Python is known for being beginner-friendly, but as the language itself evolves, many advanced features continue to be added. Using these features effectively can enhance the readability of our Python code and adapt to more complex application scenarios.