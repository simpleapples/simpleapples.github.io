---
date: "2020-03-31T12:50:00+00:00"
title: "使用Pipfile代替reqirements.txt"
categories:
  - Python
---

很多语言都提供了环境隔离的支持，例如nodejs的node_module，golang的go mod，python也有virtualenv和pyvenv等机制。为了建立依赖快照，通常会用`pip freeze > requirements.txt` 命令生成一个requirements.txt文件，在一些场景下这种方式就可以满足需求，但是在复杂场景下requirements.txt就力不从心了。

### requirements.txt

```
appdirs==1.4.3
astroid==2.3.3
attrs==19.3.0
black==19.3b0
certifi==2019.11.28
chardet==3.0.4
click==7.1.1
et-xmlfile==1.0.1
Flask==1.1.1
gevent==1.4.0
greenlet==0.4.15
idna==2.9
isort==4.3.21
itsdangerous==1.1.0
jdcal==1.4.1
Jinja2==2.11.1
lazy-object-proxy==1.4.3
MarkupSafe==1.1.1
mccabe==0.6.1
numpy==1.18.2
openpyxl==3.0.3
pandas==1.0.3
pylint==2.4.4
python-dateutil==2.8.1
pytz==2019.3
requests==2.23.0
six==1.14.0
tinydb==3.15.2
toml==0.10.0
typed-ast==1.4.1
urllib3==1.25.8
Werkzeug==1.0.0
wrapt==1.11.2
```

requirements.txt文件中只记录了依赖的版本，所以如果遇到官方的pypi源下载速度慢，需要使用更快的国内镜像下载，通常只能使用`pip install -i`安装或者修改全局的pip.conf文件。

当某个项目使用确定的python版本，这个版本也并不能在requirements.txt中体现，只能通过readme或者文档来记录，并且需要在创建虚拟环境时手动调用正确的python版本。

项目需要使用flake8、pylint、black等代码优化工具时，这些依赖也会被`pip freeze`命令写入requirements.txt中，然而这些依赖是不需要出现在生产环境的。

### Pipfile

Pipenv的出现，一举解决了上面的问题，Pipenv是Kenneth Reitz在2017年1月发布的Python依赖管理工具，他所基于的Pipfile则用来替代requirements.txt。

```
[[source]]
name = "pypi"
url = "https://pypi.doubanio.com/simple"
verify_ssl = false

[dev-packages]
isort = "*"
black = "==19.3b0"
pylint = "*"

[packages]
flask = "*"
tinydb = "*"
pandas = "*"
requests = "*"
gevent = "*"
openpyxl = "*"

[requires]
python_version = "3.6"
```

#### 好处1：记录内容更详细

相比于requirements.txt，Pipfile多了pip源的设置，可以针对不同项目使用不同环境。并且将依赖分为dev和默认环境，例如pylint、flake8、black等依赖，可以将他们放入dev依赖中。

#### 好处2：减少手动激活虚拟环境次数

pipenv将virtualenv、pyvenv和pip命令整合使用，pipenv减少了手动激活虚拟环境的次数，使用pyvenv模块运行main.py，需要先执行`source venv/bin/activate`激活虚拟环境，然后再执行`python main.py`，而pipenv只需要在项目根目录执行`pipenv run main.py` ，就可以自动激活当前虚拟环境并执行main.py。如果需要安装依赖的，直接执行`pipenv install xxx`，也不需要先激活虚拟环境，再使用`pip install xxx`安装。

####  好处3：锁机制

从Pipfile文件添加或删除安装的包，会生成Pipfile.lock来锁定安装包的版本和依赖信息，通过pipfile.lock文件，可以精确恢复以来的版本。

### 常用命令
```
# 初始化虚拟环境（可自己指定python版本）
$ pipenv --python 3.6.9

# 激活当前项目虚拟环境
$ pipenv shell

# 安装开发依赖包
$ pipenv install black --dev

# 生成lock文件
$ pipenv lock
```
