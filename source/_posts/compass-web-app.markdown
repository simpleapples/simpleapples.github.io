---
layout: post
title: "指南针WebApp"
date: 2012-11-14 13:34
comments: true
categories: Idea&Demo
---

使用javascript制作了一个指南针的WebApp。

监听了DeviceOrientation事件，设备在变换方位时会产生alpha、beta、gamma三个值，而其中的alpha值就是目前的角度值。

	window.addEventListener('deviceorientation',function(event) {
		target.style.transform = 'rotate(' + event.alpha + ')';
	},false);
alpha值以正北为0°，顺时针增加到360°，对应的就是指南针指针的旋转角度。

使用css3的transfrom属性就可以旋转指针。

最后对指南针的度数进行判断，计算出方向（如北偏东XX度，南偏西XX度等）。

只能在支持DeviceOrientation的浏览器上正常使用（mobile safari、android 4.0+ browser、mobile ）

演示地址: [http://labs.simpleapples.com/compass](http://labs.simpleapples.com/compass)

GitHub: [http://github.com/simpleapples/compass](http://github.com/simpleapples/compass)

### update1: ###

发现这个应用在iPhone下会出现将手机初始方向认成正北的问题。= =!

解决方法是使用webkitCompassHeading来获取角度，而不是alpha值。webkitCompassHeading的值是设备方向和地磁北极的角度差，而alpha值是设备转动的角度。参见苹果文档：

[http://developer.apple.com/library/safari/#documentation/SafariDOMAdditions/Reference/DeviceOrientationEventClassRef/DeviceOrientationEvent/DeviceOrientationEvent.html](http://developer.apple.com/library/safari/#documentation/SafariDOMAdditions/Reference/DeviceOrientationEventClassRef/DeviceOrientationEvent/DeviceOrientationEvent.html)

在安卓平台的Opera浏览器下alpha值就是设备和北极的角度差，可能是Opera对html5的支持比较好。