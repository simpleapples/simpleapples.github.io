---
layout: post
title: "一个关于Javascript的小测试"
date: 2012-12-03 21:25
comments: true
categories: Javascript&CSS
---

在SAE的微博上看到一个叫《你是否真的了解javascript？》的小测试，虽然只有几段代码，但却很能说明一些容易忽视的问题。  
先贴下原微博的图：  

![Alt text](/upload/weibocode.jpg)

第一段代码执行结果：1  
Javascript没有提供块级作用域，所以if语句{}中的a，在外部是可见的。  
第二段代码执行结果：1  
这里function 的名字和变量的名字一样，但是  

	var b = function a () {};

这样的用法中，a是被忽略的。也就是funciton a并不影响变量a的值。  
第三段代码执行结果：输出函数本身  
应该说，大家不会这么写代码 = =！，但是呢，既然这么写了，那么首先

	function a() {};

执行后，a的值就是function本身，

	var a;

执行后，实际上没有给a赋值，那么a还是本身，如果执行

	var a = 1;

再输出a就是1了。
第四段代码执行结果：10  
函数接收到参数的时候，是存入到arguments数组里的，而参数的定义x,y,a则分别指向arguments的0,1,2三个位置。  
所以改argument自然输出a也会变。  
第五段代码执行结果：window  
使用

	function.call(null);

或

	function.call(undefined);

时，function的this会被绑定为window。于是输出this就是window。