---
date: "2020-04-16T11:35:00+00:00"
title: "Issue with Viper Failing to Read Configuration from etcd"
categories:
  - Golang
---

### Problem Description

[Viper](https://github.com/spf13/viper) (version 1.1.0 in this context) is a comprehensive configuration solution for Go applications, widely used across various projects. [etcd](https://github.com/etcd-io/etcd) is a distributed key-value store, often used as a configuration center.

Viper supports reading configurations not only from files but also from remote configuration centers. The following code is used for configuration.

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

Running this results in the error `panic: Remote Configurations Error: No Files Found`. Upon investigation, it was found that etcd had TLS enabled, requiring access to its API via HTTPS. The code was updated as follows.

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

Replacing `AddRemoteProvider` with `AddSecureRemoteProvider` did not resolve the issue.

### Problem Diagnosis

Upon tracing the source code, it was discovered that requests to etcd were ultimately sent using the [go-etcd](https://github.com/coreos/go-etcd/) package (which is no longer maintained). In the `requests.go` file of go-etcd, the package uses the net/http package to send requests to etcd.

![](/images/20200416_01.jpg)

At this point, it was realized that the etcd certificate was self-signed. Accessing an HTTPS interface with a self-signed certificate should result in an error. As shown below, accessing the self-signed HTTPS interface of etcd in Chrome results in an invalid certificate warning.

![](/images/20200416_02.jpg)

To investigate further, a simple Go code snippet was written to request the etcd HTTPS interface, as follows.

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

As expected, the code resulted in the error `x509: certificate signed by unknown authority`. This error is understandable since the certificate is self-signed, and the client cannot verify its authenticity. The discrepancy between the behavior of go-etcd and our test code suggested something was overlooked. A thorough review of go-etcd's source code revealed the cause.

![](/images/20200416_03.jpg)

In the `initHTTPSClient` method of the `client.go` file, it was found that certificate verification could be bypassed. This explains why data could be retrieved despite the invalid certificate—certificate verification was skipped, allowing any certificate to be used. This explains why using `AddRemoteProvider` with an HTTPS interface worked. However, it did not explain why `AddSecureRemoteProvider` failed to retrieve content from the HTTPS interface, since both methods ignored certificate verification during the HTTP request phase.

Reviewing the comments for `AddSecureRemoteProvider` revealed the reason.

![](/images/20200416_04.jpg)

It turns out that the "Secure" in `AddSecureRemoteProvider` does not refer to using a secure HTTPS connection. Instead, it refers to an additional decryption step after retrieving the content (Secure refers to requesting encrypted content, not using an encrypted connection). The last parameter is not a client certificate but a decryption GPG key. According to Viper's documentation, this GPG key is optional. In this example, passing an empty string for the GPG key would also work...

A critique of Viper's naming is warranted here; it should be `AddEncryptedRemoteProvider`, not `AddSecureRemoteProvider`.

### Conclusion

The issue arose mainly from a misunderstanding of what the `AddSecureRemoteProvider` interface signifies, compounded by go-etcd's allowance to bypass certificate verification, which made the problem more perplexing.

Of course, go-etcd's configuration is quite reasonable, as using self-signed certificates internally is a common practice.