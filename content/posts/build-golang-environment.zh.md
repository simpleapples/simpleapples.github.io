---
date: "2018-07-10T21:45:00+00:00"
title: "Golang环境安装和依赖管理"
categories:
  - Golang
---

2015 年，Go 1.5 加入了一个试验性的 vendor 机制（到 2016 年的 Go 1.6 版变为默认开启），vendor 机制就是在项目中加入了 vendor 文件夹，用于存放依赖，这样就可以将不同项目的依赖隔离开。
![](/images/20180710_02.png)

Golang 一种静态强类型、编译型、并发型，并具有垃圾回收功能的编程语言。Golang 提供了方便的安装包，支持 Windows、Linux、Mac 系统。

# 下载安装包

Golang 的官网是[https://golang.org/](https://golang.org/)，如果官网打不开，可以访问[https://golang.google.cn/](https://golang.google.cn/)这个域名。在官网点击 Download Go 会进入下载页，可以看到这里提供了针对各个系统的安装包，也提供了源码，可以下载源码编译安装。

![](/images/20180710_03.png)

下载运行安装包后，在 terminal 中执行 go env 命令，如果出现下面的输出说明已经安装成功。

![](/images/20180710_04.png)

# GOROOT 与 GOPATH

仔细看上面的输出，会发现其中有一个 GOPATH，又有一个 GOROOT，那么到底哪个才是 Golang 的运行环境呢。

首先访问一下 GOROOT 这个路径，会发现其中包含 bin、lib 等文件夹。GOROOT 就是 Golang 的安装路径，其中包含 Golang 编译、工具、标准库等，在安装后就会存在。

和 GOROOT 不同，GOPATH 是工作空间路径，从 go 1.8 开始，如果 GOPATH 没有被设置，会有一个默认值，在 Unix 上为$HOME/go，在 Windows 上为%USERPROFILE%/go，当调用 go build 时，它会在 GOPATH 中寻找源码。访问一下 GOPATH 这个路径，会发现其中只有 pkg、bin、src 三个文件夹，并且里面基本是空的，这是一个约定的目录结构，src 文件夹用来存放源码、pkg 存放编译后生成的文件，bin 存放编译后生成的可执行文件。项目代码需要在 GOPATH/src 路径下。

GOPATH 路径下出了存放项目代码，还存放所有通过 go get 安装的依赖，项目代码和依赖代码是平级的，当各个项目都有很多依赖的时候，这个 GOPATH 路径下的代码量会多的吓人，并且难以拆分。

# Vendor

当使用 go run 或者 go build 命令时，会首先从当前路径下的 vendor 文件夹中查找依赖，如果 vendor 不存在，才会从 GOPATH 中查找依赖。

然而我们安装依赖通常使用 go get 或者 go install 命令，这两个命令依旧会把依赖安装到 GOPATH 路径下。

# 包管理工具 dep

Vendor 只是 go 官方提供的一个机制，但是包管理的问题依然没有解决，并且也没有对依赖进行版本管理。如果要实现上述的功能，还需要借助包管理工具。

Go 官方给出了包管理工具的对比：[https://github.com/golang/go/wiki/PackageManagementTools](https://github.com/golang/go/wiki/PackageManagementTools)

dep 是官方的试验性包管理工具，可以通过如下脚本安装

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

dep 包管理的流程如图

![](/images/20180710_05.jpg)

- solving 功能，它将当前项目中的导入包和 Gopkg.toml 中的规则作为输入，不可变的依赖关系图作为传递完成后的输出，形成 Gopkg.lock。

- vendor 功能，将 Gopkg.lock 中的信息作为输入，确保项目编译时能使用在 Gopkg.lock 文件中锁定的版本。

使用如下命令添加依赖

```
dep ensure -add [github.com/gin-gonic/gin](http://github.com/gin-gonic/gin)
```

使用如下命令更新 Gopkg.lock

```
dep ensure -update
```
