---
date: "2012-12-19T12:10:00+00:00"
title: "nettop命令引发的一个小问题"
categories:
  - Mac&Linux
---

在网上看到一篇帖子，是说 Mac OSX 10.7 中新加入了一个 nettop 命令，可以实时查看当前网络链接和数据流量。这是 nettop 命令的描述：

> The nettop program displays a list of sockets or routes. The counts for network structures are updated periodically.

于是在 Terminal 中尝试了一下。  
尝鲜过后就再也没管。但是关闭 Terminal 大概一两分钟后，Mac 的风扇突然疯狂的转了起来。iStatMenu 上看达到了 5300rpm 左右。一般情况下，除非开游戏或者看 Flash，才有可能出现风扇飞转的情况，但是看了一下 dock 发现只开了 Chrome、iMessage 和 iTunes，也没有开 Apache 之类的服务。打开活动检测器，发现 CPU 四个核心都已经爆表，查看进程，有两个 nettop 进程几乎占用了所有 CPU 资源。

![Alt text](/images/nettop1.png)

关闭 nettop 之后，CPU 占用率迅速下降，风扇飞转的情况也逐渐消失。

![Alt text](/images/nettop2.png)

回想一下，可能是使用 nettop 命令后没有退出 nettop，而直接关闭 Terminal 造成的。经过尝试，发现问题确实出在没有正确退出 nettop 上。可能这是一个设计中没有考虑到的小 bug。  
使用 man nettop 查看文档，文档说明中退出 nettop 应该采用 q，但没有说必须这样退出，而且很多时候，直接关闭 Terminal 确实是一些人的习惯，比如我：）
