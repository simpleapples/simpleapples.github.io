---
layout: post
title: "创建一个简单的Safari扩展"
date: 2014-10-23 17:40
comments: true
categories: Idea&Demo
---

之前做过一个把网址转为二维码的[Chrome扩展](https://chrome.google.com/webstore/detail/url2qrcode/dohkaoejmhididdilnijehaeegkgchfl?utm_source=chrome-ntp-icon)，想在Safari中也使用这样的扩展，搜索了一下貌似没有同类型的，所以自己打造了一个Safari扩展，并且把过程记录下来。

获得开发者证书
---
要建立一个Safari扩展，首先需要生成一个开发者证书。访问[Apple开发者中心](https://developer.apple.com/account/overview.action)，加入Safari Developer Program，加入开发者计划是免费的。加入开发者计划后就可以生成证书了，访问[Certificates, Identifiers & Profiles](https://developer.apple.com/account/safari/certificate/certificateList.action)，点击右上角的加号，生成一个开发者证书。成功后将证书下载到本地并导入Keychain Access中。

在Safari中创建扩展
---
打开Safari，在菜单中选择*Safari—Preferences-Advanced*，勾选最下方的*Show Develop menu in menu bar*，如图。

![图1](/upload/safari-extension-1.png)

这时在菜单栏中会出现*Develop*菜单，选择*Develope-Show Extension Builder*，打开扩展编辑器，点击左下角的*+*，选择*New Extension*，保存到一个位置（例如Desktop）。

![图2](/upload/safari-extension-2.png)

这时，Desktop文件夹中会出现一个*demo.safariextension*文件夹，这个文件夹里的内容就是我们生成的Safari扩展的根目录。如果前面的开发者证书已经正确导入，扩展的介绍里会出现Safari开发者的Id。

![图3](/upload/safari-extension-3.png)

编辑扩展基本信息
---
扩展建立后，下面会有一票东西需要填写，首先填写扩展的基本信息。

* Display Name: 扩展的显示名称
* Author: 作者名字
* Description: 插件介绍
* Website: 插件网站
* Bundle Identifier: 这里需要填写唯一id
* Update Manifest: 这里需要填写一个plist格式文件的地址，Apple会定期检查这个地址中的Version，如果有升级，就会访问插件的下载地址更新插件，当然，如果插件只是自用而不提交Safari Extensions Gallery的话，这一栏可以不填，plist文件格式如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
   <key>Extension Updates</key>
   <array>
     <dict>
       <key>CFBundleIdentifier</key>
       <string>com.zangzhiya.url2qrcode</string>
       <key>Developer Identifier</key>
       <string>开发者ID</string>
       <key>CFBundleVersion</key>
       <string>1</string>
       <key>CFBundleShortVersionString</key>
       <string>1.0</string>
       <key>URL</key>
       <string>http://simpleapples.com/upload/url2qrcode-safari/url2qrcode.safariextz</string>
     </dict>
   </array>
</dict>
</plist>
```

* Access Level: 这里需要选择插件对页面访问的权限，比如我们我们要做的URL转二维码插件，需要获取当前Tab的URL，那么这里需要选择ALL

![图4](/upload/safari-extension-4.png)

添加图标
---
我们的扩展到现在还没有图标，Safari会分配一个默认的指南针图标，添加图标的方式很简单，在扩展的根目录下放置一个16px * 16px的png格式图片，Safari就会自动将其置为图标。

添加Toolbar Item和Popovers
---
首先看一下这个扩展的完成态，如图。

![图5](/upload/safari-extension-5.png)

可以看到这个插件有两部分组成，一个是工具栏的按钮，在Safari中被称为Toolbar Item，一个是点击按钮后弹出的层，是一个Popover，和Chrome中的Popup类似，这个Popover也是一个html页面。

接下来，需要在Safari Extension Builder中继续编辑，添加一个Toolbar Item和一个Popover，如图。

![图6](/upload/safari-extension-6.png)

Toobar Item红的Image必须是一个8bit的16px * 16px透明背景的黑白png图像（繁琐的要求），而Popover需要是一个html文件。这里的路径都是相对于扩展文件夹的。到这里插件的配置工作就完成了。

编程
---
可以在[我的Github上](https://github.com/simpleapples/url2qrcode-safari)查看这个扩展的代码，里面用到的Safari Api（获取当前页URL），可以在[Safari Developer Libray](https://developer.apple.com/library/safari/documentation/Tools/Conceptual/SafariExtensionGuide/Introduction/Introduction.html)中找到，里面的内容非常详细。

打包
---
当扩展开发完成后，就可以点击Safari Extension Builder中的*Build Package*打包了，打包出来的会是一个*safariextz*格式的文件，双击就可以安装。如果不想提交Safari Extension Gallery，可以直接把这个文件拷贝给他人安装。

![图7](/upload/safari-extension-7.png)