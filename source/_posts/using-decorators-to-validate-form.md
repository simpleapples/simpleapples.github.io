---
layout: post
title: 用装饰器封装Flask-WTF表单验证逻辑
date: 2018-04-26 16:15
comments: true
categories: Python
---

> Don't repeat yourself

在使用Flask-WTF的时候，常会用下面这样的代码来验证表单数据的合法性：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = TestForm()
	# 判断是否合法
	if not form.validate_on_submit():
		return 'err', 400
	# 主要逻辑
```

对于有很多提交接口的项目来说，需要在每个路由下写相同的的逻辑，造成了大量的代码重复。在Flask-Login中，要把一个路由设置为登录后才能访问，只需要在路由上加一个@login_required装饰器，不需要额外的代码。能不能像Flask-Login一样，用装饰器来封装对表单的验证逻辑呢？

# 实现表单验证装饰器

由于不同路由使用的表单类不一样，所以需要为装饰器传入一个表单类参数，并且在路由函数中需要用到表单中的值，所以还需要将验证通过的表单传给路由函数。

上代码：

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

使用方式如下：

```python
@validate_form(TestForm)  # 需要传入要验证的表单类
@app.route('/', methods=['GET', 'POST'])
def index(form):
    # 执行到这里说明表单验证通过
```

经过在项目中的应用，发现装饰器还是有一些缺陷：

- 无法自定义处理非法表单的逻辑
- 不支持get方式提交的表单（查看validate_on_submit()源码可知其只支持对post和put方式提交的表单进行验证）

# 丰富一下

要自定义处理非法表单的逻辑，需要增加一个可以传入自定义逻辑的接口。表单非法时接口的返回往往是一致的，所以我们为所有应用装饰器的路由传入一个统一的处理逻辑。将装饰器封装在一个类中，在类中添加一个配置处理逻辑的方法。

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

error_handler也是一个装饰器，被它修饰的方法就是处理非法表单的方法。

```python
@form_validator.error_handler
def error_handler(errors):
    return jsonify({'errors': errors}), 400
```

接下来支持get方法，在flask中，我们可以通过request.args来获取到get方法提交的参数。思路是用获取到的参数生成一个表单类的实例，然后就可以通过调用表单类的validate()方法来判断是否合法了。修改validate_form装饰器：

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

大功告成！使用上面的装饰器，就可以免除在路由函数中重复写表单验证逻辑，并且同时支持put、post和get方法提交的表单。

# 开箱即用

笔者已经把上面的代码封装成了一个库发布到了PyPI，想直接用的朋友可以使用`pip install flask-wtf-decorators`安装，项目源码也已经发布到Github。

[查看PyPI](https://pypi.org/project/Flask-WTF-Decorators/)

[查看Github](https://github.com/simpleapples/flask-wtf-decorators)

# 欢迎关注Python私房菜

![](/upload/wechat-qrcode.jpg)
