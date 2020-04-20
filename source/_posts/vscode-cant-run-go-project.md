---
layout: post
title: 探究vscode debug流程，解决无法运行go程序的问题
date: 2020-04-20 15:35
comments: true
categories: Golang
---

### 问题描述

vscode 无法以 `run` 模式运行 go 项目（只能以 `debug` 模式调试），并且有如下报错。

![](/upload/20200420_01.png)

图中被遮盖的部分是项目内的 package，并非第三方 package，也就是说在以 `run` 模式运行 go 项目时无法找到其他的 go 文件，只能找到入口文件。

### 初步排查

找不到其他文件，首先想到的是 GO_PATH 的问题，但是项目使用了 go mod，允许在 GO_PATH 之外的路径创建项目，所以这个怀疑点排除。接下来怀疑 vscode 的配置有问题，每个 vscode 项目中都有 .launch.json 文件，配置运行代码时的环境，下面是项目中的 .launch.json。

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch",
            "type": "go",
            "request": "launch",
            "mode": "auto",
            "program": "${workspaceRoot}/src/main.go",
            "env": {},
            "args": []
        }
    ]
}
```

可以看到 .launch.json 里没有指定程序的工作目录，`debug` 模式和 `run` 模式会不会默认的工作路径不同呢？于是在 main 函数里使用 `os.Getwd()` 打印一下当前的路径，结果如下：

- `debug` 模式：项目所在目录
- `run` 模式：用户目录

基本可以确认，`run` 模式下的工作路径设置不正确，导致找不到路径。在 .launch.json 中加入 `cwd` 参数，手动填入项目路径。

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch",
            "type": "go",
            "request": "launch",
            "mode": "auto",
            "program": "${workspaceRoot}/src/main.go",
            "cwd": "${workspaceRoot}",
            "env": {},
            "args": []
        }
    ]
}
```

但是修改 .launch.json 后运行程序，输出的工作目录仍然是用户目录，`cwd` 参数并没有生效。

### 探究 vscode 的 debug 流程

至此，bug 的气息越来越浓厚，`cwd` 参数没有生效，肯定有问题！

一不做二不休，索性看看 vscode 的调试流程吧，用一个很暴力的方式，看看点击运行按钮后，vscode 到底是如何运行 go 程序的。

```go
package main
import "time"
func main() {
    time.Sleep(10000000000)
}
```

运行程序后，使用 `ps -ef|grep go` 查看进程。

![](/upload/20200420_02.jpg)

截图中三个进程从上到下均是父子关系，也就是说在 vscode 中即便使用 `run` 模式运行，也不是直接执行 `go run xxxx.go`，这与 Goland 等其他 IDE 的行为是不同的。vscode 首先调用了 language server 中的 node，执行了 go extention（vscode 的 go 扩展，安装后才支持 go 语言项目）中的一个 `goDebug.js`，而后 `goDebug.js` 中调用了 `go run xxxx.go`。（图中 /tmp  路径下的 main 文件是 go run 执行过程中生成的二进制文件）

接下来查看 `goDebug.js` 的逻辑，找到了调用 `go run` 的代码。

```js
this.debugProcess = spawn(getBinPathWithPreferredGopath('go', []), runArgs, { env });
```
查看代码上面几行的逻辑，根据参数的命名，可以猜测出来，.launch.json 中的配置在这里是可以获取到的。接下来直接修改 js 文件，进行调试，证实上述的猜测，由于我们无法直接看到 node goDebug.js 的输出，所以通过写入文件的方式进行调试。

```js
fs.writeFile('test.log', this.debugProcess.cwd(), function (err) {}
```

加入这句后再次运行，我们可以看到 test.log 文件中已经打印出了这个进程的工作路径，也就是 go run 的工作路径，是用户目录。至此，可以将问题缩小到：在 node 调用 go run 时没有将 .launch.json 文件中的 cwd 传给子进程（go run）。

`spawn` 是 nodejs 中的函数，看一下 spawn 的文档可以发现，spawn 有三个参数 `child_process.spawn(command[, args][, options])` 第三个参数 options 中可以指定 cwd 工作路径。而 `goDebug.js` 这段启动子进程的代码并没有设置 cwd，只设置了`env` 参数，这就是 `run` 模式无法运行 go 程序的原因。

![](/upload/20200420_03.jpg)

### 解决方案

在发现这个问题时，vscode go extention的最新版本是0.13，这个问题暂时只能通过修改 goDebug.js 的源码解决，如下图所示加入注释中的代码，将 `cwd` 参数传入子进程，就可以解决问题。

![](/upload/20200420_04.png)

同时，这个 bug 已经被解决，可以参考 [ISSUE #3096](https://github.com/microsoft/vscode-go/issues/3096)，程序员在解决另一个问题这个 ISSUE 的问题时，“顺手”把 `cwd`  的问题修复了。在 vscode go extention 0.14版发布后（已发布），将 go extension 更新到最新版就可以正常运行和调试 go 项目了。


### 参考资料
[Debugging in Visual Studio Code](https://code.visualstudio.com/docs/editor/debugging)

[Node.js v13.13.0 Documentation](
https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options)

[Debug: add "go run ." support #3096](https://github.com/microsoft/vscode-go/issues/3096)
