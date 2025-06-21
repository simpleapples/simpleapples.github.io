---
date: "2012-10-20T13:13:00+00:00"
title: "浏览器不支持removeAttribute()的解决方法"
categories:
  - Javascript&CSS
---

今天在做一个网页的时候，想实现 mouse over 时候给 li 加载 background-image，在 mouse out 时候移除 background-image。  
通过 js 实现：

    if(action == 0) {
    	btn.style.backgroundImage = "url(images/index_nav1_07.jpg)";
    	btn.style.backgroundRepeat = "repeat-x";
    } else {
    	btn.removeAttribute("style");
    }

发现可以兼容 ff 和 ie，但是在 chrome 下 mouse out 动作没有执行。

后发现可能是 chrome 不支持 removeAttribute()，于是加入兼容写法：

    if(action == 0) {
    	btn.style.backgroundImage = "url(images/index_nav1_07.jpg)";
    	btn.style.backgroundRepeat = "repeat-x";
    } else {
    	btn.style.backgroundImage = "";
    	btn.style.backgroundRepeat = "";
    	btn.removeAttribute("style");
    }

此方法实现了 ff、ie 和 chrome 兼容。
