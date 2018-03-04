---
layout: post
title: "Air SDK和Flex SDK的区别"
date: 2014-03-27 17:10
comments: true
categories: Actionscript
---

最近将AS开发的SDK从Flex SDK 4.9.1升级到了Air SDK 4.0，导致之前写的一个FLV播放器不能播放视频了，最后发现bug是一个方法内的变量名和类中的一个get方法重名了。类似下图中所示情况：

![Alt text](/upload/air-and-flex-sdk.png)

图中变量time和get方法time重名，而编译器对这种重名的处理在Flex SDK和Air SDK下是不一样的。

Flex SDK下，会根据上下文将```var time:int = time;```中的第二个time作为get方法，而Air SDK中，这行两个time会被当作同一个变量，也就是自己等于自己，而int类型定义时候会被初始化为0，所以使用Air SDK输出结果为0，使用Flex SDK输出结果为1000。

看来Air SDK不如Flex SDK智能啊 :)