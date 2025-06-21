---
date: "2020-03-31T12:50:00+00:00"
title: "Using Pipfile Instead of requirements.txt"
categories:
  - Python
---

Many programming languages provide support for environment isolation, such as Node.js with node_modules, Golang with go mod, and Python with virtualenv and pyvenv. To create a dependency snapshot, the `pip freeze > requirements.txt` command is often used to generate a requirements.txt file. In some scenarios, this method suffices, but in more complex situations, requirements.txt falls short.

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

The requirements.txt file only records the versions of dependencies. If the official PyPI source is slow, and you need to use a faster domestic mirror, you typically have to use `pip install -i` or modify the global pip.conf file.

When a project uses a specific Python version, this version cannot be reflected in requirements.txt; it must be documented in the README or other documentation, and the correct Python version must be manually invoked when creating a virtual environment.

When projects need to use code optimization tools like flake8, pylint, or black, these dependencies are also written into requirements.txt by the `pip freeze` command, even though they are not needed in the production environment.

### Pipfile

The emergence of Pipenv has solved these issues. Pipenv is a Python dependency management tool released by Kenneth Reitz in January 2017, and it uses Pipfile to replace requirements.txt.

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

#### Benefit 1: More Detailed Records

Compared to requirements.txt, Pipfile includes the pip source settings, allowing different environments for different projects. Dependencies are divided into dev and default environments; for example, pylint, flake8, and black can be placed in the dev dependencies.

#### Benefit 2: Fewer Manual Activations of Virtual Environments

Pipenv integrates the use of virtualenv, pyvenv, and pip commands, reducing the number of times you need to manually activate a virtual environment. To run main.py using the pyvenv module, you first need to execute `source venv/bin/activate` to activate the virtual environment, then execute `python main.py`. With pipenv, you only need to execute `pipenv run main.py` in the project's root directory to automatically activate the current virtual environment and run main.py. If you need to install dependencies, simply execute `pipenv install xxx` without first activating the virtual environment and using `pip install xxx`.

#### Benefit 3: Lock Mechanism

Adding or removing installed packages from the Pipfile generates a Pipfile.lock to lock the versions and dependency information of the installed packages. The pipfile.lock file allows you to precisely restore dependency versions.

### Common Commands
```
# Initialize a virtual environment (you can specify the Python version)
$ pipenv --python 3.6.9

# Activate the virtual environment for the current project
$ pipenv shell

# Install development dependencies
$ pipenv install black --dev

# Generate a lock file
$ pipenv lock
```