---
date: "2015-06-11T11:00:00+00:00"
title: "在阿里云CentOS7中配置基于Nginx+Supervisor+Gunicorn的Flask项目"
categories:
  - Python
---

需要在阿里云的CentOS7中搭建Flask应用的生产环境，记录一下。

## 配置Centos7

root登录后，首先新建一个普通用户并设置密码

``` 
adduser user
passwd user
```

接下来将用户的公钥复制到~/.ssh中，命名为authorised_keys，修改/etc/ssh/sshd_config禁用ssh中的root登录，修改默认ssh端口，并使用证书登陆，修改如下内容

``` 
Port 65535
PasswordAuthentication no
PermitRootLogin no
```

配置完成后重启ssh服务

``` 
systemctl restart sshd.service
```

CentOS7中用firewalld替换了iptables，需要手动将80端口和修改后的ssh端口添加到firewalld中

``` 
firewalld --add-port 80/tcp --permanent
firewalld --add-port 65535/tcp --permanent
firewalld --reload
```

## 配置Nginx

yum中可以直接安装nginx

``` 
yum install nginx
```

安装好后在/etc/nginx/default.d中添加location的配置，并指向8001端口，以后Flask会监听8001端口

``` 
location / {
	proxy_pass http://127.0.0.1:8001
}
```

配置好后重新载入nginx配置

``` 
systemctl reload nginx.service
```

## 安装Python

CentOS自带Python2.7，如果使用Python3，需要单独安装。

``` 
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar xf Python-3.4.3.tgz
cd Python-3.4.3
./configure --prefix=/usr/local --enable-shared
make
make altinstall
```

接下来在项目中搭建虚拟环境，Python2虚拟环境使用virtualenv安装（使用pip install virtualenv命令安装），Python3环境使用pyvenv安装（Python3自带pyvenv），以Python3环境为例，在Web项目中，建立虚拟环境文件夹venv

``` 
pyvenv venv
```

接下来在项目路径下启用虚拟环境

``` 
source venv/bin/active
```

退出虚拟环境使用Ctrl+C或deactive命令

## 安装配置Gunicorn

Gunicorn使用pip install gunicorn安装，注意需要在虚拟环境中使用pip安装，这样才对应虚拟环境中的Python版本。安装好后，新建一个Gunicorn的配置文件，比如deploy_config.py，加入内容如下

``` 
import os
bind='127.0.0.1:8001' #绑定的端口
workers=4	#worker数量
backlog=2048
debug=True
proc_name='gunicorn.pid'
pidfile='/var/log/gunicorn/debug.log'
loglevel='debug'
```

保存文件后在虚拟环境中使用Gunicorn尝试启动

``` 
gunicorn -c deploy_config.py myapp:app
```

myapp是入口Python文件名，app是函数名。如果输出worker相关信息，表明启动成功。

## 安装配置Supervisor

yum可以直接安装Supervisor，需要注意的是Supervisor只支持Python2，所以不要在虚拟环境中使用pip安装supervisor。

``` 
yum install supervisor
```

安装后，在/etc/supervisord.d中建立配置文件xxx.ini，内容如下

``` 
[program:xxx]
command=/var/proj/xxx/venv/bin/python /usr/bin/gunicorn -c /var/proj/xxx/deploy_config.py myapp:app
autorstart=true
directory=/var/proj/xxx
autorestart=true
startsecs=10
startretries=20
```

xxx是项目名称，注意command中最好都写全路径，以区别系统环境和项目虚拟环境。完成后启动supervisord，使配置生效

``` 
supervisord -c /etc/supervisord.conf
```

