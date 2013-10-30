---
layout: post
title: "iOS6文字居中问题"
date: 2013-03-05 12:18
comments: true
categories: Mobile
---

升级Xcode之后一直没有用过，今天给一个label写居中属性，发现以前的文字居中属性UITextAlignment已经不推荐使用。如图。

->![Alt text](/upload/ios6-text1.png)<-

查看文档，原来在iOS6中已经有了新的属性NSTextAlignment。

->![Alt text](/upload/ios6-text2.png)<-

->![Alt text](/upload/ios6-text3.png)<-

新属性增加了Justified和Natural，于是好奇在label中尝试了一下Natural属性。报错。

->![Alt text](/upload/ios6-text4.png)<-

提示textAlignment中不能使用NSTextAlignmentNatural，当然，Justified也不能用（= .=），也就是说，对于label标签中的文字，只能使用center、left、right三种属性，和UITextAlignment一样。ok，那么，什么情况下可以使用Justified和Natural呢？

搜了一下，没有发现问题的解答，不过从苹果的文档来看，Justified和Natural可能是针对大段文字的，没有尝试，只是推测。(⊙o⊙)…