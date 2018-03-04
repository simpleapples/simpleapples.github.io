---
layout: post
title: "升级到Flex SDK 4.9.1后无法找到基类BitmapAsset的问题"
date: 2013-08-27 12:41
comments: true
categories: Actionscript
---

一个使用flex sdk编译的项目在升级sdk到4.9.1后出现了如下错误：

>errors: 1017: The definition of base class BitmapAsset was not found.

google后发现也有人遇到了这样的问题，详见：[http://mail-archives.apache.org/mod_mbox/flex-dev/201303.mbox/%3CCD596C86.4E4D3%25aharui@adobe.com%3E](http://mail-archives.apache.org/mod_mbox/flex-dev/201303.mbox/%3CCD596C86.4E4D3%25aharui@adobe.com%3E)

flex sdk 4.9中的core.swc的体积比4.8中core.swc的体积小了大概1/2，估计部分基类被从core.swc中移了出来，导致找不到BitmapAsset。

解决办法是，在项目上单击右键——属性——Actionscript构建路径——添加SWC，定位到sdk安装路径下的framework/libs文件夹下，选择framework.swc。

如果展开framework.swc包，可以看到BitmapAsset类，所以将其添加到构建路径中，就可以解决找不到基类的问题。

![Alt text](/upload/frameworkswc.png)