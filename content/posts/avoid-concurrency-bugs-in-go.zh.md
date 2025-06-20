---
date: "2021-08-17T20:53:00+00:00"
title: "规避 Go 中的常见并发 bug"
categories:
  - Golang
---

在[Understanding Real-World Concurrency Bugs in Go](https://cseweb.ucsd.edu/~yiying/GoStudy-ASPLOS19.pdf)这篇论文中，几名研究人员分析了常见的Go并发bug，并在最流行的几个Go开源项目中进行了验证。本文梳理了论文中提到的常见的bug并给出解决方法的分析。

论文中对bugs进行了分类，分为阻塞式和非阻塞式两种：
阻塞式：goroutine发生阻塞无法继续执行（例如死锁）
非阻塞式：不会阻塞执行，但存在潜在的数据冲突（例如并发写）

# 阻塞式bug

阻塞式bug发生的根因有两种，一种是共享内存（例如卡在了意图保护共享内存的锁操作上），一种是消息传递（比如等待chan）。同时研究发现共享内存和消息传递导致的bug数量不想上下，但是共享这种方法的使用量比消息传递使用的更频繁，所以也得出了共享内存方式更不容易导致bug的结论。

## 读写锁优先级导致的死锁

在Go中的写锁优先级高于读锁优先级，假设一个goroutine（goroutine A）连续获取两次读锁，而另一个goroutine（goroutine B）在gouroutine A两次获取读锁中间获取了写锁，就会导致死锁的发生。论文中没有针对这个bug给出示例代码，我写了一个简单的代码示意一下。

```go
func gouroutine1() {
    m.RLock()
    m.RLock()
}

func gouroutine2() {
    m.WLock()
}
```

f1和f2都在goroutine中执行，当f1执行完第一个l.RLock()语句后，假设这时f2的m.WLock执行，由于写锁是排它的，WLock本身被f1的第一个m.RLock()阻塞，写锁操作本身又会阻塞f1中的第二个m.RLock

## WaitGroup误用导致的死锁

这种情况就是比较典型的WaitGroup的误用了，提前执行group.Wait()会导致部分group.Done()无法执行到，进而导致程序被阻塞。

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

for循环内的group.Wait()执行到的时候，循环内的部分goroutine还没有被创建出来，其中的group.Done()也就永远没法执行到，所以会导致永远阻塞在这一句，正确的写法是将group.Wait()移到for循环外。

## Channel的误用

Channel是go支持并发的一个非常重要的特性，Channel虽然在很多场景下非常解决问题，但是误用也是不容易发现的。

```go
func goroutine1() {
    m.Lock()
    ch <- request  // blocked
    m.Unlock()
}

func goroutine2() {
    for {
        m.Lock()  // 阻塞
        m.Unlock()
        request <- ch
    }
}
```

这段代码的业务语义是goroutine1会通过ch接收goroutine2发送的消息，但是当goroutine1执行到ch <- request时候会阻塞并等待ch，此时由于goroutine1没有释放锁，goroutine2的m.Lock()也会阻塞，形成死锁。

## 特殊库的误用

```go
hctx, hcancel := context.WithCancel(ctx)
if timeout > 0 {
    hctx, hcancel = context.WithTimeout(ctx, timeout)
}
```

除了显式的使用channel，go提供了一些lib来在goroutine之间传递消息，上面代码在执行hctx, hcancel := context.WithCancel(ctx)时会创建一个goroutine出来，而当timeout>0时又回创建新的channel赋给同一个变量hcancel，这会导致第一行创建出的channel不会被关闭，也不能再给这个channel发消息。

# 非阻塞式bug

和阻塞式bug类似，非阻塞式bug也由共享内存和消息传递引起：当试图保护一个共享变量失败时候，或消息传递使用不当时候，都可能造成非阻塞式的bug。

## 匿名函数

虽然论文中将这一类错误归结为匿名函数的不正确使用，但实际上产生这类bug的原因是工程师忽略了实际上在跨goroutine共享的变量。

```go
for i := 17; i <= 21; i++ { // write
    go func() { /* Create a new goroutine */ 
        apiVersion := fmt.Sprintf("v1.%d", i) // read
        ...
    }()
}
```

如这段代码（也经常出现在面试中），由于变量i在匿名函数构建出的goroutine和主goroutine共享，又不能保证goroutine什么时候执行，所以goroutine中拿到的i并不确定（大概率这几个循环创建出的goroutine拿到的都是21）。

## WaitGroup的误用

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

上面这段代码中，由于不能保证send方法的goroutine什么时候执行，所以可能导致stop函数的p.wg.Wait()在send函数的p.wg.Add(1)之前执行。

## 特殊库的误用

诸如context这样被设计会在多个goroutine间传递数据的库，在使用时也需要特别注意，可能会导致数据竞争。

## Channel的误用

```go
select {
    case <- c.closed:
    default:
        close(c.closed)
}
```

由于default语句可能被多次触发，导致一个channel可能被多次关闭，进而造成panic。

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

对于上面这段代码，当f是一个耗时函数时，很可能出现一次for循环后stopCh和ticker两个case同时满足，这时是没法确认先进哪个case的。

## 特殊库的误用

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

上面这段代码中，第一行创建的timer由于超时时间是0，所以会立刻触发select中的第一个case，导致和期望不符合的行为。

# 总结

Go的特性使得线程的创建和数据传递都非常容易，但是容易的背后线程间通信的那些坑依然是存在的，论文认为go的消息传递机制会导致更多的bug出现。在我看来，go的消息传递机制相比于传统的共享内存机制，相当于多了一层逻辑层面的封装，这种特性有时会让传统的多线程编程经验不能直接发挥价值，但是只要把握住底层的机制，可以很快积累基于go的语言特性的并发编程经验。
