---
layout: post
title: 理解Golang的Time结构
date: 2018-10-26 17:58
comments: true
categories: Golang
---

![](/upload/20181026_01.png)

在golang中创建并打印一个时间对象，会看到如下输出

```
2018-10-26 14:15:50.306558969 +0800 CST m=+0.000401093
```

前面表示的意义好理解，分别是年月日和时间时区，最后的m=+xxxx这部分代表什么呢？

<!-- more --> 

### Monotonic Clocks 和 Wall Clocks

根据golang的time包的文档可以知道，golang的time结构中存储了两种时钟，一种是Wall Clocks，一种是Monotonic Clocks。

Wall Clocks，顾名思义，表示墙上挂的钟，在这里表示我们平时理解的时间，存储的形式是自 1970 年 1 月 1 日 0 时 0 分 0 秒以来的时间戳，当系统和授时服务器进行校准时间时间操作时，有可能造成这一秒是2018-1-1 00:00:00，而下一秒变成了2017-12-31 23:59:59的情况。Monotonic Clocks，意思是单调时间的，所谓单调，就是只会不停的往前增长，不受校时操作的影响，这个时间是自进程启动以来的秒数。

如果每隔一秒生成一个Time并打印出来，就会看到如下输出。

```
2018-10-26 14:15:50.306558969 +0800 CST m=+0.000401093
2018-10-26 14:15:51.310559881 +0800 CST m=+1.004425285
2018-10-26 14:15:52.311822486 +0800 CST m=+2.005711106
2018-10-26 14:15:53.314599457 +0800 CST m=+3.008511329
2018-10-26 14:15:54.31882248 +0800 CST m=+4.012757636
2018-10-26 14:15:55.320059921 +0800 CST m=+5.014018292
2018-10-26 14:15:56.323814998 +0800 CST m=+6.017796644
2018-10-26 14:15:57.324858749 +0800 CST m=+7.018863606
2018-10-26 14:15:58.325164174 +0800 CST m=+8.019192224
2018-10-26 14:15:59.329058535 +0800 CST m=+9.023109863
2018-10-26 14:16:00.329591268 +0800 CST m=+10.023665796
```

可以看到m=+后面所显示的数字，就是文档中所说的Monotonic Clocks。

### Time结构

那么Monotonic Clock和Wall Clock在Time中是怎么存储的呢？来看一下Time结构体。

```go
type Time struct {
	wall uint64
	ext  int64
	loc *Location
}
```

Time结构体中由三部分组成，loc比较明了，表示时区，wall和ext所存储的信息规则相对复杂，根据文档的介绍总结成了下图：

![](/upload/20181026_02.jpg)

golang中的Time结构，不像很多语言保存Unix时间戳（也就是最早只能表示到1970年1月1日），而是至少可以安全的表示1885年以来的时间。

```go
t, _ := time.Parse(time.RFC3339, "1890-01-02T15:04:05Z")
fmt.Println(t) // 1890-01-02 15:04:05 +0000 UTC
```

### 实践中需要注意的问题

既然Time结构所表示的时间，有可能有Monotonic Clock也可能没有，那么在使用中就有可能遇到一些问题，例如下面这种情况。

```go
now := time.Now()
encodeNow, _ := json.Marshal(now)

decodeNow := time.Time{}
json.Unmarshal(encodeNow, &decodeNow)

fmt.Println(now)  // 2018-10-26 16:04:55.230121766 +0800 CST m=+0.000520419
fmt.Println(decodeNow)  // 2018-10-26 16:04:55.230121766 +0800 CST
```

可以看到，经过JSON转码之后，Time结构体会被表示成不带Monotonic Clock的字符串，丢失了Monotonic Clock信息，而将字符串转码回Time结构时，自然也就和转码之前的不一样了。同样的情况，也发生在数据库存储中，存储到数据库里的Time结构和从数据库取出来的也是不一样的。

当调用Equal比较两个Time时，只有两个Time都含有Monotonic Clock时，才会根据Monotonic Clock比较大小，其他情况只比较Wall Clock部分。

```go
timeA := time.Now()
timeB := time.Unix(0, timeA.UnixNano())

fmt.Println(timeA)  // 2018-10-26 16:37:02.216165074 +0800 CST m=+0.000363156
fmt.Println(timeB)  // 2018-10-26 16:37:02.216165074 +0800 CST

r := timeA.Equal(timeB)
fmt.Println(r)  // true
```

上面两个时间的Wall Clock部分相同，一个有Monotonic Clock一个没有，但是比较的结果是两个时间是相同的。

```go
timeA := time.Now()
timeB := time.Unix(timeA.Unix(), 0)

fmt.Println(timeA)  // 2018-10-26 16:38:25.653953438 +0800 CST m=+0.000364851
fmt.Println(timeB)  // 2018-10-26 16:38:25 +0800 CST

r := timeA.Equal(timeB)
fmt.Println(r)  // false
```

需要注意的是Wall Clock并不是秒之前的部分，Wall Clock本身也可以精确到纳秒级别，所以一个精确到纳秒的时间和一个精确到秒的时间也是不同的。

对于Time中的Monotonic Clock，我们可以使用`time.Round(0)`方法将其消除掉，以实现和其他语言一致的行为。

```go
timeA := time.Now()
timeB := timeA.Round(0)

fmt.Println(timeA)  // 2018-10-26 16:43:03.799263739 +0800 CST m=+0.000357758
fmt.Println(timeB)  // 2018-10-26 16:43:03.799263739 +0800 CST
```

### 参考文章

[https://golang.org/pkg/time/](https://golang.org/pkg/time/)
