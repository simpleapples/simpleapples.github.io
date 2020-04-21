---
layout: post
title: "15行Python代码，帮你理解令牌桶算法"
date: 2018-03-20 12:50
comments: true
categories: Python
---

![](/upload/20180320_01.jpg)

在网络中传输数据时，为了防止网络拥塞，需限制流出网络的流量，使流量以比较均匀的速度向外发送，令牌桶算法就实现了这个功能，**可控制发送到网络上数据的数目，并允许突发数据的发送。**

# 什么是令牌

从名字上看令牌桶，大概就是一个装有令牌的桶吧，那么什么是令牌呢？

紫薇格格拿的令箭，可以发号施令，令行禁止。在计算机的世界中，令牌也有令行禁止的意思，有令牌，则相当于得到了进行操作的授权，没有令牌，就什么都不能做。

# 用令牌实现限速器

我们用1块令牌来代表发送1字节数据的资格，假设我们源源不断的发放令牌给程序，程序就有资格源源不断的发送数据，当我们不发放令牌给程序，程序就相当于被限流，无法发送数据了。接下来我们说说限速器，所谓限速器，就是让程序在单位时间内，最多只能发送一定大小的数据。假设在1秒发放10块令牌，那么程序发送数据的速度就会被限制在10bytes/s。如果1秒内有大于10bytes的数据需要发送，就会因为没有令牌而被丢弃。

# 改进限速器——加个桶

![](/upload/20180320_02.jpg)

我们实现的限速器，速度是恒定的，但是在实际的应用中，往往会有突发的传输需求（需要更快速的发送，但是不会持续太久，也不会引起网络拥塞），这种数据碰上我们的限速器，就因为拿不到令牌而无法发送。

对限速器进行一下改动，依然1秒产生10块令牌，但是我们把产生出来的令牌先放到一个桶里，当程序需要发送的时候，从桶里取令牌，不需要的时候，令牌就会在桶里沉淀下来，假设桶里沉淀了10块令牌，程序最多就可以在1秒内发送20bytes的数据，满足了突发数据传输的要求，并且由于桶里的令牌被用完，下一秒最多依然只能发10bytes的数据，不会因为持续发送大量数据，对网络造成压力。

![](/upload/20180320_03.jpg)

# 15行Python代码实践令牌桶

令牌桶需要以一定的速度生成令牌放入桶中，当程序要发送数据时，再从桶中取出令牌。这里似乎有点问题，如果我们使用一个死循环，来不停地发放令牌，程序就被阻塞住了，有没有更好的办法？

我们可以在取令牌的时候，用现在的时间减去上次取令牌的时间，乘以令牌的发放速度，计算出桶里可以取的令牌数量（当然不能超过桶的大小），从而避免循环发放的逻辑。

接下来看代码：

```python
import time


class TokenBucket(object):

    # rate是令牌发放速度，capacity是桶的大小
    def __init__(self, rate, capacity):
        self._rate = rate
        self._capacity = capacity
        self._current_amount = 0
        self._last_consume_time = int(time.time())

    # token_amount是发送数据需要的令牌数
    def consume(self, token_amount):
        increment = (int(time.time()) - self._last_consume_time) * self._rate  # 计算从上次发送到这次发送，新发放的令牌数量
        self._current_amount = min(
            increment + self._current_amount, self._capacity)  # 令牌数量不能超过桶的容量
        if token_amount > self._current_amount:  # 如果没有足够的令牌，则不能发送数据
            return False
        self._last_consume_time = int(time.time())
        self._current_amount -= token_amount
        return True
```
