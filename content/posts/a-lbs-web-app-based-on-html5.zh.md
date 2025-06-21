---
date: "2012-11-10T13:26:00+00:00"
title: "使用javascript和html5制作的LBS类WebApp"
categories:
  - Idea&Demo
---

使用 javascript 和 html5+css3 制作的一个可以显示目前位置以及行动路径的 webapp。

调用了百度地图的 api，在地图上绿色的线画出了当天的路径。

一个 marker 显示了当前的位置。

首页的圆是用 canvas 画的，但是没能把文字画进去，还在研究。

至于获取到的数据都存到了 localStorage 里，目前是每 3s 定位一次，不知道这样的数据量如何，如果数据量大，localStorage 还是不太适合。

还没有仔细测试，应该还有不少 bug。

![Alt text](/upload/cellphonepreview.jpg)

这是在我手机浏览器上运行的效果，定位有些不太准 = =!

演示地址：[http://labs.simpleapples.com/liner](http://labs.simpleapples.com/liner)

### update1:

修改了几个 bug，发布到 github 了。

github:[https://github.com/simpleapples/liner](https://github.com/simpleapples/liner)
