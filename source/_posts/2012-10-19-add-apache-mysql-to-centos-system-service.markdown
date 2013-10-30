---
layout: post
title: "将Apache和Mysql添加为CentOS服务"
date: 2012-10-19 12:59
comments: true
categories: Mac&Linux
---

当安装自己编译的Apache和Mysql后，默认是不添加为系统服务的，所以我们需要手动将其添加为服务。

添加Apache为系统服务

1.将apachectl拷贝到init.d下

	#cp /usr/local/apache/bin/apachectl /etc/rc.d/init.d/httpd

2.修改httpd

	#vi /etc/rc.d/init.d/httpd

添加以下注释内容

	#chkconfig: 345 85 15
	#decription: apache server

3.向系统服务添加apache

	#chkconfig --add httpd

添加Mysql为系统服务

1. 将mysql拷贝到init.d下

		#cp /usr/local/mysql5/share/mysql/mysql.server /etc/init.d/mysqld

2. 将mysqld添加到系统服务

		#chkconfig --add mysqld

完成上述步骤，就可以使用

	#service httpd/mysqld restart/start/stop

来控制apache/mysql的启动停止重启了