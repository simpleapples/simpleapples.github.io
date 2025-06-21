---
date: "2018-07-15T00:00:00+00:00"
title: "Troubleshooting DNS Resolution Issues When Setting Up a Kubernetes Cluster"
categories:
  - DevOps
---

![](/images/20180715_01.jpg)

# Problem Description

While setting up a Kubernetes cluster and installing the kube-dns plugin, I ran an Ubuntu container and found that it couldn't resolve domain names outside the cluster. Initially, it could resolve domain names within the cluster, but after some time, it couldn't even resolve those.

```bash
$ nslookup kubernetes.default
Server:    10.99.0.2
Address 1: 10.99.0.2 kube-dns.kube-system.svc.cluster.local

nslookup: can't resolve 'kubernetes.default'
```

# Troubleshooting Process

Before troubleshooting, let's consider the DNS resolution process in a Kubernetes cluster. In a cluster with kube-dns installed, the dnsPolicy attribute of a regular Pod is set to the default value ClusterFirst, meaning it points to the internal DNS server of the cluster. Kube-dns is responsible for resolving internal domain names, and the dnsPolicy value of the kube-dns Pod is Default, meaning it inherits the DNS server from the Node it resides on. For unresolved external domain names, kube-dns queries the external DNS server, as illustrated in the diagram.

![](/images/20180715_02.jpg)

The Ubuntu container is a regular Pod, and in a Linux system, /etc/resolv.conf is the file that stores DNS server information. The /etc/resolv.conf file of a regular Pod should store the Service IP of kube-dns.

```bash
nameserver 10.99.0.2  # This stores the Service IP of kube-dns
search default.svc.cluster.local. svc.cluster.local. cluster.local.
options ndots:5
```

Upon checking, I found that the /etc/resolv.conf file indeed stored the Service IP of kube-dns, indicating no issue there. Next, I checked the kube-dns Pod by inspecting its /etc/resolv.conf file, which should store the DNS server address for external queries. I discovered it stored the address 127.0.0.53. Further inspection of the kube-dns Pod logs revealed numerous i/o timeout errors.

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

The root cause of the problem is now apparent: kube-dns can only resolve internal cluster addresses, while external addresses should be sent to an external DNS server. Since the /etc/resolv.conf file in the kube-dns Pod stores the DNS server address as 127.0.0.53, which is a loopback address, DNS resolution requests for external domains are sent back to kube-dns, creating a loop. This results in dozens of i/o timeout logs per second, as requests keep circulating within kube-dns, which acts like a black hole, consuming all DNS resolution requests. The accumulation of these requests eventually causes network lag across the entire cluster.

![](/images/20180715_03.jpg)

# Why

Although the cause of the problem is identified, why does the /etc/resolv.conf file in the kube-dns Pod store the DNS server as 127.0.0.53?

The dnsPolicy value of the kube-dns Pod is Default. Referring to the Kubernetes documentation:

> "`Default`": The Pod inherits the name resolution configuration from the node that the pods run on. See [related discussion](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/#inheriting-dns-from-the-node) for more details.

Thus, the /etc/resolv.conf file of kube-dns is inherited from the Node. Checking the Node's /etc/resolv.conf file, it indeed stores the DNS server address as 127.0.0.53. The next question arises: why doesn't this create a loopback issue when sending DNS resolution requests from the Node?

The Node runs Ubuntu 18.04 Server. In this version, DNS resolution requests are not directly sent to the network's DNS server. Ubuntu 18.04 includes a systemd-resolved service that provides DNS resolution services for local applications. For example, when running nslookup localhost, the resolver finds the DNS server 127.0.0.53 from /etc/resolv.conf and sends the request. The systemd-resolved service listens on port 53 and captures the request. If it can resolve it, like localhost, it returns 127.0.0.1. If not, it forwards the request to an external server, whose address is stored in /run/systemd/resolve/resolv.conf, the configuration file for systemd-resolved, as illustrated in the diagram.

![](/images/20180715_04.jpg)

# Solution

Understanding the problem's ins and outs, the solution emerges. In a Kubernetes cluster, kubelet is a worker component responsible for managing Pods. According to Kubernetes documentation, kubelet by default reads the DNS server address from the Node's /etc/resolv.conf file, allowing Pods with a dnsPolicy of Default to inherit it. The --resolv-conf parameter in kubelet can specify the address of this configuration file. In Ubuntu 18.04, setting this parameter to the DNS server configuration file of systemd-resolved, /run/systemd/resolve/resolv.conf, allows Pods to inherit the actual external DNS server.

# Summary

Through exploring the problem, I also understood the complete DNS resolution process in a Kubernetes cluster, as illustrated in the diagram.

![](/images/20180715_05.jpg)

_\* In Ubuntu 16.04, a similar logic applies, except systemd-resolved is replaced by dnsmasq, which listens on 127.0.1.1._
_\* During practical implementation, I also explored the architectural and logical differences between CoreDNS and KubeDNS, but that's beyond the scope of this discussion. Interested readers can explore further on their own._
_\* If the Kubernetes cluster is installed on a virtual machine under a NAT network, the /etc/resolv.conf file in the virtual machine (i.e., the Node in the Kubernetes cluster) might be modified to the NAT address, avoiding the above issue._

# References

[https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
[https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
[https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/)
[https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html)
[https://github.com/kubernetes/kubernetes/issues/49411](https://github.com/kubernetes/kubernetes/issues/49411)
[https://github.com/kubernetes/kubernetes/issues/45828](https://github.com/kubernetes/kubernetes/issues/45828)