---
layout: post
title: "nettop命令引发的一个小问题"
date: 2012-12-19 12:10
comments: true
categories: Mac&Linux
---

在网上看到一篇帖子，是说Mac OSX 10.7中新加入了一个nettop命令，可以实时查看当前网络链接和数据流量。这是nettop命令的描述：  
>The nettop program displays a list of sockets or routes. The counts for network structures are updated periodically.

于是在Terminal中尝试了一下。  
尝鲜过后就再也没管。但是关闭Terminal大概一两分钟后，Mac的风扇突然疯狂的转了起来。iStatMenu上看达到了5300rpm左右。一般情况下，除非开游戏或者看Flash，才有可能出现风扇飞转的情况，但是看了一下dock发现只开了Chrome、iMessage和iTunes，也没有开Apache之类的服务。打开活动检测器，发现CPU四个核心都已经爆表，查看进程，有两个nettop进程几乎占用了所有CPU资源。

![Alt text](/upload/nettop1.png)

关闭nettop之后，CPU占用率迅速下降，风扇飞转的情况也逐渐消失。

![Alt text](/upload/nettop2.png)

回想一下，可能是使用nettop命令后没有退出nettop，而直接关闭Terminal造成的。经过尝试，发现问题确实出在没有正确退出nettop上。可能这是一个设计中没有考虑到的小bug。  
使用man nettop查看文档，文档说明中退出nettop应该采用q，但没有说必须这样退出，而且很多时候，直接关闭Terminal确实是一些人的习惯，比如我：）