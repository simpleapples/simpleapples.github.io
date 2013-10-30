---
layout: post
title: "迅雷链接解密"
date: 2012-11-12 13:30
comments: true
categories: Idea&Demo
---

经常在网上看到迅雷专有的以thunder://开头的连接链接，其它软件无法下载。

其实迅雷连接链接是使用base64加密的结果，只要解密一下，就可以获取到原来的连接链接地址。

拿百度logo图片的连接链接举个例子，原链接为

>http://www.baidu.com/img/baidu_sylogo1.gif

迅雷是在原链接前加AA，后加ZZ，行程一个新的字符串

>AAhttp://www.baidu.com/img/baidu_sylogo1.gifZZ

然后对字符串使用base64加密，再加上thunder://前缀，就完成了。感兴趣的童鞋可以在linux中使用

	$echo AAhttp://www.baidu.com/img/baidu_sylogo1.gifZZ | base64

来加密字符串。结果为：
>QUFodHRwOi8vd3d3LmJhaWR1LmNvbS9pbWcvYmFpZHVfc3lsb2dvMS5naWZaWg==

其它的下载软件使用的方法也大同小异，FlashGet是在字符串前后加```[FLASHGET]``` ，然后base64加密，而QQ旋风则直接对连接链接进行加密。

这里有一个在线的迅雷链接解密程序：[http://labs.simpleapples.com/thunderurl](http://labs.simpleapples.com/thunderurl)