---
date: "2018-06-28T23:51:00+00:00"
title: "The Secrets of Python You Didn't Know | String Concatenation"
categories:
  - Python
---

![](/images/20180628_04.jpg)

String concatenation is the process of merging two or more strings into one. While it may seem like a basic problem, in Python, there are multiple ways to achieve string concatenation. A poor choice can lead to performance issues.

# Method 1: Plus Operator

Many languages support using the plus operator for string concatenation, and Python is no exception. Simply add two or more strings together to concatenate them.

```python
a = 'Python'
b = 'Cuisine'
r = a + b  # Outputs 'PythonCuisine'
```

# Method 2: Using the % Operator

Before Python 2.6, the % operator was the only way to format strings, and it can also be used for string concatenation.

```python
a = 'Python'
b = 'Cuisine'
r = '%s%s' % (a, b)  # Outputs 'PythonCuisine'
```

# Method 3: Using the format Method

The format method, introduced in Python 2.6, is an alternative to the % operator for string formatting and can also be used for concatenation.

```python
a = 'Python'
b = 'Cuisine'
r = '{}{}'.format(a, b)
```

# Method 4: Using f-string

Formatted String Literals, or f-strings, were introduced in Python 3.6 as an evolution of the % operator and format method. The method of using f-strings for concatenation is similar to using the % operator and format method.

```python
a = 'Python'
b = 'Cuisine'
r = f'{a}{b}'
```

# Method 5: Using str.join() Method

Strings have a built-in join method, which takes a sequence type as its parameter, such as a list or tuple.

```python
a = 'Python'
b = 'Cuisine'
r = ''.join([a, b])
```

# Comparison Test

With so many methods available for string concatenation, which one should you choose? Let's evaluate the five methods in terms of code readability and performance.

Using the timeit module, we execute the example code for each of the five methods 100,000 times. The execution times are shown in the image below.

![](/images/20180628_05.png)

As seen, the % operator, format, and f-string are all string formatting methods, with performance increasing in that order. The performance of the plus operator is on par with f-string.

It's important to note that strings are immutable, so each time you use the plus operator to concatenate strings, a new string is generated. When concatenating multiple strings, inefficiency is inevitable. We increase the number of strings concatenated at once to 10 and 20, and conduct two more rounds of testing. Below are the results for concatenating 20 strings.

![](/images/20180628_06.png)

The results differ somewhat from concatenating two strings. First, when using the plus operator for a large number of strings (more than 10), performance drops sharply. The str.join() method performs best when concatenating a large number of strings.

# Summary

**When concatenating a small number of strings:**
Using the **plus** operator is wise for both performance and readability. If you have higher readability requirements and are using Python 3.6 or above, **f-string** is also a great choice. For example, in the following case, f-string is clearly more readable than the plus operator.

```python
a = f'Name: {name} Age: {age} Gender: {gender}'
b = 'Name: ' + name + ' Age: ' + age + ' Gender: ' + gender
```

**When concatenating a large number of strings:**
**join** and **f-string** are the best choices for performance. The choice still depends on your Python version and readability requirements. f-string may not always be the most readable when concatenating a large number of strings. Avoid using the plus operator, especially in a for loop.