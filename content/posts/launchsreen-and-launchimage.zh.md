---
date: "2014-10-25T13:20:00+00:00"
title: "iOS8中LaunchImage和LaunchScreen的完美结合"
categories:
  - Mobile
---

Apple 在 iOS8 中推出了 LaunchScreen.xib 来代替之前的 LaunchImage 作为程序的启动界面，相比与 LaunchImage，在 iOS 设备屏幕尺寸越来越多样的情况下，LaunchScreen.xib 依托 AutoLayout 无疑更方便，否则，对于一个兼容 iPhone5-iPhone6Plus 的应用，就需要有 4 长不同尺寸的 LaunchImage。

但是 LaunchScreen 只有在 iOS8 中才能被支持，所以一些开发者还是选择用传统的 LaunchImage 方式。不过，还有一种方式是将 LaunchImage 和 LaunchScreen 结合，在大尺寸 iPhone 中使用 LaunchScreen（iPhone6 和 iPhone6Plus 都是 iOS8 系统），在 iOS7 中使用 LaunchImage（使用 iOS7 的手机只有 4 寸和 5.5 寸的 iPhone，所以只需要两张图）。

首先进入 Target 配置，找到 App Icons and Launch Images，Xcode6 中默认使用了 LaunchScreen.xib，而 LaunchImage 则没有使用。

![图1](/images/launch-screen-1.png)

接下来点击 Use Assets Catelog，这时 Xcode 会在 Images.xcassets 中生成 LaunchImage，这里我们只需要给 4 寸 Retina 屏和 3.5 寸 2x 屏放两张 LaunchImage 就好了。

在 iOS8 中系统会优先调用 LaunchScreen 作为启动界面，而 iOS7 不支持 LaunchScreen 则会使用 LaunchImage 中的图片作为启动界面。

![图2](/images/launch-screen-2.png)

项目在 iOS7 模拟器中运行效果（使用 LaunchImage）

![图3](/images/launch-screen-3.png)

项目在 iOS8 模拟器中运行效果（使用默认的 LaunchScreen.xib）
