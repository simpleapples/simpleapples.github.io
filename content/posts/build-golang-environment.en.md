---
date: "2018-07-10T21:45:00+00:00"
title: "Installing Golang Environment and Dependency Management"
categories:
  - Golang
---

In 2015, Go 1.5 introduced an experimental vendor mechanism (which became enabled by default in Go 1.6 in 2016). The vendor mechanism involves adding a vendor folder to the project to store dependencies, allowing different projects to isolate their dependencies.
![](/images/20180710_02.png)

Golang is a statically typed, compiled, concurrent programming language with garbage collection. Golang provides convenient installation packages, supporting Windows, Linux, and Mac systems.

# Download and Install Package

The official Golang website is [https://golang.org/](https://golang.org/). If the official site is inaccessible, you can visit [https://golang.google.cn/](https://golang.google.cn/). On the website, clicking on Download Go will take you to the download page, where installation packages for various systems are available, along with source code for compiling and installation.

![](/images/20180710_03.png)

After downloading and running the installation package, execute the `go env` command in the terminal. If you see the following output, the installation was successful.

![](/images/20180710_04.png)

# GOROOT and GOPATH

Looking closely at the output above, you’ll notice both GOPATH and GOROOT. So, which one is the Golang runtime environment?

First, access the GOROOT path, and you'll find it contains folders like bin and lib. GOROOT is the Golang installation path, containing the Golang compiler, tools, standard library, etc., and it exists after installation.

Unlike GOROOT, GOPATH is the workspace path. Starting from Go 1.8, if GOPATH is not set, it defaults to $HOME/go on Unix and %USERPROFILE%/go on Windows. When you call `go build`, it looks for source code in GOPATH. Accessing the GOPATH path, you'll find only pkg, bin, and src folders, which are mostly empty. This is a conventional directory structure: the src folder is for source code, pkg stores compiled files, and bin holds compiled executables. Project code needs to be under the GOPATH/src path.

Besides storing project code, the GOPATH path also holds all dependencies installed via `go get`. Project code and dependency code are at the same level, and when each project has many dependencies, the amount of code in the GOPATH path can become overwhelming and difficult to manage.

# Vendor

When using `go run` or `go build`, dependencies are first searched for in the current path's vendor folder. If vendor doesn't exist, dependencies are then searched for in GOPATH.

However, when installing dependencies, we usually use `go get` or `go install`, which still install dependencies to the GOPATH path.

# Dependency Management Tool: dep

Vendor is merely a mechanism provided by Go, but it doesn't solve package management issues, nor does it manage dependency versions. To achieve these functionalities, a package management tool is needed.

Go provides a comparison of package management tools: [https://github.com/golang/go/wiki/PackageManagementTools](https://github.com/golang/go/wiki/PackageManagementTools)

dep is the official experimental package management tool, and it can be installed using the following script:

```bash
curl [https://raw.githubusercontent.com/golang/dep/master/install.sh](https://raw.githubusercontent.com/golang/dep/master/install.sh) | sh
```

After installation, navigate to the project path and execute:

```
dep init
```

This will create two files and a directory in the project:

```
Gopkg.toml
Gopkg.lock
vendor
```

The dep package management process is illustrated as follows:

![](/images/20180710_05.jpg)

- The solving function takes the imported packages in the current project and the rules in Gopkg.toml as input, producing an immutable dependency graph as output, forming Gopkg.lock.

- The vendor function uses the information in Gopkg.lock as input to ensure the project can be compiled using the versions locked in the Gopkg.lock file.

Use the following command to add dependencies:

```
dep ensure -add [github.com/gin-gonic/gin](http://github.com/gin-gonic/gin)
```

Use the following command to update Gopkg.lock:

```
dep ensure -update
```