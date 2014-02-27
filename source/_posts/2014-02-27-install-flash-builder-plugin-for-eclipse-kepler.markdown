---
layout: post
title: "Eclipse 4.3安装Flash Builder Plugin"
date: 2014-02-27 14:37
comments: true
categories: Actionscript
---

Flash Builder是一个基于Eclipse的IDE，在Flash Builder文件夹下的utilities目录下，官方已经为我们提供了插件版的安装程序，名为Adobe Flash Builder 4.7 Plug-in Utility，插件版可以将Flash Builder嵌入到已经安装好的Eclipse中，作为Eclipse的一个视图，这样就可以在Eclipse中开发AS程序。

执行插件版安装程序后按提示进行，Eclipse目前的最新版是4.3，而Flash Builder 4.7的插件版只支持Eclipse 3.7或4.2版，无法安装在4.3中。

->![Alt text](/upload/flashbuilder4.7plugin.png)<-

解决办法是，下载Eclipse 4.2，现将Flash Builder插件版安装到4.2版的Eclipse中，再拷贝Eclipse文件夹下的dropins目录覆盖Eclipse 4.3的dropins。启动Eclipse 4.3，第一次启动速度会很慢，启动后，Flash Builder插件版就已经安装到Eclipse 4.3中了。