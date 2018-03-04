---
layout: post
title: "解决超链接点击后周围有虚线框的问题"
date: 2012-10-20 13:03
comments: true
categories: Javascript&CSS
---

在火狐或IE浏览器中点击点击```<a>```标签，标签周围会出现虚线框（如图），影响美观。

![Alt text](/upload/outline.png)

针对IE浏览器解决这个问题的方法是将

	hidefocus="hidefocus"

添加到```<a>```标签中。

针对firefox浏览器的方法是添加css属性

	outline:none