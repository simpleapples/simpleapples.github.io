---
date: "2014-10-23T17:40:00+00:00"
title: "创建一个简单的Safari扩展"
categories:
  - Idea&Demo
---

之前做过一个把网址转为二维码的[Chrome 扩展](https://chrome.google.com/webstore/detail/url2qrcode/dohkaoejmhididdilnijehaeegkgchfl?utm_source=chrome-ntp-icon)，想在 Safari 中也使用这样的扩展，搜索了一下貌似没有同类型的，所以自己打造了一个 Safari 扩展，并且把过程记录下来。

## 获得开发者证书

要建立一个 Safari 扩展，首先需要生成一个开发者证书。访问[Apple 开发者中心](https://developer.apple.com/account/overview.action)，加入 Safari Developer Program，加入开发者计划是免费的。加入开发者计划后就可以生成证书了，访问[Certificates, Identifiers & Profiles](https://developer.apple.com/account/safari/certificate/certificateList.action)，点击右上角的加号，生成一个开发者证书。成功后将证书下载到本地并导入 Keychain Access 中。

## 在 Safari 中创建扩展

打开 Safari，在菜单中选择*Safari—Preferences-Advanced*，勾选最下方的*Show Develop menu in menu bar*，如图。

![图1](/images/safari-extension-1.png)

这时在菜单栏中会出现*Develop*菜单，选择*Develope-Show Extension Builder*，打开扩展编辑器，点击左下角的*+*，选择*New Extension*，保存到一个位置（例如 Desktop）。

![图2](/images/safari-extension-2.png)

这时，Desktop 文件夹中会出现一个*demo.safariextension*文件夹，这个文件夹里的内容就是我们生成的 Safari 扩展的根目录。如果前面的开发者证书已经正确导入，扩展的介绍里会出现 Safari 开发者的 Id。

![图3](/images/safari-extension-3.png)

## 编辑扩展基本信息

扩展建立后，下面会有一票东西需要填写，首先填写扩展的基本信息。

- Display Name: 扩展的显示名称
- Author: 作者名字
- Description: 插件介绍
- Website: 插件网站
- Bundle Identifier: 这里需要填写唯一 id
- Update Manifest: 这里需要填写一个 plist 格式文件的地址，Apple 会定期检查这个地址中的 Version，如果有升级，就会访问插件的下载地址更新插件，当然，如果插件只是自用而不提交 Safari Extensions Gallery 的话，这一栏可以不填，plist 文件格式如下：

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
       <string>http://simpleapples.com/images/url2qrcode-safari/url2qrcode.safariextz</string>
     </dict>
   </array>
</dict>
</plist>
```

- Access Level: 这里需要选择插件对页面访问的权限，比如我们我们要做的 URL 转二维码插件，需要获取当前 Tab 的 URL，那么这里需要选择 ALL

![图4](/images/safari-extension-4.png)

## 添加图标

我们的扩展到现在还没有图标，Safari 会分配一个默认的指南针图标，添加图标的方式很简单，在扩展的根目录下放置一个 16px \* 16px 的 png 格式图片，Safari 就会自动将其置为图标。

## 添加 Toolbar Item 和 Popovers

首先看一下这个扩展的完成态，如图。

![图5](/images/safari-extension-5.png)

可以看到这个插件有两部分组成，一个是工具栏的按钮，在 Safari 中被称为 Toolbar Item，一个是点击按钮后弹出的层，是一个 Popover，和 Chrome 中的 Popup 类似，这个 Popover 也是一个 html 页面。

接下来，需要在 Safari Extension Builder 中继续编辑，添加一个 Toolbar Item 和一个 Popover，如图。

![图6](/images/safari-extension-6.png)

Toobar Item 红的 Image 必须是一个 8bit 的 16px \* 16px 透明背景的黑白 png 图像（繁琐的要求），而 Popover 需要是一个 html 文件。这里的路径都是相对于扩展文件夹的。到这里插件的配置工作就完成了。

## 编程

可以在[我的 Github 上](https://github.com/simpleapples/url2qrcode-safari)查看这个扩展的代码，里面用到的 Safari Api（获取当前页 URL），可以在[Safari Developer Libray](https://developer.apple.com/library/safari/documentation/Tools/Conceptual/SafariExtensionGuide/Introduction/Introduction.html)中找到，里面的内容非常详细。

## 打包

当扩展开发完成后，就可以点击 Safari Extension Builder 中的*Build Package*打包了，打包出来的会是一个*safariextz*格式的文件，双击就可以安装。如果不想提交 Safari Extension Gallery，可以直接把这个文件拷贝给他人安装。

![图7](/images/safari-extension-7.png)
