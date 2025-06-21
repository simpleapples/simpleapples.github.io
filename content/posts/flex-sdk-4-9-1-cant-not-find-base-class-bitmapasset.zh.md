---
date: "2013-08-27T12:41:00+00:00"
title: "升级到Flex SDK 4.9.1后无法找到基类BitmapAsset的问题"
categories:
  - Actionscript
---

一个使用 flex sdk 编译的项目在升级 sdk 到 4.9.1 后出现了如下错误：

> errors: 1017: The definition of base class BitmapAsset was not found.

google 后发现也有人遇到了这样的问题，详见：[http://mail-archives.apache.org/mod_mbox/flex-dev/201303.mbox/%3CCD596C86.4E4D3%25aharui@adobe.com%3E](http://mail-archives.apache.org/mod_mbox/flex-dev/201303.mbox/%3CCD596C86.4E4D3%25aharui@adobe.com%3E)

flex sdk 4.9 中的 core.swc 的体积比 4.8 中 core.swc 的体积小了大概 1/2，估计部分基类被从 core.swc 中移了出来，导致找不到 BitmapAsset。

解决办法是，在项目上单击右键——属性——Actionscript 构建路径——添加 SWC，定位到 sdk 安装路径下的 framework/libs 文件夹下，选择 framework.swc。

如果展开 framework.swc 包，可以看到 BitmapAsset 类，所以将其添加到构建路径中，就可以解决找不到基类的问题。

![Alt text](/images/frameworkswc.png)
