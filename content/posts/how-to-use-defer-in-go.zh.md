---
date: "2018-09-14T13:31:00+00:00"
title: "Go语言中defer的一些坑"
categories:
  - Golang
---

![](/images/20180914_01.png)

defer 语句是 Go 中一个非常有用的特性，可以将一个方法延迟到包裹该方法的方法返回时执行，在实际应用中，defer 语句可以充当其他语言中 try…catch…的角色，也可以用来处理关闭文件句柄等收尾操作。

### defer 触发时机

> A "defer" statement invokes a function whose execution is deferred to the moment the surrounding function returns, either because the surrounding function executed a return statement, reached the end of its function body, or because the corresponding goroutine is panicking.

Go 官方文档中对 defer 的执行时机做了阐述，分别是。

- 包裹 defer 的函数返回时
- 包裹 defer 的函数执行到末尾时
- 所在的 goroutine 发生 panic 时

### defer 执行顺序

当一个方法中有多个 defer 时， defer 会将要延迟执行的方法“压栈”，当 defer 被触发时，将所有“压栈”的方法“出栈”并执行。所以 defer 的执行顺序是 LIFO 的。

所以下面这段代码的输出不是 1 2 3，而是 3 2 1。

```go
func stackingDefers() {
    defer func() {
        fmt.Println("1")
    }()
    defer func() {
        fmt.Println("2")
    }()
    defer func() {
        fmt.Println("3")
    }()
}
```

### 坑 1：defer 在匿名返回值和命名返回值函数中的不同表现

先看下面两个方法执行的结果。

```go
func returnValues() int {
    var result int
    defer func() {
        result++
        fmt.Println("defer")
    }()
    return result
}

func namedReturnValues() (result int) {
    defer func() {
        result++
        fmt.Println("defer")
    }()
    return result
}
```

上面的方法会输出 0，下面的方法输出 1。上面的方法使用了匿名返回值，下面的使用了命名返回值，除此之外其他的逻辑均相同，为什么输出的结果会有区别呢？

要搞清这个问题首先需要了解 defer 的执行逻辑，文档中说 defer 语句在方法返回“时”触发，也就是说 return 和 defer 是“同时”执行的。以匿名返回值方法举例，过程如下。

- 将 result 赋值给返回值（可以理解成 Go 自动创建了一个返回值 retValue，相当于执行 retValue = result）
- 然后检查是否有 defer，如果有则执行
- 返回刚才创建的返回值（retValue）

在这种情况下，defer 中的修改是对 result 执行的，而不是 retValue，所以 defer 返回的依然是 retValue。在命名返回值方法中，由于返回值在方法定义时已经被定义，所以没有创建 retValue 的过程，result 就是 retValue，defer 对于 result 的修改也会被直接返回。

### 坑 2：在 for 循环中使用 defer 可能导致的性能问题

看下面的代码

```go
func deferInLoops() {
    for i := 0; i < 100; i++ {
        f, _ := os.Open("/etc/hosts")
        defer f.Close()
    }
}
```

defer 在紧邻创建资源的语句后生命力，看上去逻辑没有什么问题。但是和直接调用相比，defer 的执行存在着额外的开销，例如 defer 会对其后需要的参数进行内存拷贝，还需要对 defer 结构进行压栈出栈操作。所以在循环中定义 defer 可能导致大量的资源开销，在本例中，可以将 f.Close()语句前的 defer 去掉，来减少大量 defer 导致的额外资源消耗。

### 坑 3：判断执行没有 err 之后，再 defer 释放资源

一些获取资源的操作可能会返回 err 参数，我们可以选择忽略返回的 err 参数，但是如果要使用 defer 进行延迟释放的的话，需要在使用 defer 之前先判断是否存在 err，如果资源没有获取成功，即没有必要也不应该再对资源执行释放操作。如果不判断获取资源是否成功就执行释放操作的话，还有可能导致释放方法执行错误。

正确写法如下。

```go
resp, err := http.Get(url)
// 先判断操作是否成功
if err != nil {
    return err
}
// 如果操作成功，再进行Close操作
defer resp.Body.Close()
```

### 坑 4：调用 os.Exit 时 defer 不会被执行

当发生 panic 时，所在 goroutine 的所有 defer 会被执行，但是当调用 os.Exit()方法退出程序时，defer 并不会被执行。

```go
func deferExit() {
    defer func() {
        fmt.Println("defer")
    }()
    os.Exit(0)
}
```

上面的 defer 并不会输出。
