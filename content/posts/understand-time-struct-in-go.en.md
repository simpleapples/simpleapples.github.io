---
date: "2018-10-26T17:58:00+00:00"
title: "Understanding Golang's Time Structure"
categories:
  - Golang
---

![](/images/20181026_01.png)

When you create and print a time object in Golang, you'll see an output like this:

```
2018-10-26 14:15:50.306558969 +0800 CST m=+0.000401093
```

The initial part is easy to understand, representing the year, month, day, time, and timezone. But what does the last part `m=+xxxx` signify?

<!-- more -->

### Monotonic Clocks and Wall Clocks

According to the documentation of Golang's time package, the time structure in Golang stores two types of clocks: Wall Clocks and Monotonic Clocks.

Wall Clocks, as the name suggests, represent the time shown on a wall clock, which is the time we usually understand. It is stored as a timestamp since January 1, 1970, 00:00:00. When the system synchronizes time with a time server, it might cause a situation where one second is 2018-1-1 00:00:00, and the next second becomes 2017-12-31 23:59:59. Monotonic Clocks, on the other hand, represent a monotonically increasing time that is unaffected by time synchronization operations. This time represents the number of seconds since the process started.

If you generate a Time object every second and print it, you will see the following output:

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

You can see that the numbers following `m=+` represent the Monotonic Clocks mentioned in the documentation.

### Time Structure

So how are Monotonic Clocks and Wall Clocks stored in Time? Let's take a look at the Time struct.

```go
type Time struct {
	wall uint64
	ext  int64
	loc *Location
}
```

The Time struct consists of three parts. `loc` is straightforward, representing the timezone. The information stored in `wall` and `ext` is relatively complex. Based on the documentation, it can be summarized in the diagram below:

![](/images/20181026_02.jpg)

Unlike many languages that store Unix timestamps (which can only represent time from January 1, 1970, onwards), Golang's Time structure can safely represent time from the year 1885 onwards.

```go
t, _ := time.Parse(time.RFC3339, "1890-01-02T15:04:05Z")
fmt.Println(t) // 1890-01-02 15:04:05 +0000 UTC
```

### Practical Considerations

Since the Time structure might or might not include a Monotonic Clock, you may encounter some issues in practice, such as the following scenario.

```go
now := time.Now()
encodeNow, _ := json.Marshal(now)

decodeNow := time.Time{}
json.Unmarshal(encodeNow, &decodeNow)

fmt.Println(now)  // 2018-10-26 16:04:55.230121766 +0800 CST m=+0.000520419
fmt.Println(decodeNow)  // 2018-10-26 16:04:55.230121766 +0800 CST
```

As you can see, after JSON encoding, the Time structure is represented as a string without the Monotonic Clock, losing the Monotonic Clock information. Naturally, when converting the string back to a Time structure, it differs from the original. The same situation occurs with database storage; the Time structure stored in the database is different from what is retrieved.

When calling `Equal` to compare two Time objects, the comparison will use the Monotonic Clock if both Time objects contain it; otherwise, it will only compare the Wall Clock part.

```go
timeA := time.Now()
timeB := time.Unix(0, timeA.UnixNano())

fmt.Println(timeA)  // 2018-10-26 16:37:02.216165074 +0800 CST m=+0.000363156
fmt.Println(timeB)  // 2018-10-26 16:37:02.216165074 +0800 CST

r := timeA.Equal(timeB)
fmt.Println(r)  // true
```

In the example above, the Wall Clock parts of the two times are the same, one has a Monotonic Clock, and the other doesn't, but the comparison result is that they are equal.

```go
timeA := time.Now()
timeB := time.Unix(timeA.Unix(), 0)

fmt.Println(timeA)  // 2018-10-26 16:38:25.653953438 +0800 CST m=+0.000364851
fmt.Println(timeB)  // 2018-10-26 16:38:25 +0800 CST

r := timeA.Equal(timeB)
fmt.Println(r)  // false
```

It's important to note that the Wall Clock is not just the part before the seconds; it can also be precise to the nanosecond level. Therefore, a time precise to the nanosecond and one precise to the second are different.

For the Monotonic Clock in Time, you can use the `time.Round(0)` method to eliminate it, achieving behavior consistent with other languages.

```go
timeA := time.Now()
timeB := timeA.Round(0)

fmt.Println(timeA)  // 2018-10-26 16:43:03.799263739 +0800 CST m=+0.000357758
fmt.Println(timeB)  // 2018-10-26 16:43:03.799263739 +0800 CST
```

### References

[https://golang.org/pkg/time/](https://golang.org/pkg/time/)