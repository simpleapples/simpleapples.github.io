---
date: "2020-04-23T14:30:00+00:00"
title: "Issues Arising from Cross-Process Use of gRPC"
categories:
  - Python
---

### Problem Description

When using gRPC for communication in a Python project, issues such as blocking or errors can occur when used across processes (the symptoms vary depending on the version of gRPC.io). The following code demonstrates a cross-process usage demo where the main process sends requests to a gRPC server on port 30001, and the child process also sends requests to the same server.

```python
def send():
    channel = grpc.insecure_channel('localhost:30001')
    stub = message_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(message_pb2.HelloRequest(name='you'))
    print(f"Greeter client received 1: " + response.message)

def main():
    channel = grpc.insecure_channel('localhost:30001')
    stub = message_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello2(message_pb2.HelloRequest(name='you'))
    print("Greeter client received 2: " + response.message)
    p = multiprocessing.Process(target=send)
    p.start()
    p.join()

if __name__ == '__main__':
    main()
```

When using gRPC.io version 1.28.1, an error occurs: the main process can receive the server's response normally, but the child process reports `Socket operation on non-socket`.

```bash
raise _InactiveRpcError(state)
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.UNAVAILABLE
        details = "Socket operation on non-socket"
        debug_error_string = "{"created":"@1587481625.192071231","description":"Error received from peer ipv6:[::1]:50051","file":"src/core/lib/surface/call.cc","file_line":1056,"grpc_message":"Socket operation on non-socket","grpc_status":14}"
>
```

### Troubleshooting Process

According to the code, the main process and the child process each create their own Channel. The logic seems fine, but there are no clear ideas, so let's try a few different scenarios for testing. First, I tried having the main process and child process request different servers. Two gRPC Servers were started on ports 30001 and 30002, and the client code was modified so that the main process requests port 30001 and the child process requests port 30002. The code runs normally. At this point, the situation is even more confusing. The code clearly indicates that the main and child processes each create a Channel, but the phenomenon seems to suggest that **when requesting the same server, the child process reuses the socket connection of the main process**. gRPC uses HTTP2 at its core, and HTTP2 uses persistent connections. Could this be the reason?

> With the new framing mechanism, HTTP/2 no longer relies on multiple TCP connections to multiplex streams in parallel; each stream is split into many frames, which can be interleaved and have individual priorities set. Therefore, all HTTP/2 connections are persistent, requiring only one connection per origin, bringing numerous performance benefits. — [Introduction to HTTP/2](https://developers.google.com/web/fundamentals/performance/http2?hl=en)

From the principles of HTTP2, this explanation seems plausible. Coincidentally, there is an issue in the gRPC project that mentions the problem of using gRPC across processes. See [Failed to run grpc python on multiprocessing #18321](https://github.com/grpc/grpc/issues/18321), where the developer explains the reason for the error when using the Demo in this way.

> **gRPC Core's API for fork support**
> A process may fork after invoking grpc_init() and use gRPC in the child if and only if the child process first destroys all gRPC resources inherited from the parent process and invokes grpc_shutdown().
Subsequent to this, the child will be able to re-initialize and use gRPC. After fork, the parent process will be able to continue to use existing gRPC resources such as channels and calls without interference
from the child process.

> **gRPC Python behavior at fork()**
> To facilitate gRPC Python applications meeting the above constraints, gRPC Python will automatically destroy and shutdown all gRPC Core resources in the child's post-fork handler, including cancelling in-flight calls. From the client's perspective, the child process is now free to create new channels and use gRPC.

In simplified terms, at the level of the gRPC Core API, the child process needs to destroy the gRPC resources inherited from the parent process before using gRPC, and then recreate the connection to use it normally; otherwise, it may lead to a deadlock.

Additionally, there is a dedicated document for gRPC's support for fork behavior. [https://github.com/grpc/grpc/blob/master/doc/fork_support.md](https://github.com/grpc/grpc/blob/master/doc/fork_support.md)

> The background Python thread was removed entirely. This allows forking after creating a channel. However, the channel must not have issued any RPCs prior to the fork. Attempting to fork with an active channel that has been used can result in deadlocks/corrupted wire data.

From the document and the issue description, when the main process has an active gRPC connection, it cannot fork, as this will cause deadlocks or errors (possibly related to the persistent connection mechanism of HTTP2). If you need to fork, you must first close the active connection and then re-establish the gRPC connection in the forked child process (meaning that the main and child processes each hold their own HTTP2 connections).

### Practical Solutions

Based on the documentation and the methods mentioned by developers in the issue, there are three ways to make the Demo run:

- Set `GRPC_ENABLE_FORK_SUPPORT=1` in the environment variables (see [https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111](https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111))

- Use `channel.close()` to close the active gRPC connection before forking the child process (see [https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close](https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close))
```python
def main():
    channel = grpc.insecure_channel('localhost:30001')
    stub = message_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello2(message_pb2.HelloRequest(name='you'))
    print("Greeter client received 2: " + response.message)
    channel.close()  # Close the channel before forking
    
    p = multiprocessing.Process(target=send)
    p.start()
    p.join()
```

- Use the `with` statement, which will automatically close the active gRPC connection after the statement ends (see [https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_client.py#L29](https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_client.py#L29))

```python
def main():
    # Use with statement
    with grpc.insecure_channel('localhost:30001') as channel:
        stub = message_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello2(message_pb2.HelloRequest(name='you'))
        print("Greeter client received 2: " + response.message)
   
    p = multiprocessing.Process(target=send)
    p.start()
    p.join()
```

### References

[https://grpc.github.io/grpc/python/grpc.html#channel-object](https://grpc.github.io/grpc/python/grpc.html#channel-object)

[https://developers.google.com/web/fundamentals/performance/http2?hl=en](https://developers.google.com/web/fundamentals/performance/http2?hl=en)

[https://github.com/grpc/grpc/issues/18321](https://github.com/grpc/grpc/issues/18321)

[https://github.com/grpc/grpc/pull/16264](https://github.com/grpc/grpc/pull/16264)

[https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111](https://github.com/grpc/grpc/blob/master/doc/fork_support.md#111)

[https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close](https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.close)