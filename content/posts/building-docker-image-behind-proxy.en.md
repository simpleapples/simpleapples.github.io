---
date: "2019-04-18T10:55:00+00:00"
title: "Solution Approach for Using Proxy in Docker Build"
categories:
  - DevOps
---

### Problem Description

When using `docker build` to package an image, there is a need to access the network via a proxy. The following Dockerfile simulates this scenario:

```dockerfile
FROM golang:1.12
RUN curl www.google.com --max-time 3
```

In a typical network environment in China, `curl www.google.com` cannot return normally. The `--max-time` option is added to ensure the curl command does not take too long.

<!-- more -->

### Configuring the http_proxy Variable

First, you need to set the `http_proxy` and `https_proxy` environment variables so that network access commands (represented here by curl) can access www.google.com through the proxy server configured in the environment variables.

Although the `docker build` command is executed on the host where Docker is located and seems to directly use the host's network environment, in reality, `docker build` also starts a container for building. Therefore, all commands during the build process are executed within the container, and the `http_proxy` and `https_proxy` configurations should also be done within the container. You can use `ENV` to configure environment variables in the container.

The proxy server is started on port 1087 of the host. Modify the Dockerfile:

```dockerfile
FROM golang:1.12

ENV http_proxy "http://127.0.0.1:1087"
ENV HTTP_PROXY "http://127.0.0.1:1087"
ENV https_proxy "http://127.0.0.1:1087"
ENV HTTPS_PROXY "http://127.0.0.1:1087"

RUN curl www.google.com --max-time 3
```

Re-running `docker build` will show that curl still cannot access www.google.com. The error message indicates that there is no service on port 1087 of 127.0.0.1.

### Accessing the Host

Since the container uses a bridged network by default, the host and the container are on the same level, placed in a virtual network segment. For the container, accessing the proxy server on the host is essentially accessing a server on another machine, and 127.0.0.1 points to the container itself. In Docker's default bridged network, the host's IP is usually 172.17.0.1 (Linux) or 192.168.65.1 (MacOS). You can change the IP in `http_proxy` to 172.17.0.1/192.168.65.1 to access the network through the host's proxy server. Modify the Dockerfile:

```dockerfile
FROM golang:1.12

ENV http_proxy "http://172.17.0.1:1087"
ENV HTTP_PROXY "http://172.17.0.1:1087"
ENV https_proxy "http://172.17.0.1:1087"
ENV HTTPS_PROXY "http://172.17.0.1:1087"

RUN curl www.google.com --max-time 3
```

Although this method achieves the goal, if the build environment changes or the proxy server configuration changes, even if the operating system changes from Linux to MacOS, the Dockerfile needs to be modified, which is not decoupled enough and not convenient.

### Configuring Network Mode

Docker also has a host network mode, which allows the container to use the host's network, effectively not isolating the container from the host at the network layer. Using this network mode to execute `docker build` eliminates the need to add `http_proxy` environment variables in the Dockerfile, as the container can directly read the environment variables on the host.

First, import the `http_proxy` environment variables on the host:

```bash
export http_proxy="http://127.0.0.1:1087"
export HTTP_PROXY="http://127.0.0.1:1087"
export https_proxy="http://127.0.0.1:1087"
export HTTPS_PROXY="http://127.0.0.1:1087"
```

Next, simplify the Dockerfile:

```dockerfile
FROM golang:1.12
RUN curl www.google.com --max-time 3
```

Re-run `docker build` with the `--network host` parameter to use the host network:

```bash
docker build --network host .
```

After execution, curl can access www.google.com through the proxy just as if it were executed directly on the host.