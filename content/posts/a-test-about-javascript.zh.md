---
date: "2012-12-03T21:25:00+00:00"
title: "一个关于Javascript的小测试"
categories:
  - Javascript&CSS
---

在 SAE 的微博上看到一个叫《你是否真的了解 javascript？》的小测试，虽然只有几段代码，但却很能说明一些容易忽视的问题。  
先贴下原微博的图：

![Alt text](/upload/weibocode.jpg)

第一段代码执行结果：1  
Javascript 没有提供块级作用域，所以 if 语句{}中的 a，在外部是可见的。  
第二段代码执行结果：1  
这里 function 的名字和变量的名字一样，但是

    var b = function a () {};

这样的用法中，a 是被忽略的。也就是 funciton a 并不影响变量 a 的值。  
第三段代码执行结果：输出函数本身  
应该说，大家不会这么写代码 = =！，但是呢，既然这么写了，那么首先

    function a() {};

执行后，a 的值就是 function 本身，

    var a;

执行后，实际上没有给 a 赋值，那么 a 还是本身，如果执行

    var a = 1;

再输出 a 就是 1 了。
第四段代码执行结果：10  
函数接收到参数的时候，是存入到 arguments 数组里的，而参数的定义 x,y,a 则分别指向 arguments 的 0,1,2 三个位置。  
所以改 argument 自然输出 a 也会变。  
第五段代码执行结果：window  
使用

    function.call(null);

或

    function.call(undefined);

时，function 的 this 会被绑定为 window。于是输出 this 就是 window。
