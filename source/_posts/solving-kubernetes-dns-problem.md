---
layout: post
title: 搭建Kubernetes集群时DNS无法解析问题的处理过程
date: 2018-07-15 00:00
comments: true
categories: DevOps
---

![](/upload/20180715_01.jpg)

# 问题描述

在搭建Kubernetes集群过程中，安装了kube-dns插件后，运行一个ubuntu容器，发现容器内无法解析集群外域名，一开始可以解析集群内域名，一段时间后也无法解析集群内域名。

```bash
$ nslookup kubernetes.default
Server:    10.99.0.2
Address 1: 10.99.0.2 kube-dns.kube-system.svc.cluster.local

nslookup: can't resolve 'kubernetes.default'
```

# 排查过程

在排查问题前，先思考一下Kubernetes集群中的DNS解析过程，在安装好kube-dns的集群中，普通Pod的dnsPolicy属性是默认值ClusterFirst，也就是会指向集群内部的DNS服务器，kube-dns负责解析集群内部的域名，kube-dns Pod的dnsPolicy值是Default，意思是从所在Node继承DNS服务器，对于无法解析的外部域名，kube-dns会继续向集群外部的dns进行查询，过程如图。

![](/upload/20180715_02.jpg)

Ubuntu容器是一个普通的Pod，在Linux系统中，/etc/resolv.conf是存储DNS服务器的文件，普通Pod的/etc/resolv.conf文件应该存储的是kube-dns的Service IP。

```bash
nameserver 10.99.0.2  # 这里存储的是kube-dns的Service IP
search default.svc.cluster.local. svc.cluster.local. cluster.local.
options ndots:5
```

查看后发现/etc/resolv.conf文件中存储的是kube-dns的Service IP，证明这一步没有问题，接下来查看一下kube-dns的Pod，先进入kube-dns的Pod中检查一下/etc/resolv.conf文件，这里存储的应该是集群外部的DNS服务器地址，查看后发现，这里存储的地址是127.0.0.53，进一步查看kube-dns Pod的log，发现出现了非常多的i/o timeout错误。

```bash
 2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:38019->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:57567->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:52599->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:42539->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:46885->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:44189->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:56505->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:47320->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:42464->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:49203->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:58103->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:47148->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:36883->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:40968->127.0.0.53:53: i/o timeout
2018/07/11 07:12:47 [ERROR] 2 [www.baidu.com](http://www.baidu.com/). A: unreachable backend: read udp 127.0.0.1:55672->127.0.0.53:53: i/o timeout
```

现在基本上可以发现问题的原因了，kube-dns只能解析集群内部地址，而集群外部地址应该发给外部DNS服务器进行解析，由于kube-dns Pod中的/etc/resolv.conf文件存储的DNS服务器地址是127.0.0.53，127.*.*.*都是回环地址，也就是集群外域名的DNS解析请求会再次发送回kube-dns，导致形成一个循环，这也是一秒钟会出现几十次i/o timeout日志的原因，请求会不断的在kube-dns中循环，kube-dns就像一个黑洞一样，吃掉了所有dns解析请求，不断累积的请求最终会导致整个集群的网络出现卡顿。

![](/upload/20180715_03.jpg)

# 为什么

虽然问题的原因找到了，但是为什么kube-dns Pod中/etc/resolv.conf文件存储的DNS服务器是127.0.0.53？

kube-dns Pod的dnsPolicy值是Default，查看一下Kubernetes文档。

> "`Default`": The Pod inherits the name resolution configuration from the node that the pods run on. See [related discussion](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/#inheriting-dns-from-the-node) for more details.

所以kube-dns的/etc/resolv.conf文件是从Node中继承来的，查看Node中的/etc/resolv.conf文件，存储的DNS服务器地址确实是127.0.0.53，那么下一个问题出现了，在Node中发送DNS解析请求为什么不会产生回环的问题呢？

Node使用的是Ubuntu 18.04 Server，在这个版本的系统中，DNS解析请求并不是直接发给所在网络的DNS服务器的，Ubuntu 18.04中有一个systemd-resolved服务，为本地应用程序提供了DNS解析服务，例如nslookup localhost，解析程序从/etc/resolv.conf文件中找到DNS服务器127.0.0.53，发送解析请求，systemd-resolved会监听在53端口上，捕获到解析请求后，如果是自己可以解析的，例如localhost，会直接返回127.0.0.1，如果不能解析，才会发送给外部服务器，而外部服务器的地址存储在/run/systemd/resolve/resolv.conf文件中，这个文件是systemd-resolved服务器的配置文件，过程如图。

![](/upload/20180715_04.jpg)

# 怎么破

理解了问题的来龙去脉，解决问题的办法也就应运而生。在Kubernetes集群中，kubelet是worker组建，负责管理Pod，根据kubernetes文档，kubelet默认会从Node的/etc/resolv.conf文件读取DNS服务器地址，使得dnsPolicy是Default的Pod得以继承，kubelet中的--resolv-conf参数可以指定这个配置文件的地址。在Ubuntu 18.04中，将这个参数设置为systemd-resolved的DNS服务器配置文件/run/systemd/resolve/resolv.conf，Pod就会继承真正的外部DNS服务器。

# 总结

通过对问题的探究，也理解了Kubernetes集群中DNS解析的完整过程，如图。

![](/upload/20180715_05.jpg)

*\* 在Ubuntu 16.04中也是类似的逻辑，只不过systemd-resolved换成了dnsmasq，监听地址是127.0.1.1*
*\* 在具体实践过程中，也顺便探究了CoreDNS和KubeDNS架构和解析逻辑上的区别，不过不在此问题的讨论范围，有兴趣的朋友可以自己看一下。*
*\* 如果Kubernetes集群是安装在NAT网络下的虚拟机上，虚拟机（也就是Kubernetes集群中的Node）中/etc/resolv.conf文件可能被修改为NAT的地址，也就不会出现上面这个问题。*

# 参考内容

 [https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
[https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
[https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)
[https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html)
[https://github.com/kubernetes/kubernetes/issues/49411](https://github.com/kubernetes/kubernetes/issues/49411)
[https://github.com/kubernetes/kubernetes/issues/45828](https://github.com/kubernetes/kubernetes/issues/45828)
