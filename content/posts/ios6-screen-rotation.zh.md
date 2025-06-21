---
date: "2013-05-21T12:26:00+00:00"
title: "iOS6屏幕旋转问题"
categories:
  - Mobile
---

使用 iOS6 SDK 创建 xib 文件时，会默认启用 AutoLayout 功能，AutoLayout 是 iOS6 中新推出的自动布局功能，通过相对定位来实现适应多种屏幕分辩率的自动布局（iOS 设备分辨率会朝着多样化的方向发展？）。  
当使用 AutoLayout 的项目在 iOS6 以下的系统中运行时，程序执行会报错，于是，关闭所有 xib 的 AutoLayout 选项，再次运行，发现原本设置为横屏显示的项目变成了竖屏，所有横屏设置失效。  
解决办法是，在需要横屏的 Controller 中添加如下代码，最好在将 self.window 设定成一个 RootViewController，然后在 RootViewController 中添加如下代码：

    // ios5下的旋屏
    - (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
        return UIInterfaceOrientationIsLandscape(interfaceOrientation);
    }

    // ios6下的旋屏
    -(BOOL)shouldAutorotate {
        return YES;
    }
