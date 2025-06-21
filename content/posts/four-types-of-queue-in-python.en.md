---
date: "2018-05-22T10:25:00+00:00"
title: "A Brief Analysis of Four Types of Queues in Python"
categories:
  - Python
---

A queue is a linear data structure that only allows insertion operations at one end and deletion operations at the other end.

Searching for "queue" in the Python documentation reveals that the Python standard library includes four types of queues: queue.Queue, asyncio.Queue, multiprocessing.Queue, and collections.deque.

# collections.deque

Deque is short for double-ended queue. Since both ends can be edited, deque can be used to implement both stacks and queues.

Deque supports a rich set of operations, with the main methods illustrated below:

![](/images/20180522_01.jpg)

Compared to queues implemented with lists, those implemented with deque have lower time and space complexity. The space complexity for list implementations during dequeue (pop) and insertion (insert) is approximately O(n), whereas deque has a time complexity of O(1) for both dequeue (pop) and enqueue (append).

Deque also supports the `in` operator, which can be used as follows:

```python
q = collections.deque([1, 2, 3, 4])
print(5 in q)  # False
print(1 in q)  # True
```

Deque also encapsulates methods for clockwise and counterclockwise rotation: rotate.

```python
# Clockwise
q = collections.deque([1, 2, 3, 4])
q.rotate(1)
print(q)  # [4, 1, 2, 3]
q.rotate(1)
print(q)  # [3, 4, 1, 2]

# Counterclockwise
q = collections.deque([1, 2, 3, 4])
q.rotate(-1)
print(q)  # [2, 3, 4, 1]
q.rotate(-1)
print(q)  # [3, 4, 1, 2]
```

In terms of thread safety, by examining the source code of methods like append() and pop() in collections.deque, it is clear that they are atomic operations, thus making them thread-safe under the protection of the GIL.

```c
static PyObject *
deque_append(dequeobject *deque, PyObject *item) { 
    Py_INCREF(item);
    if (deque_append_internal(deque, item, deque->maxlen) < 0) 
        return NULL;
    Py_RETURN_NONE;
}
```

Using the `dis` method, it can be seen that append is an atomic operation (one line of bytecode).

![](/images/20180522_02.png)

In summary, collections.deque is a data structure that conveniently implements queues, is thread-safe, and offers high performance.

# queue.Queue & asyncio.Queue

Both queue.Queue and asyncio.Queue support multi-producer, multi-consumer queues. Based on collections.deque, they both provide Queue (FIFO queue), PriorityQueue (priority queue), and LifoQueue (LIFO queue), with similar interfaces.

The difference lies in their application scenarios: queue.Queue is suitable for multithreading scenarios, while asyncio.Queue is used for communication in coroutine scenarios. Due to the addition of asyncio, the blocking interfaces in queue.Queue are executed by returning coroutine objects in asyncio.Queue. The specific differences are shown in the table below:

|               | queue.Queue                                                                                                                                                                                  | asyncio.Queue                                                                                                                                                                   |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Introduction  | Synchronous queue                                                                                                                                                                            | asyncio queue                                                                                                                                                                   |
| Thread Safety | Yes                                                                                                                                                                                           | No                                                                                                                                                                              |
| Timeout       | Implemented via the timeout parameter                                                                                                                                                        | Implemented via the asyncio.wait_for() method                                                                                                                                   |
| qsize()       | Estimated queue length (between obtaining qsize and the next operation, the queue may be modified by other threads, causing the qsize to change)                                              | Accurate queue length (since it is single-threaded, the queue will not be modified by other threads)                                                                            |
| put() / set() | put(item, block=True, timeout=None), can configure whether the put and set methods are blocking by setting block to True, and can set the maximum duration for blocking operations with timeout | The put() method returns a coroutine object, so there is no block parameter or timeout parameter. For non-blocking methods, use put_nowait(). For blocking methods with timeout, use coroutine asyncio.wait_for(). |

# multiprocessing.Queue

Multiprocessing provides three types of queues: Queue, SimpleQueue, and JoinableQueue.

![](/images/20180522_03.png)

Multiprocessing.Queue is both thread-safe and process-safe, essentially a multi-process clone of queue.Queue. Similar to threading.Queue, multiprocessing.Queue supports put and get operations, with its underlying structure being multiprocessing.Pipe.

The underlying structure of multiprocessing.Queue is based on Pipe, but data is not directly written into the Pipe. Instead, it is written into a local buffer of the process and then written into the underlying Pipe through a feeder thread. This approach is to achieve timeout control and non-blocking put/get operations. Therefore, Queue provides join_thread, cancel_join_thread, and close functions to control the behavior of the feeder. The close function is used to close the feeder thread, join_thread is used to join the feeder thread, and cancel_join_thread is used to prevent automatically joining the feeder thread when the process exits. Using cancel_join_thread may result in data loss if some data has not been written into the Pipe by the feeder.

Unlike threading.Queue, multiprocessing.Queue does not support join() and task_done operations by default. These are supported by using the mp.JoinableQueue object.

SimpleQueue is a simplified queue that removes the buffer from Queue, eliminating potential issues with Queue. However, the put and get methods are blocking and do not have timeout control.

# Summary

By comparison, it can be seen that all four structures implement queues but have different focuses. Collections.deque implements queues at the data structure level but does not support application scenarios, making it a basic data structure. The queue module implements queues for multi-producer and multi-consumer threads, the asyncio.queue module implements queues for multi-producer and multi-consumer coroutines, and the multiprocessing.queue module implements queues for multi-producer and multi-consumer processes.

# References

[https://docs.python.org/3/library/collections.html#collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)  
[https://docs.python.org/3/library/queue.html](https://docs.python.org/3/library/queue.html?highlight=queue#module-queue)  
[https://docs.python.org/3/library/asyncio-queue.html](https://docs.python.org/3/library/asyncio-queue.html?highlight=queue)  
[https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue)  
[https://bugs.python.org/issue15329](https://bugs.python.org/issue15329)  
[http://blog.ftofficer.com/2009/12/python-multiprocessing-3-about-queue/](http://blog.ftofficer.com/2009/12/python-multiprocessing-3-about-queue/)  
[http://cyrusin.github.io/2016/04/27/python-gil-implementaion/](http://cyrusin.github.io/2016/04/27/python-gil-implementaion/)  
