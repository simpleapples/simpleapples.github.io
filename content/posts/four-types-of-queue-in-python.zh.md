---
date: "2018-05-22T10:25:00+00:00"
title: "简析Python中的四种队列"
categories:
  - Python
---

队列是一种只允许在一端进行插入操作，而在另一端进行删除操作的线性表。

在 Python 文档中搜索队列（queue）会发现，Python 标准库中包含了四种队列，分别是 queue.Queue / asyncio.Queue / multiprocessing.Queue / collections.deque。

# collections.deque

deque 是双端队列（double-ended queue）的缩写，由于两端都能编辑，deque 既可以用来实现栈（stack）也可以用来实现队列（queue）。

deque 支持丰富的操作方法，主要方法如图：

![](/images/20180522_01.jpg)

相比于 list 实现的队列，deque 实现拥有更低的时间和空间复杂度。list 实现在出队（pop）和插入（insert）时的空间复杂度大约为 O(n)，deque 在出队（pop）和入队（append）时的时间复杂度是 O(1)。

deque 也支持 in 操作符，可以使用如下写法：

```python
q = collections.deque([1, 2, 3, 4])
print(5 in q)  # False
print(1 in q)  # True
```

deque 还封装了顺逆时针的旋转的方法：rotate。

```python
# 顺时针
q = collections.deque([1, 2, 3, 4])
q.rotate(1)
print(q)  # [4, 1, 2, 3]
q.rotate(1)
print(q)  # [3, 4, 1, 2]

# 逆时针
q = collections.deque([1, 2, 3, 4])
q.rotate(-1)
print(q)  # [2, 3, 4, 1]
q.rotate(-1)
print(q)  # [3, 4, 1, 2]
```

线程安全方面，通过查看 collections.deque 中的 append()、pop()等方法的源码可以知道，他们都是原子操作，所以是 GIL 保护下的线程安全方法。

```c
static PyObject *
deque_append(dequeobject *deque, PyObject *item) { 
    Py_INCREF(item);
    if (deque_append_internal(deque, item, deque->maxlen) < 0) 
        return NULL;
    Py_RETURN_NONE;
}
```

通过 dis 方法可以看到，append 是原子操作（一行字节码）。

![](/images/20180522_02.png)

综上，collections.deque 是一个可以方便实现队列的数据结构，具有线程安全的特性，并且有很高的性能。

# queue.Queue & asyncio.Queue

queue.Queue 和 asyncio.Queue 都是支持多生产者、多消费者的队列，基于 collections.deque，他们都提供了 Queue（FIFO 队列）、PriorityQueue（优先级队列）、LifoQueue（LIFO 队列），接口方面也相同。

区别在于 queue.Queue 适用于多线程的场景，asyncio.Queue 适用于协程场景下的通信，由于 asyncio 的加成，queue.Queue 下的阻塞接口在 asyncio.Queue 中则是以返回协程对象的方式执行，具体差异如下表：

|               | queue.Queue                                                                                                                                                                                  | asyncio.Queue                                                                                                                                                                   |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 介绍          | 同步队列                                                                                                                                                                                     | asyncio 队列                                                                                                                                                                    |
| 线程安全      | 是                                                                                                                                                                                           | 否                                                                                                                                                                              |
| 超时机制      | 通过 timeout 参数实现                                                                                                                                                                        | 通过 asyncio.wait_for()方法实现                                                                                                                                                 |
| qsize()       | 预估的队列长度（获取 qsize 到下一个操作之间，queue 有可能被其它的线程修改，导致 qsize 大小发生变化）                                                                                         | 准确的队列长度（由于是单线程，所以 queue 不会被其它线程修改）                                                                                                                   |
| put() / set() | put(item, block=True, timeout=None)，可以通过设置 block 是否为 True 来配置 put 和 set 方法是否为阻塞，并且可以为阻塞操作设置最大时长 timeout，block 为 False 时行为和 put_nowait()方法一致。 | put()方法会返回一个协程对象，所以没有 block 参数和 timeout 参数，如果需要非阻塞方法，可以使用 put_nowait()，如果需要对阻塞方法应用超时，可以使用 coroutine asyncio.wait_for()。 |

# multiprocessing.Queue

multiprocessing 提供了三种队列，分别是 Queue、SimpleQueue、JoinableQueue。

![](/images/20180522_03.png)

multiprocessing.Queue 既是线程安全也是进程安全的，相当于 queue.Queue 的多进程克隆版。和 threading.Queue 很像，multiprocessing.Queue 支持 put 和 get 操作，底层结构是 multiprocessing.Pipe。

multiprocessing.Queue 底层是基于 Pipe 构建的，但是数据传递时并不是直接写入 Pipe，而是写入进程本地 buffer，通过一个 feeder 线程写入底层 Pipe，这样做是为了实现超时控制和非阻塞 put/get，所以 Queue 提供了 join_thread、cancel_join_thread、close 函数来控制 feeder 的行为，close 函数用来关闭 feeder 线程、join_thread 用来 join feeder 线程，cancel_join_thread 用来在控制在进程退出时，不自动 join feeder 线程，使用 cancel_join_thread 有可能导致部分数据没有被 feeder 写入 Pipe 而导致的数据丢失。

和 threading.Queue 不同的是，multiprocessing.Queue 默认不支持 join()和 task_done 操作，这两个支持需要使用 mp.JoinableQueue 对象。

SimpleQueue 是一个简化的队列，去掉了 Queue 中的 buffer，没有了使用 Queue 可能出现的问题，但是 put 和 get 方法都是阻塞的并且没有超时控制。

# 总结

通过对比可以发现，上述四种结构都实现了队列，但是用处却各有偏重，collections.deque 在数据结构层面实现了队列，但是并没有应用场景方面的支持，可以看做是一个基础的数据结构。queue 模块实现了面向多生产线程、多消费线程的队列，asyncio.queue 模块则实现了面向多生产协程、多消费协程的队列，而 multiprocessing.queue 模块实现了面向多成产进程、多消费进程的队列。

# 参考

[https://docs.python.org/3/library/collections.html#collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
[https://docs.python.org/3/library/queue.html](https://docs.python.org/3/library/queue.html?highlight=queue#module-queue)
[https://docs.python.org/3/library/asyncio-queue.html](https://docs.python.org/3/library/asyncio-queue.html?highlight=queue)
[https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue)
[https://bugs.python.org/issue15329](https://bugs.python.org/issue15329)
[http://blog.ftofficer.com/2009/12/python-multiprocessing-3-about-queue/](http://blog.ftofficer.com/2009/12/python-multiprocessing-3-about-queue/)
[http://cyrusin.github.io/2016/04/27/python-gil-implementaion/](http://cyrusin.github.io/2016/04/27/python-gil-implementaion/)
