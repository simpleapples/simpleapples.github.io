---
date: "2012-10-19T12:16:00+00:00"
title: "Creating iOS Push Certificates (JAVA/PHP)"
categories:
  - Mobile
---

When setting up an iOS push server using Java or PHP, you need to export the `aps_developer_identity` certificate and the `Apple Development Push Services` certificate from the developer website and combine them to generate a p12 certificate for Java or a pem certificate for PHP.

The application process for the `aps_developer_identity` certificate and the `Apple Development Push Services` certificate can be referenced here:

[http://www.cnblogs.com/hubj/archive/2012/06/14/2549816.html](http://www.cnblogs.com/hubj/archive/2012/06/14/2549816.html)

This article focuses on how to combine the certificates.

1. Convert `aps_developer_identity.cer` to pem:
```
$openssl x509 -in aps_developer_identity.cer -inform der -out PushChatCert.pem
```
2. Convert the `Apple Development Push Services` certificate to pem:
```
$openssl pkcs12 -nocerts -out PushChatKey.pem -in Push.p12
```
3. Combine the two pem certificates:

1) For a Java server, the required certificate format is p12:
```
$openssl pkcs12 -export -in PushChatCert.pem -inkey PushChatKey.pem -out pushCert.p12 -name “apns-cert”
```
2) For a PHP server, the required certificate format is pem:
```
$cat PushChatCert.pem PushChatKey.pem > pushCert.pem
```