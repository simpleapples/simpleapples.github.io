---
date: "2018-05-07T16:12:00+00:00"
title: "Do You Really Know How to Use Assertions Correctly?"
categories:
  - Python
---

![](/images/20180507_01.jpg)

# What is an Assertion

Assertions were invented as a debugging tool to check conditions that "should always be true if the code is correct." For example, if we want to assert that a variable `a` must be greater than 2, we can write:

```python
assert a > 2
```

When the condition is not met, an `AssertionError` exception is raised, equivalent to the following code:

```python
if not assert_condition:
    raise AssertionError
```

Since assertions are a debugging tool, Python's implementation aligns with this philosophy. In Python, the execution of the `assert` statement depends on the `__debug__` variable. The `assert` statement will only be executed if `__debug__` is true.

```python
if __debug__ and not assert_condition:
    raise AssertionError
```

By default, when we run a Python file, `__debug__` is set to True. It is only set to False when the `-O` or `-OO` parameter is used.

Create a new `assert.py` file and write the following code:

```python
print(__debug__)
assert 2 > 5
```

When running with `python assert.py`, `__debug__` will output True, and the statement `assert 2 > 5` will raise an `AssertionError`.

When running with `python -O assert.py`, `__debug__` will output False, and the statement `assert 2 > 5` will not execute, so no exception will be raised.

# Assertion or Exception

Let's consider these questions: In what situations should assertions be used? What is the difference between exceptions and assertions?

To summarize the usage scenarios for assertions and their difference from exceptions in one sentence:

> Use assertions to check preconditions, and exceptions to check postconditions.

Let's define a `read_file` function:

```python
def read_file(file_path):
    pass
```

The `read_file` function requires certain conditions to be met at the start of execution: `file_path` must be of type `str`. This condition is a precondition, and if it is not met, the function should not be called. If such a situation arises, it indicates a bug in the code. In this case, we can use an `assert` statement to infer the type of `file_path` and remind the programmer to modify the code. Such inference is not needed in a production environment. Although we could use an `if + raise` statement to achieve the same result as `assert`, it would be much more cumbersome.

```python
def read_file(file_path):
    assert isinstance(file_path, str)
```

After the `read_file` function is called and executed, it still needs to satisfy certain conditions, such as the file specified by `file_path` must exist and the current user must have permission to read it. These conditions are called postconditions, and for checking postconditions, we need to use exceptions.

```python
def read_file(file_path):
    assert isinstance(file_path, str)
    if not check_exist(file_path):
        raise NotFoundError()
    if not has_privilege(file_path):
        raise PermissionError()
```

File non-existence and lack of permission are not code bugs; they are part of the code logic. The upper-level code may execute other logic after catching these exceptions, so we cannot allow this part of the code to be ignored in a production environment. Moreover, compared to `assert` statements that can only raise `AssertionError`, using exceptions allows for more detailed errors, enabling the upper-level code to execute different logic for different errors.