---
date: "2015-06-11T11:00:00+00:00"
title: "Configuring a Flask Project with Nginx+Supervisor+Gunicorn on Alibaba Cloud CentOS7"
categories:
  - Python
---

This document records the setup of a production environment for a Flask application on Alibaba Cloud's CentOS7.

## Configuring CentOS7

After logging in as root, first create a new regular user and set a password:

``` 
adduser user
passwd user
```

Next, copy the user's public key to `~/.ssh`, name it `authorized_keys`, and modify `/etc/ssh/sshd_config` to disable root login via SSH, change the default SSH port, and use certificate login. Modify the following settings:

``` 
Port 65535
PasswordAuthentication no
PermitRootLogin no
```

After configuration, restart the SSH service:

``` 
systemctl restart sshd.service
```

In CentOS7, `firewalld` replaces `iptables`. You need to manually add port 80 and the modified SSH port to `firewalld`:

``` 
firewalld --add-port 80/tcp --permanent
firewalld --add-port 65535/tcp --permanent
firewalld --reload
```

## Configuring Nginx

Nginx can be installed directly via yum:

``` 
yum install nginx
```

After installation, add a location configuration in `/etc/nginx/default.d`, pointing to port 8001, which Flask will listen to:

``` 
location / {
	proxy_pass http://127.0.0.1:8001
}
```

Reload the Nginx configuration after setting it up:

``` 
systemctl reload nginx.service
```

## Installing Python

CentOS comes with Python 2.7. If you need Python 3, install it separately:

``` 
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar xf Python-3.4.3.tgz
cd Python-3.4.3
./configure --prefix=/usr/local --enable-shared
make
make altinstall
```

Next, set up a virtual environment in the project. Use `virtualenv` for Python 2 (install with `pip install virtualenv`) and `pyvenv` for Python 3 (Python 3 comes with `pyvenv`). For a Python 3 environment, create a virtual environment folder `venv` in the web project:

``` 
pyvenv venv
```

Activate the virtual environment in the project path:

``` 
source venv/bin/activate
```

Exit the virtual environment using Ctrl+C or the `deactivate` command.

## Installing and Configuring Gunicorn

Install Gunicorn using `pip install gunicorn`. Make sure to use pip within the virtual environment to match the Python version of the virtual environment. After installation, create a Gunicorn configuration file, such as `deploy_config.py`, with the following content:

``` 
import os
bind='127.0.0.1:8001' # Bound port
workers=4	# Number of workers
backlog=2048
debug=True
proc_name='gunicorn.pid'
pidfile='/var/log/gunicorn/debug.log'
loglevel='debug'
```

Save the file and try to start Gunicorn in the virtual environment:

``` 
gunicorn -c deploy_config.py myapp:app
```

`myapp` is the entry Python file name, and `app` is the function name. If worker-related information is output, it indicates a successful start.

## Installing and Configuring Supervisor

Supervisor can be installed directly via yum. Note that Supervisor only supports Python 2, so do not use pip to install Supervisor in the virtual environment.

``` 
yum install supervisor
```

After installation, create a configuration file `xxx.ini` in `/etc/supervisord.d` with the following content:

``` 
[program:xxx]
command=/var/proj/xxx/venv/bin/python /usr/bin/gunicorn -c /var/proj/xxx/deploy_config.py myapp:app
autorstart=true
directory=/var/proj/xxx
autorestart=true
startsecs=10
startretries=20
```

`xxx` is the project name. Ensure that the command paths are fully specified to distinguish between the system environment and the project virtual environment. After completion, start `supervisord` to apply the configuration:

``` 
supervisord -c /etc/supervisord.conf
```

