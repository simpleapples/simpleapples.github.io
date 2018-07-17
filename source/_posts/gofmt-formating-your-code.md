---
layout: post
title: 使用gofmt格式化代码
date: 2018-07-17 14:13
comments: true
categories: Golang
---

![](/upload/20180717_01.png)

对于一门编程语言来说，代码格式化是最容易引起争议的一个问题，不同的开发者可能会有不同的编码风格和习惯，但是如果所有开发者都能使用同一种格式来编写代码，开发者就可以将宝贵的时间专注在语言要解决的问题上。

# gofmt介绍

Golang的开发团队制定了统一的官方代码风格，并且推出了gofmt工具（gofmt或go fmt）来帮助开发者格式化他们的代码到统一的风格。gofmt是一个cli程序，会优先读取标准输入，如果传入了文件路径的话，会格式化这个文件，如果传入一个目录，会格式化目录中所有.go文件，如果不传参数，会格式化当前目录下的所有.go文件。

gofmt默认不对代码进行简化，使用-s参数可以开启简化代码功能，具体来说会进行如下的转换：

*   去除数组、切片、Map初始化时不必要的类型声明：

```go
如下形式的切片表达式：
    []T{T{}, T{}}
将被简化为：
    []T{{}, {}}
```

*   去除数组切片操作时不必要的索引指定

```go
如下形式的切片表达式：
    s[a:len(s)]
将被简化为：
    s[a:]
```

*   去除迭代时非必要的变量赋值

```go
如下形式的迭代：
    for x, _ = range v {...}
将被简化为：
    for x = range v {...}
如下形式的迭代：
    for _ = range v {...}
将被简化为：
    for range v {...}
```

gofmt命令参数列表如下：

```bash
usage: gofmt [flags] [path ...]
  -cpuprofile string
        write cpu profile to this file
  -d    display diffs instead of rewriting files
  -e    report all errors (not just the first 10 on different lines)
  -l    list files whose formatting differs from gofmt's
  -r string
        rewrite rule (e.g., 'a[b:len(a)] -> a[b:]')
  -s    simplify code
  -w    write result to (source) file instead of stdout
```

可以看到，gofmt命令还支持自定义的重写规则，使用-r参数，按照pattern -> replacement的格式传入规则。

有如下内容的Golang程序，存储在main.go文件中。

```go
package main

import "fmt"

func main() {
   a := 1
   b := 2
   c := a + b
   fmt.Println(c)
}
```

用以下规则来格式化上面的代码。

```bash
gofmt -r "a + b -> b + a"
```

格式化的结果如下。

```go
package main

import "fmt"

func main() {
   a := 1
   b := 2
   c := b + a
   fmt.Println(c)
}
```

**\*注意：Gofmt使用tab来表示缩进，并且对行宽度无限制，如果手动对代码进行了换行，gofmt也不会强制把代码格式化回一行。**

# go fmt和gofmt

gofmt是一个独立的cli程序，而go中还有一个go fmt命令，go fmt命令是gofmt的简单封装。

```bash
usage: go fmt [-n] [-x] [packages]

Fmt runs the command 'gofmt -l -w' on the packages named
by the import paths. It prints the names of the files that are modified.
For more about gofmt, see 'go doc cmd/gofmt'.
For more about specifying packages, see 'go help packages'.
The -n flag prints commands that would be executed.
The -x flag prints commands as they are executed.
To run gofmt with specific options, run gofmt itself.

See also: go fix, go vet.
```

go fmt命令本身只有两个可选参数-n和-x，-n仅打印出内部要执行的go fmt的命令，-x命令既打印出go fmt命令又执行它，如果需要更细化的配置，需要直接执行gofmt命令。

go fmt在调用gofmt时添加了-l -w参数，相当于执行了`gofmt -l -w`。

# goland中配置gofmt

Goland是JetBrains公司推出的Go语言IDE，是一款功能强大，使用便捷的产品。

在Goland中，可以通过添加一个File Watcher来在文件发生变化的时候调用gofmt进行代码格式化，具体方法是，点击Preferences -> Tools -> File Watchers，点加号添加一个go fmt模版，Goland中预置的go fmt模版使用的是go fmt命令，将其替换为gofmt，然后在参数中增加-l -w -s参数，启用代码简化功能。添加配置后，保存源码时，goland就会执行代码格式化了。

![](/upload/20180717_02.png)

# 参考文章

[https://golang.org/cmd/gofmt/](https://golang.org/cmd/gofmt/)

[https://golang.org/doc/effective_go.html](https://golang.org/doc/effective_go.html)

[https://openhome.cc/Gossip/Go/gofmt.html](https://openhome.cc/Gossip/Go/gofmt.html)

[https://github.com/hyper0x/go_command_tutorial/blob/master/0.9.md](https://github.com/hyper0x/go_command_tutorial/blob/master/0.9.md)

# 点击关注知乎专栏[Golang私房菜](https://zhuanlan.zhihu.com/golang-fans)
