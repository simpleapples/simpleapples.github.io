---
layout: post
title: "浏览器不支持removeAttribute()的解决方法"
date: 2012-10-20 13:13
comments: true
categories: Javascript&CSS
---

今天在做一个网页的时候，想实现mouse over时候给li加载background-image，在mouse out时候移除background-image。  
通过js实现：  

	if(action == 0) {
		btn.style.backgroundImage = "url(images/index_nav1_07.jpg)";
		btn.style.backgroundRepeat = "repeat-x";
	} else {
		btn.removeAttribute("style");
	}

发现可以兼容ff和ie，但是在chrome下mouse out动作没有执行。

后发现可能是chrome不支持removeAttribute()，于是加入兼容写法：

	if(action == 0) {
		btn.style.backgroundImage = "url(images/index_nav1_07.jpg)";
		btn.style.backgroundRepeat = "repeat-x";
	} else {
		btn.style.backgroundImage = "";
		btn.style.backgroundRepeat = "";
		btn.removeAttribute("style");
	}
此方法实现了ff、ie和chrome兼容。