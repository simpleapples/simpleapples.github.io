---
date: "2012-10-19T12:16:00+00:00"
title: "iOS 推送证书制作 （JAVA/PHP）"
categories:
  - Mobile
---

在使用 Java 或者 PHP 制作 iOS 推送服务器的时候，需要自己从开发者网站上导出的 aps_developer_identity 证书和 Apple Development Push Services 证书进行合成，生成可以供 Java 使用的 p12 证书或供 PHP 使用的 pem 证书。

aps_developer_identity 证书和 Apple Development Push Services 证书的申请过程可以参考：

[http://www.cnblogs.com/hubj/archive/2012/06/14/2549816.html](http://www.cnblogs.com/hubj/archive/2012/06/14/2549816.html)

本文着重讨论如何合成证书

1.将 aps_developer_identity.cer 转换成 pem

```
$openssl x509 -in aps_developer_identity.cer -inform der -out PushChatCert.pem
```

2.将 Apple Development Push Services 证书转换成 pem

```
$openssl pkcs12 -nocerts -out PushChatKey.pem -in Push.p12
```

3.合成两个 pem 证书

1)Java 服务器所需的证书为 p12 格式

```
$openssl pkcs12 -export -in PushChatCert.pem -inkey PushChatKey.pem -out pushCert.p12 -name “apns-cert”
```

2）PHP 服务器所需证书为 pem 格式

```
$cat PushChatCert.pem PushChatKey.pem > pushCert.pem
```
