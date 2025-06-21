---
date: "2018-04-26T16:15:00+00:00"
title: "Encapsulating Flask-WTF Form Validation Logic with Decorators"
categories:
  - Python
---

> Don't repeat yourself

When using Flask-WTF, you often use the following code to validate the legitimacy of form data:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TestForm()
    # Check if valid
    if not form.validate_on_submit():
        return 'err', 400
    # Main logic
```

For projects with many submission interfaces, you need to write the same logic under each route, resulting in a lot of code duplication. In Flask-Login, to set a route to be accessible only after logging in, you just need to add a @login_required decorator to the route without any extra code. Can we encapsulate the form validation logic with a decorator like Flask-Login?

# Implementing a Form Validation Decorator

Since different routes use different form classes, the decorator needs to accept a form class parameter, and the validated form needs to be passed to the route function for use.

Here's the code:

```python
def validate_form(self, form_cls):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not form.validate_on_submit():
                return 'error', 400
            return fn(form, *args, **kwargs)
        return wrapper
    return decorator
```

Usage is as follows:

```python
@validate_form(TestForm)  # Pass in the form class to be validated
@app.route('/', methods=['GET', 'POST'])
def index(form):
    # Reaching here means form validation passed
```

After applying it in a project, some shortcomings of the decorator were discovered:

- Cannot customize the logic for handling invalid forms
- Does not support forms submitted via GET method (as seen in the validate_on_submit() source code, it only supports validation for forms submitted via POST and PUT methods)

# Enhancements

To customize the logic for handling invalid forms, an interface for passing custom logic needs to be added. The return of the interface for invalid forms is often consistent, so we pass a unified handling logic to all routes using the decorator. Encapsulate the decorator in a class and add a method for configuring the handling logic.

```python
from functools import wraps

from flask import request


class FormValidator(object):

    def __init__(self, error_handler=None):
        self._error_handler = error_handler

    def validate_form(self, form_cls):
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                if not form.validate_on_submit() and self._error_handler:
                    return self._error_handler(form.errors)
                return fn(form, *args, **kwargs)
            return wrapper
        return decorator

    def error_handler(self, fn):
        self._error_handler = fn
        return fn
```

The error_handler is also a decorator, and the method it decorates is the method for handling invalid forms.

```python
@form_validator.error_handler
def error_handler(errors):
    return jsonify({'errors': errors}), 400
```

Next, support for the GET method is added. In Flask, we can use request.args to get parameters submitted via the GET method. The idea is to generate an instance of the form class using the obtained parameters, and then use the form class's validate() method to check if it's valid. Modify the validate_form decorator:

```Python
def validate_form(self, form_cls):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.method == 'GET':
                form = form_cls(formdata=request.args)
            elif request.method in ('POST', 'PUT'):
                form = form_cls()
            else:
                return fn(*args, **kwargs)
            if not form.validate() and self._error_handler:
                return self._error_handler(form.errors)
            return fn(form, *args, **kwargs)
        return wrapper
    return decorator
```

Mission accomplished! Using the above decorator, you can avoid writing repetitive form validation logic in route functions, and it supports forms submitted via PUT, POST, and GET methods.

# Ready to Use

I've packaged the above code into a library and released it on PyPI. If you want to use it directly, you can install it with `pip install flask-wtf-decorators`. The project source code is also available on GitHub.

[View on PyPI](https://pypi.org/project/Flask-WTF-Decorators/)

[View on GitHub](https://github.com/simpleapples/flask-wtf-decorators)