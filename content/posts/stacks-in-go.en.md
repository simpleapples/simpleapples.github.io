---
date: "2018-10-11T18:41:00+00:00"
title: "Stack Space Management in Go"
categories:
  - Golang
---

![](/images/20181011_01.jpg)

### Basic Logic of Stack Space Management

The Go language provides support for concurrent programming through goroutines. Goroutines are a feature of the Go runtime library, not implemented as operating system threads, and can be understood as user-level threads.

Since goroutines are managed by the Go runtime library, the library also needs to create and manage the corresponding stack space for each goroutine. The stack space allocated for each goroutine should not be too large, as it would waste a lot of space when many goroutines are created, nor too small, as it would lead to stack overflow. Go chooses a stack space management strategy where it starts with a relatively small space and automatically grows as needed. When a goroutine no longer needs such a large space, the stack space should also automatically shrink.

### Segment Stacks

Before Go 1.3, Go used segment stacks.

Segment stacks implement a non-contiguous but continuously growing stack. Initially, the stack has only one segment. When more stack space is needed, a new segment is allocated and linked bidirectionally with the previous stack. Thus, a stack consists of multiple bidirectionally linked segments. When the newly allocated segment is no longer needed, it is released.

![](/images/20181011_02.png)

Segment stacks allow on-demand shrinking of the stack and do not require copying data from existing segments when adding new ones, making the cost of using goroutines very low.

The advantage of segment stacks is that they can grow on demand, with relatively high space utilization. However, segment stacks have certain drawbacks in some situations. When a segment is nearly exhausted, using a for loop to execute a function that consumes a lot of space can lead to segment allocation during function execution and segment destruction upon return. This results in multiple stack expansions and contractions within the loop, causing significant performance loss. This situation is known as stack splitting.

### Contiguous Stacks

Go 1.3 introduced contiguous stacks, which use a different strategy. Instead of dividing the stack into segments, when the stack space is insufficient, a new stack space twice the size is allocated, and the data from the original stack space is copied to the new stack space, after which the old stack is destroyed. This prevents stack splitting when the stack space reaches its boundary.

Continuing with the assumption that the current stack space is nearly exhausted and a space-consuming function needs to be executed in a for loop. When the function executes, the stack space expands to twice its original size. After the function completes once, the stack space usage shrinks back to its pre-execution size, but since the usage does not fall below one-fourth of the stack size, stack contraction is not triggered. Thus, during the entire for loop execution, repeated stack space expansion and contraction are avoided.

### Summary

Compared to segment stacks, contiguous stacks avoid frequent stack space expansions and contractions in certain scenarios. It is important to note that shrinking a contiguous stack also requires reallocating a space (half the original size) and performing a stack copy operation.