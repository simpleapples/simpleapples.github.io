---
date: "2012-11-14T13:34:00+00:00"
title: "指南针WebApp"
categories:
  - Idea&Demo
---

使用 javascript 制作了一个指南针的 WebApp。

监听了 DeviceOrientation 事件，设备在变换方位时会产生 alpha、beta、gamma 三个值，而其中的 alpha 值就是目前的角度值。

    window.addEventListener('deviceorientation',function(event) {
    	target.style.transform = 'rotate(' + event.alpha + ')';
    },false);

alpha 值以正北为 0°，顺时针增加到 360°，对应的就是指南针指针的旋转角度。

使用 css3 的 transfrom 属性就可以旋转指针。

最后对指南针的度数进行判断，计算出方向（如北偏东 XX 度，南偏西 XX 度等）。

只能在支持 DeviceOrientation 的浏览器上正常使用（mobile safari、android 4.0+ browser、mobile ）

演示地址: [http://labs.simpleapples.com/compass](http://labs.simpleapples.com/compass)

GitHub: [http://github.com/simpleapples/compass](http://github.com/simpleapples/compass)

### update1:

发现这个应用在 iPhone 下会出现将手机初始方向认成正北的问题。= =!

解决方法是使用 webkitCompassHeading 来获取角度，而不是 alpha 值。webkitCompassHeading 的值是设备方向和地磁北极的角度差，而 alpha 值是设备转动的角度。参见苹果文档：

[http://developer.apple.com/library/safari/#documentation/SafariDOMAdditions/Reference/DeviceOrientationEventClassRef/DeviceOrientationEvent/DeviceOrientationEvent.html](http://developer.apple.com/library/safari/#documentation/SafariDOMAdditions/Reference/DeviceOrientationEventClassRef/DeviceOrientationEvent/DeviceOrientationEvent.html)

在安卓平台的 Opera 浏览器下 alpha 值就是设备和北极的角度差，可能是 Opera 对 html5 的支持比较好。
