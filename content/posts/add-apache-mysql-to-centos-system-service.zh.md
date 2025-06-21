---
date: "2012-10-19T12:59:00+00:00"
title: "将Apache和Mysql添加为CentOS服务"
categories:
  - Mac&Linux
---

当安装自己编译的 Apache 和 Mysql 后，默认是不添加为系统服务的，所以我们需要手动将其添加为服务。

添加 Apache 为系统服务

1.将 apachectl 拷贝到 init.d 下

    #cp /usr/local/apache/bin/apachectl /etc/rc.d/init.d/httpd

2.修改 httpd

    #vi /etc/rc.d/init.d/httpd

添加以下注释内容

    #chkconfig: 345 85 15
    #decription: apache server

3.向系统服务添加 apache

    #chkconfig --add httpd

添加 Mysql 为系统服务

1.  将 mysql 拷贝到 init.d 下

        #cp /usr/local/mysql5/share/mysql/mysql.server /etc/init.d/mysqld

2.  将 mysqld 添加到系统服务

        #chkconfig --add mysqld

完成上述步骤，就可以使用

    #service httpd/mysqld restart/start/stop

来控制 apache/mysql 的启动停止重启了
