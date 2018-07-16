---
layout: post
title: Golang环境安装和依赖管理
date: 2018-07-10 21:45
comments: true
categories: Golang
---

![](/upload/20180710_02.png)


Golang一种静态强类型、编译型、并发型，并具有垃圾回收功能的编程语言。Golang提供了方便的安装包，支持Windows、Linux、Mac系统。

# 下载安装包

Golang的官网是[https://golang.org/](https://golang.org/)，如果官网打不开，可以访问[https://golang.google.cn/](https://golang.google.cn/)这个域名。在官网点击Download Go会进入下载页，可以看到这里提供了针对各个系统的安装包，也提供了源码，可以下载源码编译安装。

![](/upload/20180710_03.png)

下载运行安装包后，在terminal中执行go env命令，如果出现下面的输出说明已经安装成功。

![](/upload/20180710_04.png)

# GOROOT与GOPATH

仔细看上面的输出，会发现其中有一个GOPATH，又有一个GOROOT，那么到底哪个才是Golang的运行环境呢。

首先访问一下GOROOT这个路径，会发现其中包含bin、lib等文件夹。GOROOT就是Golang的安装路径，其中包含Golang编译、工具、标准库等，在安装后就会存在。

和GOROOT不同，GOPATH是工作空间路径，从go 1.8开始，如果GOPATH没有被设置，会有一个默认值，在Unix上为$HOME/go，在Windows上为%USERPROFILE%/go，当调用go build时，它会在GOPATH中寻找源码。访问一下GOPATH这个路径，会发现其中只有pkg、bin、src三个文件夹，并且里面基本是空的，这是一个约定的目录结构，src文件夹用来存放源码、pkg存放编译后生成的文件，bin存放编译后生成的可执行文件。项目代码需要在GOPATH/src路径下。

GOPATH路径下出了存放项目代码，还存放所有通过go get安装的依赖，项目代码和依赖代码是平级的，当各个项目都有很多依赖的时候，这个GOPATH路径下的代码量会多的吓人，并且难以拆分。

# Vendor

2015年，Go 1.5加入了一个试验性的vendor机制（到2016年的Go 1.6版变为默认开启），vendor机制就是在项目中加入了vendor文件夹，用于存放依赖，这样就可以将不同项目的依赖隔离开。

当使用go run或者go build命令时，会首先从当前路径下的vendor文件夹中查找依赖，如果vendor不存在，才会从GOPATH中查找依赖。

然而我们安装依赖通常使用go get或者go install命令，这两个命令依旧会把依赖安装到GOPATH路径下。

# 包管理工具dep

Vendor只是go官方提供的一个机制，但是包管理的问题依然没有解决，并且也没有对依赖进行版本管理。如果要实现上述的功能，还需要借助包管理工具。

Go官方给出了包管理工具的对比：[https://github.com/golang/go/wiki/PackageManagementTools](https://github.com/golang/go/wiki/PackageManagementTools)

dep是官方的试验性包管理工具，可以通过如下脚本安装

curl [https://raw.githubusercontent.com/golang/dep/master/install.sh](https://raw.githubusercontent.com/golang/dep/master/install.sh) | sh

安装完成后，进入项目路径，执行

```
dep init
```

项目中会出现两个文件一个目录

```
Gopkg.toml
Gopkg.lock
vendor
```

dep包管理的流程如图

![](/upload/20180710_05.jpg)

- solving功能，它将当前项目中的导入包和Gopkg.toml中的规则作为输入，不可变的依赖关系图作为传递完成后的输出，形成Gopkg.lock。

- vendor功能，将Gopkg.lock中的信息作为输入，确保项目编译时能使用在Gopkg.lock文件中锁定的版本。

使用如下命令添加依赖

```
dep ensure -add [github.com/gin-gonic/gin](http://github.com/gin-gonic/gin)
```

使用如下命令更新Gopkg.lock

```
dep ensure -update
```

**欢迎关注知乎专栏【Golang私房菜】**