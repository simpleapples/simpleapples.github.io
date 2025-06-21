---
date: "2012-10-19T12:59:00+00:00"
title: "Add Apache and MySQL as CentOS Services"
categories:
  - Mac&Linux
---

When you install self-compiled Apache and MySQL, they are not added as system services by default, so we need to manually add them as services.

Adding Apache as a System Service

1. Copy `apachectl` to the `init.d` directory

   ```bash
   # cp /usr/local/apache/bin/apachectl /etc/rc.d/init.d/httpd
   ```

2. Edit `httpd`

   ```bash
   # vi /etc/rc.d/init.d/httpd
   ```

   Add the following comment lines:

   ```bash
   # chkconfig: 345 85 15
   # description: Apache server
   ```

3. Add Apache to the system services

   ```bash
   # chkconfig --add httpd
   ```

Adding MySQL as a System Service

1. Copy MySQL to the `init.d` directory

   ```bash
   # cp /usr/local/mysql5/share/mysql/mysql.server /etc/init.d/mysqld
   ```

2. Add `mysqld` to the system services

   ```bash
   # chkconfig --add mysqld
   ```

After completing the above steps, you can use:

   ```bash
   # service httpd/mysqld restart/start/stop
   ```

to control the start, stop, and restart of Apache/MySQL.