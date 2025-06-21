---
date: "2014-03-27T17:10:00+00:00"
title: "Air SDK和Flex SDK的区别"
categories:
  - Actionscript
---

最近将 AS 开发的 SDK 从 Flex SDK 4.9.1 升级到了 Air SDK 4.0，导致之前写的一个 FLV 播放器不能播放视频了，最后发现 bug 是一个方法内的变量名和类中的一个 get 方法重名了。类似下图中所示情况：

![Alt text](/upload/air-and-flex-sdk.png)

图中变量 time 和 get 方法 time 重名，而编译器对这种重名的处理在 Flex SDK 和 Air SDK 下是不一样的。

Flex SDK 下，会根据上下文将`var time:int = time;`中的第二个 time 作为 get 方法，而 Air SDK 中，这行两个 time 会被当作同一个变量，也就是自己等于自己，而 int 类型定义时候会被初始化为 0，所以使用 Air SDK 输出结果为 0，使用 Flex SDK 输出结果为 1000。

看来 Air SDK 不如 Flex SDK 智能啊 :)
