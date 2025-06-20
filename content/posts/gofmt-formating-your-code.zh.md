---
date: "2018-07-17T14:13:00+00:00"
title: "使用gofmt格式化代码"
categories:
  - Golang
---

![](/images/20180717_01.png)

对于一门编程语言来说，代码格式化是最容易引起争议的一个问题，不同的开发者可能会有不同的编码风格和习惯，但是如果所有开发者都能使用同一种格式来编写代码，开发者就可以将宝贵的时间专注在语言要解决的问题上。

# gofmt 介绍

Golang 的开发团队制定了统一的官方代码风格，并且推出了 gofmt 工具（gofmt 或 go fmt）来帮助开发者格式化他们的代码到统一的风格。gofmt 是一个 cli 程序，会优先读取标准输入，如果传入了文件路径的话，会格式化这个文件，如果传入一个目录，会格式化目录中所有.go 文件，如果不传参数，会格式化当前目录下的所有.go 文件。

gofmt 默认不对代码进行简化，使用-s 参数可以开启简化代码功能，具体来说会进行如下的转换：

- 去除数组、切片、Map 初始化时不必要的类型声明：

```go
如下形式的切片表达式：
    []T{T{}, T{}}
将被简化为：
    []T{{}, {}}
```

- 去除数组切片操作时不必要的索引指定

```go
如下形式的切片表达式：
    s[a:len(s)]
将被简化为：
    s[a:]
```

- 去除迭代时非必要的变量赋值

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

gofmt 命令参数列表如下：

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

可以看到，gofmt 命令还支持自定义的重写规则，使用-r 参数，按照 pattern -> replacement 的格式传入规则。

有如下内容的 Golang 程序，存储在 main.go 文件中。

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

**\*注意：Gofmt 使用 tab 来表示缩进，并且对行宽度无限制，如果手动对代码进行了换行，gofmt 也不会强制把代码格式化回一行。**

# go fmt 和 gofmt

gofmt 是一个独立的 cli 程序，而 go 中还有一个 go fmt 命令，go fmt 命令是 gofmt 的简单封装。

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

go fmt 命令本身只有两个可选参数-n 和-x，-n 仅打印出内部要执行的 go fmt 的命令，-x 命令既打印出 go fmt 命令又执行它，如果需要更细化的配置，需要直接执行 gofmt 命令。

go fmt 在调用 gofmt 时添加了-l -w 参数，相当于执行了`gofmt -l -w`。

# goland 中配置 gofmt

Goland 是 JetBrains 公司推出的 Go 语言 IDE，是一款功能强大，使用便捷的产品。

在 Goland 中，可以通过添加一个 File Watcher 来在文件发生变化的时候调用 gofmt 进行代码格式化，具体方法是，点击 Preferences -> Tools -> File Watchers，点加号添加一个 go fmt 模版，Goland 中预置的 go fmt 模版使用的是 go fmt 命令，将其替换为 gofmt，然后在参数中增加-l -w -s 参数，启用代码简化功能。添加配置后，保存源码时，goland 就会执行代码格式化了。

![](/images/20180717_02.png)

# 参考文章

[https://golang.org/cmd/gofmt/](https://golang.org/cmd/gofmt/)

[https://golang.org/doc/effective_go.html](https://golang.org/doc/effective_go.html)

[https://openhome.cc/Gossip/Go/gofmt.html](https://openhome.cc/Gossip/Go/gofmt.html)

[https://github.com/hyper0x/go_command_tutorial/blob/master/0.9.md](https://github.com/hyper0x/go_command_tutorial/blob/master/0.9.md)
