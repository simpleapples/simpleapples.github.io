---
layout: post
title: "iOS6屏幕旋转问题"
date: 2013-05-21 12:26
comments: true
categories: Mobile
---

使用iOS6 SDK创建xib文件时，会默认启用AutoLayout功能，AutoLayout是iOS6中新推出的自动布局功能，通过相对定位来实现适应多种屏幕分辩率的自动布局（iOS设备分辨率会朝着多样化的方向发展？）。  
当使用AutoLayout的项目在iOS6以下的系统中运行时，程序执行会报错，于是，关闭所有xib的AutoLayout选项，再次运行，发现原本设置为横屏显示的项目变成了竖屏，所有横屏设置失效。  
解决办法是，在需要横屏的Controller中添加如下代码，最好在将self.window设定成一个RootViewController，然后在RootViewController中添加如下代码：

	// ios5下的旋屏
	- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
	    return UIInterfaceOrientationIsLandscape(interfaceOrientation);
	}
	
	// ios6下的旋屏
	-(BOOL)shouldAutorotate {
	    return YES;
	}