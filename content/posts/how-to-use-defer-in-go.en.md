---
date: "2018-09-14T13:31:00+00:00"
title: "Pitfalls of 'defer' in Go"
categories:
  - Golang
---

![](/images/20180914_01.png)

The `defer` statement is a very useful feature in Go, allowing a method to be delayed until the method enclosing it returns. In practical applications, `defer` can serve the role of try…catch… in other languages and can be used for handling cleanup operations such as closing file handles.

### Timing of `defer` Execution

> A "defer" statement invokes a function whose execution is deferred to the moment the surrounding function returns, either because the surrounding function executed a return statement, reached the end of its function body, or because the corresponding goroutine is panicking.

The official Go documentation explains the timing of `defer` execution as follows:

- When the function enclosing the `defer` returns
- When the function enclosing the `defer` reaches its end
- When the goroutine in which it resides panics

### Order of `defer` Execution

When a method contains multiple `defer` statements, `defer` pushes the methods to be executed later onto a stack. When `defer` is triggered, all the methods on the stack are popped and executed. Therefore, the execution order of `defer` is LIFO (Last In, First Out).

Thus, the output of the following code is not 1 2 3, but 3 2 1.

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

### Pitfall 1: Different Behavior of `defer` in Anonymous and Named Return Value Functions

First, observe the results of executing the following two methods.

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

The first method outputs 0, while the second outputs 1. The first method uses an anonymous return value, while the second uses a named return value. Other than that, the logic is the same. Why is there a difference in output?

To understand this, you need to know the execution logic of `defer`. The documentation states that the `defer` statement is triggered "at" the time of method return, meaning `return` and `defer` execute "simultaneously". Using the anonymous return value method as an example, the process is as follows:

- Assign `result` to the return value (you can think of it as Go automatically creating a return value `retValue`, equivalent to executing `retValue = result`)
- Then check for `defer`, and if present, execute it
- Return the previously created return value (`retValue`)

In this case, the modification in `defer` is applied to `result`, not `retValue`, so `defer` still returns `retValue`. In the named return value method, since the return value is already defined when the method is defined, there is no creation of `retValue`. Thus, `result` is `retValue`, and the modification in `defer` is directly returned.

### Pitfall 2: Potential Performance Issues Using `defer` in a `for` Loop

Consider the following code:

```go
func deferInLoops() {
    for i := 0; i < 100; i++ {
        f, _ := os.Open("/etc/hosts")
        defer f.Close()
    }
}
```

`defer` is declared immediately after the resource creation statement, and the logic seems fine. However, compared to direct invocation, `defer` has additional overhead, such as memory copying for the parameters needed later and pushing and popping the `defer` structure on the stack. Therefore, defining `defer` in a loop can lead to significant resource overhead. In this example, removing the `defer` before the `f.Close()` statement can reduce the extra resource consumption caused by numerous `defer` statements.

### Pitfall 3: Releasing Resources with `defer` Only After Checking for `err`

Some operations to acquire resources may return an `err` parameter. While you can choose to ignore the returned `err` parameter, if you intend to use `defer` for delayed release, you need to check for `err` before using `defer`. If the resource acquisition fails, there's no need and it is not advisable to perform a release operation on the resource. Not checking whether the resource was successfully acquired before executing the release operation can lead to errors in the release method.

The correct approach is as follows:

```go
resp, err := http.Get(url)
// First, check if the operation was successful
if err != nil {
    return err
}
// If successful, then perform the Close operation
defer resp.Body.Close()
```

### Pitfall 4: `defer` Not Executed When Calling `os.Exit`

When a panic occurs, all `defer` statements in the goroutine are executed. However, when the `os.Exit()` method is called to exit the program, `defer` statements are not executed.

```go
func deferExit() {
    defer func() {
        fmt.Println("defer")
    }()
    os.Exit(0)
}
```

The `defer` in the above example will not output anything.