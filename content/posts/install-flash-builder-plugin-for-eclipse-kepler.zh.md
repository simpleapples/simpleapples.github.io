---
date: "2014-02-27T14:37:00+00:00"
title: "Eclipse 4.3安装Flash Builder Plugin"
categories:
  - Actionscript
---

Flash Builder 是一个基于 Eclipse 的 IDE，在 Flash Builder 文件夹下的 utilities 目录下，官方已经为我们提供了插件版的安装程序，名为 Adobe Flash Builder 4.7 Plug-in Utility，插件版可以将 Flash Builder 嵌入到已经安装好的 Eclipse 中，作为 Eclipse 的一个视图，这样就可以在 Eclipse 中开发 AS 程序。

执行插件版安装程序后按提示进行，Eclipse 目前的最新版是 4.3，而 Flash Builder 4.7 的插件版只支持 Eclipse 3.7 或 4.2 版，无法安装在 4.3 中。

![Alt text](/images/flashbuilder4.7plugin.png)

解决办法是，下载 Eclipse 4.2，现将 Flash Builder 插件版安装到 4.2 版的 Eclipse 中，再拷贝 Eclipse 文件夹下的 dropins 目录覆盖 Eclipse 4.3 的 dropins。启动 Eclipse 4.3，第一次启动速度会很慢，启动后，Flash Builder 插件版就已经安装到 Eclipse 4.3 中了。
