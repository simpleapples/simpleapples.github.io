---
layout: post
title: 用Python写算法 | 蓄水池算法实现随机抽样
date: 2018-08-05 00:02
comments: true
categories: Python
---

![](/upload/20180805_01.jpg)

> 现在有一组数，不知道这组数的总量有多少，请描述一种算法能够在这组数据中随机抽取k个数，使得每个数被取出来的概率相等。

如果这组数有n个，那么每个数字取到的概率就是k/n，但是这个问题的难点在于不知道这组数的总数，也就是不知道n，那么该怎么计算每个数取到的概率呢？

# 蓄水池算法

游泳池（蓄水池）大家都不陌生，有些游泳池中的水是活的，有入水管也有出水管，那么和泳池体积相当的水流过之后，是不是泳池中所有的水都会被替换呢？当然不是，有的水在泳池中可能会存留很久，有的可能刚进去就流走了。仿照这种现象，蓄水池抽样算法诞生了，蓄水池算法的关键在于保证流入蓄水池的水和已经在池中的水以相同的概率留存在蓄水池中。并且蓄水池算法可以在不预先知道总量的情况下，在时间复杂度O(N)的情况下，来解决这类采样问题。

# 核心原理

这一部分涉及公式，为了保证效果直接贴了图过来。

![](/upload/20180805_02.jpg)

# Python实现

接下来尝试用Python实现一下蓄水池算法，由于蓄水池算法是在事先不知道总量的情况下抽样的，所以定义一个方法来接收单个元素，并且把这个方法放在类中，以持有采样后的数据。

```python
import random


class ReservoirSample(object):

    def __init__(self, size):
        self._size = size
        self._counter = 0
        self._sample = []

    def feed(self, item):
        self._counter += 1
        # 第i个元素（i <= k），直接进入池中
        if len(self._sample) < self._size:
            self._sample.append(item)
            return self._sample
        # 第i个元素（i > k），以k / i的概率进入池中
        rand_int = random.randint(1, self._counter)
        if rand_int <= self._size:
            self._sample[rand_int - 1] = item
        return self._sample
```

# 测试代码

接下来实现一个测试用例验证实现的算法是否正确，既然是随机抽样，无法通过单词测试来验证是否正确，所以通过多次执行的方式来验证，比如从1-10里随机取样3个数，然后执行10000次取样，如果算法正确，最后结果中1-10被取样的次数应该是相同的，都是3000上下。

```python
import unittest
from collections import Counter

from reservoir_sample import ReservoirSample


class TestMain(unittest.TestCase):

    def test_reservoir_sample(self):
        samples = []
        for i in range(10000):
            sample = []
            rs = ReservoirSample(3)
            for item in range(1, 11):
                sample = rs.feed(item)
            samples.extend(sample)
        r = Counter(samples)
        print(r)

if __name__ == '__main__':
    unittest.main()
```

输出的结果如下

```
Counter({7: 3084, 6: 3042, 10: 3033, 3: 3020, 8: 3016, 5: 2997, 4: 2986, 2: 2972, 9: 2932, 1: 2918})
```

上面输出了每个数字被取样到的次数，通过图表可以清晰的看到分布情况

![](/upload/20180805_03.png)

可以看出蓄水池算法对于随机抽样还是非常适合的，每个元素的抽样概率都相同。

# 代码

上述的算法和测试代码已经放在[Github](https://github.com/python-fan/reservoir-sample)，可以直接下载使用。
