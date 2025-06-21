---
date: "2018-03-06T20:00:00+00:00"
title: "No More Fear in Interviews: Understand the LRU Algorithm with 20 Lines of Python Code"
categories:
  - Python
---

![](/images/20180306_01.png)

The LRU algorithm is a common topic in backend engineer interviews. This article will help you understand the LRU algorithm and ultimately implement a cache based on the LRU algorithm using Python with ease.

## What is a Cache

![](/images/20180306_02.jpg)

Let's look at a diagram: when we visit a webpage, the browser sends a request to the server, which processes it and returns the page to the browser.

![](/images/20180306_03.jpg)

When multiple browsers access simultaneously, multiple requests are initiated in a short time, and the server has to perform the same series of operations for each request. This repetitive work not only wastes resources but can also slow down response times.

![](/images/20180306_04.jpg)

A cache can save the pages returned by the server, so when other browsers visit, the cache can return the page directly without bothering the server. To ensure quick response times, caches are usually based on expensive hardware like RAM, which means we can't store all pages in the cache. When a requested page isn't cached, the server still needs to be contacted. Due to limited cache capacity and unlimited data volume (the number of new pages generated daily on the internet is incalculable), we need to cache the most useful information.

## What is LRU

LRU is a cache eviction algorithm (also known as a page replacement algorithm in OS). Since cache space is limited, we need to evict infrequently used data to keep frequently used data, maximizing cache efficiency. LRU, which stands for Least Recently Used, is an algorithm that decides which data to evict and which to keep. From its name, "least recently used," we can understand the eviction rules of LRU.

## LRU Eviction Logic

![](/images/20180306_05.png)

Let's use a diagram to describe LRU's eviction logic. The cache in the diagram is a list structure, with the top as the head node and the bottom as the tail node, and a cache capacity of 8 (8 small boxes):

- When new data (meaning the data hasn't been cached before) arrives, it's added to the head of the list.
- When the cache reaches maximum capacity, the excess data needs to be evicted, and the data at the tail of the list is evicted.
- If cached data is accessed, it's moved to the head of the list (equivalent to newly added to the cache).

Following this logic, we can see that data frequently accessed will continuously be moved to the head of the list and won't be evicted, while less frequently accessed data is more likely to be pushed out of the cache.

## Implementing LRU with 20 Lines of Python Code

Next, we'll use Python to implement a cache using the LRU algorithm.

From the previous discussion, we know that a cache simplifies down to two functions: storing data (caching data) and retrieving data (cache hit). Therefore, our cache only needs two external interfaces: `put` and `get`.

According to the previous diagram, internally, we only need a list to implement the LRU logic. However, using a list might be slow for checking cache hits (as it requires traversing the list to check if data exists). In Python, we can use hash-based structures like dictionaries (dict) or sets to quickly check data existence, solving the performance issue of list implementation. But dictionaries and sets are unordered. If there were a data structure that could both sort and store data based on hash, it would be ideal.

In Python's `collections` package, there's a built-in useful structure called `OrderedDict`. `OrderedDict` is a subclass of `dict`, but the elements stored internally are ordered (like a list).

With the data structure problem solved, we can directly write the logic. Here is the code:

```python
class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = collections.OrderedDict()

    def get(self, key):
        if key not in self.queue:
            return -1  # Return -1 if the data is not in the cache
        value = self.queue.pop(key)  # Remove the cache hit data
        self.queue[key] = value  # Re-add the cache hit data to the head
        return self.queue[key]

    def put(self, key, value):
        if key in self.queue:  # If already in cache, remove the old data first
            self.queue.pop(key)
        elif len(self.queue.items()) == self.capacity:
            self.queue.popitem(last=False)  # If not in cache and at max capacity, evict the last data
        self.queue[key] = value  # Add new data to the head
```

Next time you encounter an LRU question in an interview, won't you feel more confident?