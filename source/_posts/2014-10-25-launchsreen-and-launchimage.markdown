---
layout: post
title: "LaunchImage和LaunchScreen的完美结合"
date: 2014-10-25 12:05
comments: true
categories: Mobile
---

Apple在iOS8中推出了LaunchScreen.xib来代替之前的LaunchImage作为程序的启动界面，相比与LaunchImage，在iOS设备屏幕尺寸越来越多样的情况下，LaunchScreen.xib依托AutoLayout无疑更方便，否则，对于一个兼容iPhone5-iPhone6Plus的应用，就需要有4长不同尺寸的LaunchImage。

但是LaunchScreen只有在iOS8中才能被支持，所以一些开发者还是选择用传统的LaunchImage方式。不过，还有一种方式是将LaunchImage和LaunchScreen结合，在大尺寸iPhone中使用LaunchScreen（iPhone6和iPhone6Plus都是iOS8系统），在iOS7中使用LaunchImage（使用iOS7的手机只有4寸和5.5寸的iPhone，所以只需要两张图）。

首先进入Target配置，找到App Icons and Launch Images，Xcode6中默认使用了LaunchScreen.xib，而LaunchImage则没有使用。

->![图1](/upload/launch-screen-1.png)<-

接下来点击Use Assets Catelog，这时Xcode会在Images.xcassets中生成LaunchImage，这里我们只需要给4寸Retina屏和3.5寸2x屏放两张LaunchImage就好了。

在iOS8中系统会优先调用LaunchScreen作为启动界面，而iOS7不支持LaunchScreen则会使用LaunchImage中的图片作为启动界面。

->![图2](/upload/launch-screen-2.png)<-

项目在iOS7模拟器中运行效果（使用LaunchImage）

->![图3](/upload/launch-screen-3.png)<-

项目在iOS8模拟器中运行效果（使用默认的LaunchScreen.xib）
