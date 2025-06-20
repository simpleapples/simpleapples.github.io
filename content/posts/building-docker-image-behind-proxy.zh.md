---
date: "2019-04-18T10:55:00+00:00"
title: "使用代理进行 docker build 问题的解决思路"
categories:
  - DevOps
---

### 问题描述

在使用 docker build 打包镜像时，遇到了需要使用代理访问网络的需求。使用如下的 Dockerfile 来模拟这个场景：

```dockerfile
FROM golang:1.12
RUN curl www.google.com --max-time 3
```

国内一般网络环境下，curl www.google.com 是无法正常返回的，加入 --max-time 让 curl 的耗时不要太长。

<!-- more -->

### 配置 http_proxy 变量

首先需要在环境变量中设置 http_proxy 和 https_proxy，使得访问网络的命令（这里使用 curl 来代表）能够通过环境变量中配置的代理服务器访问 www.google.com。

docker build 命令虽然是在 docker 所在的宿主机上执行的，看上去像是直接使用了宿主机的网络环境，但实际上 docker build 也是启动了一个 container 进行构建，所以在构建过程中的所有命令都是在 container 中执行的，http_proxy 和 https_proxy 的配置也应该是在 container 中进行的。可以使用 ENV 来配置 container 中的环境变量。

代理服务器启动在宿主机的 1087 端口上，修改 dockerfile 文件：

```dockerfile
FROM golang:1.12

ENV http_proxy "http://127.0.0.1:1087"
ENV HTTP_PROXY "http://127.0.0.1:1087"
ENV https_proxy "http://127.0.0.1:1087"
ENV HTTPS_PROXY "http://127.0.0.1:1087"

RUN curl www.google.com --max-time 3
```

重新执行 docker build 会发现 curl 依旧无法访问 www.google.com，从报错信息上可以看到 127.0.0.1 上的 1087 端口上并没有服务。

### 访问宿主机

由于 container 默认是桥接网络，宿主机和 container 是平级的，被放在了一个虚拟的网段里。访问宿主机上的代理服务器，对于 container 来说实际上是访问另一台机器上的服务器，127.0.0.1 指向的是 container 本身。在 docker 默认的桥接网络中，宿主机的 IP 一般是 172.17.0.1（Linux），或者 192.168.65.1（MacOS），可以将 http_proxy 中的 IP 换成 172.17.0.1/192.168.65.1，来实现通过宿主的代理服务器访问网络，修改 dockerfile：

```dockerfile
FROM golang:1.12

ENV http_proxy "http://172.17.0.1:1087"
ENV HTTP_PROXY "http://172.17.0.1:1087"
ENV https_proxy "http://172.17.0.1:1087"
ENV HTTPS_PROXY "http://172.17.0.1:1087"

RUN curl www.google.com --max-time 3
```

虽然使用这种方式可以达到目的，但是如果编译环境变了或者代理服务器的配置变了，哪怕只是操作系统从 Linux 变成了 MacOS，都得修改 dockerfile，显然不够解耦，也不方便。

### 配置网络模式

docker 中还有一种 host 网络模式，就是让 container 使用宿主机的网络，相当于 container 在网络层面和宿主机不做隔离，使用这种网络模式执行 docker build，就不需要在 dockerfile 中添加 http_proxy 环境变量，container 可以直接读取宿主上的环境变量。

首先在宿主上导入 http_proxy 环境变量：

```bash
export http_proxy="http://127.0.0.1:1087"
export HTTP_PROXY="http://127.0.0.1:1087"
export https_proxy="http://127.0.0.1:1087"
export HTTPS_PROXY="http://127.0.0.1:1087"
```

接下来将 dockerfile 简化：

```dockerfile
FROM golang:1.12
RUN curl www.google.com --max-time 3
```

重新执行 docker build，加上参数 --network host，使用宿主网络：

```bash
docker build --network host .
```

执行后 curl 就可以像在宿主上直接执行一样，通过代理访问 www.google.com 了。
