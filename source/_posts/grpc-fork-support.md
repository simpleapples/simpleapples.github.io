---
layout: post
title: gRPC 跨进程使用引发的问题
date: 2020-04-23 14:30
comments: true
categories: Python
---

### 问题描述

在 Python 项目中使用 gRPC 进行通信，跨进程使用时，会出现阻塞或报错的情况（根据 gRPC.io 的版本不同，现象不同）。下面代码展示了一个跨进程使用的 DEMO，主进程向 30001 端口上的 gRPC 服务器发送请求，子进程也向相同的服务器发送请求。

```python
def send():
    channel = grpc.insecure_channel('localhost:30001')
    stub = message_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(message_pb2.HelloRequest(name='you'))
    print(f"Greeter client received 1: " + response.message)

def main():
    channel = grpc.insecure_channel('localhost:30001')
    stub = message_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello2(message_pb2.HelloRequest(name='you'))
    print("Greeter client received 2: " + response.message)
    p = multiprocessing.Process(target=send)
    p.start()
    p.join()

if __name__ == '__main__':
    main()
```

使用 gRPC.io 1.28.1 的情况下，会发生报错，主进程可以正常收到服务器的返回，但是子进程报 `Socket operation on non-socket`。

```bash
raise _InactiveRpcError(state)
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAVAILABLE
        details = "Socket operation on non-socket"
        debug_error_string = "{"created":"@1587481625.192071231","description":"Error received from peer ipv6:[::1]:50051","file":"src/core/lib/surface/call.cc","file_line":1056,"grpc_message":"Socket operation on non-socket","grpc_status":14}"
>
```

### 排查过程

根据代码，主进程和子进程分别创建了自己的 Channel，看上去逻辑没什么问题，没有什么思路，所以多尝试几种情况先测试一下吧。首先尝试了一下主进程和子进程请求不同的server，在 30001 和 30002 端口分别启动两个 gRPC Server，然后将客户端代码改为主进程请求 30001 端口，子进程请求 30002 端口，代码可以正常运行。测试到这里就更摸不着头脑了，代码明明写的是主进程子进程分别创建 Channel，现在的现象看上去**像是在请求相同服务器的情况下，子进程复用了主进程的socket连接**。gRPC 底层使用的是 HTTP2，而 HTTP2 使用了长连接，会不会是这个原因？

> 有了新的分帧机制后，HTTP/2 不再依赖多个 TCP 连接去并行复用数据流；每个数据流都拆分成很多帧，而这些帧可以交错，还可以分别设定优先级。 因此，所有 HTTP/2 连接都是永久的，而且仅需要每个来源一个连接，随之带来诸多性能优势。 —— [HTTP/2 简介](https://developers.google.com/web/fundamentals/performance/http2?hl=zh-cn)

从 HTTP2 原理上来看还是说的过去的，恰好 gRPC 项目中有 Issue 提到了跨进程使用的问题，参见 [Failed to run grpc python on multiprocessing #18321](https://github.com/grpc/grpc/issues/18321)，开发者在其中说明了像 Demo 那样使用报错的原因。

> **gRPC Core's API for fork support**
> A process may fork after invoking grpc_init() and use gRPC in the child if and only if the child process first destroys all gRPC resources inherited from the parent process and invokes grpc_shutdown().
Subsequent to this, the child will be able to re-initialize and use gRPC. After fork, the parent process will be able to continue to use existing gRPC resources such as channels and calls without interference
from the child process.

> **gRPC Python behavior at fork()**
> To facilitate gRPC Python applications meeting the above constraints, gRPC Python will automatically destroy and shutdown all gRPC Core resources in the child's post-fork handler, including cancelling in-flight calls. From the client's perspective, the child process is now free to create new channels and use gRPC.

简化的说，在 gRPC Core API 的层面，子进程使用 gRPC 需要先销毁掉从父进程 fork 过来的 gRPC 资源，重新创建连接才可以正常使用，否则可能陷入死锁。

同时，gRPC 对于 fork 行为的支持也有一个专门的文档。[https://github.com/grpc/grpc/blob/master/doc/fork_support.md](https://github.com/grpc/grpc/blob/master/doc/fork_support.md)

> The background Python thread was removed entirely. This allows forking after creating a channel. However, the channel must not have issued any RPCs prior to the fork. Attempting to fork with an active channel that has been used can result in deadlocks/corrupted wire data.

从文档和 Issue 的描述看，当主进程有活动状态的 gRPC 连接时，是不可以 fork 的，会引发死锁或者报错（可能和 HTTP2 的长连接机制有关系），如果要 fork，需要先关闭掉活动的连接，在 fork 出的子进程中重新建立 gRPC 连接（也就是主子进程各自持有各自的 HTTP2 连接）。

### 实践方案

综合文档和开发者在 Issue 中提到的方法，要想让 Demo 可以运行有如下三种方法。

- 在环境变量中设置 `GRPC_ENABLE_FORK_SUPPORT=1`（参见[https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111](https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111)）

- 在 fork 子进程前使用 `channel.close()` 关闭活动的 gRPC 连接（参见[https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close](https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close)）
```python
def main():
    channel = grpc.insecure_channel('localhost:30001')
    stub = message_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello2(message_pb2.HelloRequest(name='you'))
    print("Greeter client received 2: " + response.message)
    channel.close() # 关闭 channel，再 fork
    
    p = multiprocessing.Process(target=send)
    p.start()
    p.join()
```

- 使用 `with` 语句，语句结束后会自动关闭活动的 gRPC 连接（参见[https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_client.py#L29](https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_client.py#L29))

```python
def main():
    # 使用 with 语句
    with grpc.insecure_channel('localhost:30001') as channel:
        stub = message_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello2(message_pb2.HelloRequest(name='you'))
        print("Greeter client received 2: " + response.message)
   
    p = multiprocessing.Process(target=send)
    p.start()
    p.join()
```

### 参考资料

[https://grpc.github.io/grpc/python/grpc.html#channel-object](https://grpc.github.io/grpc/python/grpc.html#channel-object)

[https://developers.google.com/web/fundamentals/performance/http2?hl=zh-cn](https://developers.google.com/web/fundamentals/performance/http2?hl=zh-cn)

[https://github.com/grpc/grpc/issues/18321](https://github.com/grpc/grpc/issues/18321)

[https://github.com/grpc/grpc/pull/16264](https://github.com/grpc/grpc/pull/16264)

[https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111](https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111)

[https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close](https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close)