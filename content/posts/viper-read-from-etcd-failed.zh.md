---
date: "2020-04-16T11:35:00+00:00"
title: "viper从etcd读取配置失败的问题"
categories:
  - Golang
---

### 问题描述

[Viper](https://github.com/spf13/viper) （本文环境是 Viper 1.1.0）是 Go 应用程序的完整配置解决方案，在很多项目中都有应用。[etcd](https://github.com/etcd-io/etcd)是一个分布式 KV 存储，最直接的应用是配置中心。

Viper 除了支持从文件中读取配置，还支持从远程的配置中心读取配置，使用下面的代码进行配置。

```go
viper.AddRemoteProvider("etcd",
        "http://127.0.0.1:2379",
        "conf.toml")
viper.SetConfigType("toml")
err := viper.ReadRemoteConfig()
if err != nil {
    panic(err)
}
```

运行后报错`panic: Remote Configurations Error: No Files Found`，检查后发现 etcd 开启了 tls，所以需要用 https 协议访问 etcd 的 API，更新代码如下。

```go
viper.AddSecureRemoteProvider("etcd",
        "https://127.0.0.1:2379",
        "conf.toml",
        "key_path")
viper.SetConfigType("toml")
err := viper.ReadRemoteConfig()
if err != nil {
    panic(err)
}
```

使用`AddSecureRemoteProvider`方法替换`AddRemoteProvider`方法，问题依旧。

### 定位问题

跟踪源码发现，最终像 etcd 发送请求的是[go-etcd](https://github.com/coreos/go-etcd/)包（目前 go-etcd 已经不维护），在 go-etcd 的 requests.go 文件中找到了相关的源码，go-etcd 调用了 net/http 包向 etcd 发送请求。

![](/images/20200416_01.jpg)

这个时候忽然想到 etcd 的证书是自签名的，访问自签名证书的 https 接口应该会报错啊，怎么会请求到内容呢？如下图，在 Chrome 中访问 etcd 的自签名 https 接口，会提示证书无效。

![](/images/20200416_02.jpg)

我们自己使用 go 实现一段请求 etcd https 接口的代码，看看到底是什么回事，代码如下。

```go
resp, err := http.Get("https://127.0.0.1:2379/v2/keys/conf.toml?quorum=false&recursive=false&sorted=false")
    if err != nil {
        // handle error
        fmt.Println(err)
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println(err)
    }
    fmt.Println(string(body))
```

果然不一样，我们的代码会报错`x509: certificate signed by unknown authority`，因为是自签名证书，客户端无法验证证书真假，所以这个报错是可以理解的，go-etcd 代码和我们的测试代码表现不一致，一定是我们落下了什么，重新梳理 go-etcd 源码终于发现了原因。

![](/images/20200416_03.jpg)

在 client.go 文件的 initHTTPSClient 方法中，发现允许绕过证书验证，这就可以解释为什么证书无效也能获取到数据了，绕过了证书的验证环节，相当于不管证书真假都拿来用。现在可以解释使用`AddRemoteProvider`方法访问 https 接口为什么可以获取到内容，但是无法解释`AddSecureRemoteProvider`方法为什么无法从 https 接口获取内容，因为两个方法在发送 http 请求阶段的代码是一致的，都忽略了证书验证。

查看`AddSecureRemoteProvider`的注释，发现了原因。

![](/images/20200416_04.jpg)

原来...`AddSecureRemoteProvider`这个 Secure 指的并不是使用安全链接 https，而是在请求到内容后加了一个解密的步骤（Secure 指请求的是加密过的内容，而不是使用加密链接请求），最后一个参数接收的也并不是客户端证书，而是解密的 gpg key... 根据 viper 的文档，这个 gpg key 是可选的，我们这个例子中，如果给 gpg key 传入一个空字符串，也是可以正常执行的...

必须吐槽一下 viper 的命名，哪里是`AddSecureRemoteProvider`，明明应该叫`AddEncryptedRemoteProvider`

### 总结

出现这个问题，主要是误会了`AddSecureRemoteProvider`接口表达的意思，并且 go-etcd 允许忽略证书验证，也让问题变得更加离奇。

当然 go-etcd 的这种配置是非常合理的，内部系统使用自签名证书是一个很正常的行为。
