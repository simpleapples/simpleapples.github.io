---
date: "2012-10-19T12:39:00+00:00"
title: "MacOS+VMware Fusion安装CentOS网络设置"
categories:
  - Mac&Linux
---

在 vmware 中最小化安装 centos6.3 后发现无论 vmware 设置城共享还是桥接形式都无法连接网络，在网络上查询到 vmware workstation 下安装 centos 的设置方法，尝试后发现并不适用 mac os 下的 vmware fusion。
经过尝试，发现 fusion 下 centos 网络配置非常简单。方法如下：

1. 将 vmware 设置成桥接网络
2. 改变网卡设置

   $vi /etc/sysconfig/network-scripts/ifcfg-eth0

修改为如下值：

    BOOTPROTO="dhcp" //使用dhcp配置ip地址
    ONBOOT="yes" //使设备启动

3.重启网络服务

    $service network restart

4.查看网络

    $ifconfig

查看设备 eth0 是否分配到正确 ip，网络是否可以 ping 通。
