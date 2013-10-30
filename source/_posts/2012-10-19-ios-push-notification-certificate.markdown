---
layout: post
title: "iOS 推送证书制作 （JAVA/PHP）"
date: 2012-10-19 12:16
comments: true
categories: Mobile
---

在使用Java或者PHP制作iOS推送服务器的时候，需要自己从开发者网站上导出的aps_developer_identity证书和Apple Development Push Services证书进行合成，生成可以供Java使用的p12证书或供PHP使用的pem证书。

aps_developer_identity证书和Apple Development Push Services证书的申请过程可以参考：

[http://www.cnblogs.com/hubj/archive/2012/06/14/2549816.html](http://www.cnblogs.com/hubj/archive/2012/06/14/2549816.html)

本文着重讨论如何合成证书

1.将aps_developer_identity.cer转换成pem
```
$openssl x509 -in aps_developer_identity.cer -inform der -out PushChatCert.pem
```
2.将Apple Development Push Services证书转换成pem
```
$openssl pkcs12 -nocerts -out PushChatKey.pem -in Push.p12
```
3.合成两个pem证书

1)Java服务器所需的证书为p12格式
```
$openssl pkcs12 -export -in PushChatCert.pem -inkey PushChatKey.pem -out pushCert.p12 -name “apns-cert”
```
2）PHP服务器所需证书为pem格式
```
$cat PushChatCert.pem PushChatKey.pem > pushCert.pem
```