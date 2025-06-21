---
date: "2013-03-05T12:18:00+00:00"
title: "iOS6文字居中问题"
categories:
  - Mobile
---

升级 Xcode 之后一直没有用过，今天给一个 label 写居中属性，发现以前的文字居中属性 UITextAlignment 已经不推荐使用。如图。

![Alt text](/images/ios6-text1.png)

查看文档，原来在 iOS6 中已经有了新的属性 NSTextAlignment。

![Alt text](/images/ios6-text2.png)

![Alt text](/images/ios6-text3.png)

新属性增加了 Justified 和 Natural，于是好奇在 label 中尝试了一下 Natural 属性。报错。

![Alt text](/images/ios6-text4.png)

提示 textAlignment 中不能使用 NSTextAlignmentNatural，当然，Justified 也不能用（= .=），也就是说，对于 label 标签中的文字，只能使用 center、left、right 三种属性，和 UITextAlignment 一样。ok，那么，什么情况下可以使用 Justified 和 Natural 呢？

搜了一下，没有发现问题的解答，不过从苹果的文档来看，Justified 和 Natural 可能是针对大段文字的，没有尝试，只是推测。(⊙o⊙)…
