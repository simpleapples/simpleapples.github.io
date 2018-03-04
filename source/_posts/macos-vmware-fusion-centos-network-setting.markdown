---
layout: post
title: "MacOS+VMware Fusion安装CentOS网络设置"
date: 2012-10-19 12:39
comments: true
categories: Mac&Linux
---

在vmware中最小化安装centos6.3后发现无论vmware设置城共享还是桥接形式都无法连接网络，在网络上查询到vmware workstation下安装centos的设置方法，尝试后发现并不适用mac os下的vmware fusion。
经过尝试，发现fusion下centos网络配置非常简单。方法如下：

1. 将vmware设置成桥接网络
2. 改变网卡设置

	$vi /etc/sysconfig/network-scripts/ifcfg-eth0

修改为如下值：

	BOOTPROTO="dhcp" //使用dhcp配置ip地址  
	ONBOOT="yes" //使设备启动  

3.重启网络服务

	$service network restart

4.查看网络

	$ifconfig

查看设备eth0是否分配到正确ip，网络是否可以ping通。