---
date: "2021-08-17T20:53:00+00:00"
title: "Avoiding Common Concurrency Bugs in Go"
categories:
  - Golang
---

In the paper [Understanding Real-World Concurrency Bugs in Go](https://cseweb.ucsd.edu/~yiying/GoStudy-ASPLOS19.pdf), several researchers analyzed common concurrency bugs in Go and validated them in some of the most popular Go open-source projects. This article organizes the common bugs mentioned in the paper and provides an analysis of solutions.

The paper categorizes bugs into two types: blocking and non-blocking:
- Blocking: A goroutine gets blocked and cannot continue execution (e.g., deadlock).
- Non-blocking: Execution is not blocked, but there is a potential data race (e.g., concurrent writes).

# Blocking Bugs

Blocking bugs have two root causes: shared memory (e.g., getting stuck on a lock operation intended to protect shared memory) and message passing (e.g., waiting on a channel). The study found that the number of bugs caused by shared memory and message passing is comparable. However, since shared memory is used more frequently than message passing, it was concluded that shared memory is less likely to lead to bugs.

## Deadlock Due to Read-Write Lock Priority

In Go, write locks have higher priority than read locks. Suppose a goroutine (goroutine A) acquires a read lock twice consecutively, and another goroutine (goroutine B) acquires a write lock between these two read locks of goroutine A. This can lead to a deadlock. The paper does not provide sample code for this bug, so I wrote a simple example to illustrate it.

```go
func goroutine1() {
    m.RLock()
    m.RLock()
}

func goroutine2() {
    m.WLock()
}
```

Both f1 and f2 are executed in goroutines. When f1 completes the first l.RLock() statement, suppose f2's m.WLock executes at this time. Since the write lock is exclusive, WLock itself is blocked by f1's first m.RLock(), and the write lock operation itself will block the second m.RLock in f1.

## Deadlock Due to Misuse of WaitGroup

This is a typical case of WaitGroup misuse. Executing group.Wait() prematurely can prevent some group.Done() from being executed, thus causing the program to block.

```go
var group sync.WaitGroup
group.Add(len(pm.plugins))
for _, p := range pm.plugins {
    go func(p *plugin) {
        defer group.Done()
    }
    group.Wait()  // blocked
}
// group.Wait() should be here
```

When group.Wait() is executed inside the for loop, some goroutines within the loop may not have been created yet, and their group.Done() will never be executed, causing a permanent block at this statement. The correct approach is to move group.Wait() outside the for loop.

## Misuse of Channels

Channels are a crucial feature in Go for supporting concurrency. Although channels solve many problems in various scenarios, their misuse can be challenging to detect.

```go
func goroutine1() {
    m.Lock()
    ch <- request  // blocked
    m.Unlock()
}

func goroutine2() {
    for {
        m.Lock()  // blocked
        m.Unlock()
        request <- ch
    }
}
```

The business logic of this code is that goroutine1 will receive messages sent by goroutine2 through ch. However, when goroutine1 reaches ch <- request, it will block and wait for ch. Since goroutine1 has not released the lock, goroutine2's m.Lock() will also block, forming a deadlock.

## Misuse of Special Libraries

```go
hctx, hcancel := context.WithCancel(ctx)
if timeout > 0 {
    hctx, hcancel = context.WithTimeout(ctx, timeout)
}
```

In addition to explicitly using channels, Go provides some libraries to pass messages between goroutines. In the code above, executing hctx, hcancel := context.WithCancel(ctx) creates a goroutine, and when timeout > 0, a new channel is created and assigned to the same variable hcancel. This results in the channel created in the first line not being closed, and no more messages can be sent to this channel.

# Non-Blocking Bugs

Similar to blocking bugs, non-blocking bugs are also caused by shared memory and message passing: when an attempt to protect a shared variable fails, or when message passing is misused, non-blocking bugs may occur.

## Anonymous Functions

Although the paper attributes this type of error to the incorrect use of anonymous functions, the actual cause of such bugs is engineers overlooking variables that are shared across goroutines.

```go
for i := 17; i <= 21; i++ { // write
    go func() { /* Create a new goroutine */ 
        apiVersion := fmt.Sprintf("v1.%d", i) // read
        ...
    }()
}
```

In this code (often seen in interviews), since the variable i is shared between the anonymous function's constructed goroutine and the main goroutine, and there's no guarantee when the goroutine will execute, the value of i obtained by the goroutine is uncertain (most likely all goroutines created in these loops will get 21).

## Misuse of WaitGroup

```go
func (p *peer) send() {
    p.mu.Lock()
    defer p.mu.Unlock()
    switch p.status {
        case idle:
        go func() {
            p.wg.Add(1)
            ...
            p.wg.Done()
        }()
        case stopped:
    }
}

func (p * peer) stop() {
    p.mu.Lock()
    p.status = stopped
    p.mu.Unlock()
    p.wg.Wait()
}
```

In the above code, since there's no guarantee when the goroutine in the send method will execute, it may cause the p.wg.Wait() in the stop function to execute before p.wg.Add(1) in the send function.

## Misuse of Special Libraries

Libraries like context, designed to pass data between multiple goroutines, require special attention during use as they may cause data races.

## Misuse of Channels

```go
select {
    case <- c.closed:
    default:
        close(c.closed)
}
```

Since the default statement may be triggered multiple times, a channel may be closed multiple times, leading to a panic.

```go
ticker := time.NewTicker()
for{
    f()  // heavy function
    select {
        case <- stopCh: return
        case <- ticker:
    }
}
```

For the above code, when f is a time-consuming function, it's possible for both stopCh and ticker cases to be satisfied after one loop iteration, making it unclear which case will be entered first.

## Misuse of Special Libraries

```go
timer := time.NewTimer(0)
if dur > 0 {
    timer = time.NewTimer(dur)
}

select {
    case <- timer.C:
    case <- ctx.Done():
        return nil
}
```

In the above code, since the timer created in the first line has a timeout of 0, it will immediately trigger the first case in the select, leading to behavior that does not match expectations.

# Conclusion

Go's features make thread creation and data passing very easy, but the pitfalls of inter-thread communication still exist. The paper suggests that Go's message-passing mechanism can lead to more bugs. In my view, Go's message-passing mechanism, compared to traditional shared memory mechanisms, adds an additional layer of logical abstraction. This feature sometimes prevents traditional multithreading programming experience from being directly applicable, but by understanding the underlying mechanisms, one can quickly accumulate concurrency programming experience based on Go's language features.