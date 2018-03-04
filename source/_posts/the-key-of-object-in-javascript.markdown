---
layout: post
title: "Javscript中Object的Key"
date: 2014-01-08 13:30
comments: true
categories: Javascript&CSS
---

先来看一段代码：

```
<div id="e1"></div>
<div id="e2"></div>
<script>
	var c1 = document.getElementById("e1");
	var c2 = document.getElementById("e2");
	var obj = {};
	obj[c1] = 1;
	obj[c2] = 2;
	console.log(obj);
</script>
```

上面这段代码会输出什么结果呢？答案是：

```
Object {[object HTMLDivElement]: 2}
```

为什么给了obj两个元素，输出出来却变成了一个呢？难道c1和c2指向同一个元素？首先c1和c2是两个不同的dom节点，并且通过输出```c1 === c2```会发现结果为false，而输出```obj[c1] === obj[c2]```的结果却为true。通过上面结果可以初步推断，c1和c2作为object的key时，值可能是一样的。object的key所接受的值只有string一种，所以当c1这个dom元素作为key时，会被转换为string类型，而c2和c1由于都是div，所以转换成string后，值都是一样的，c2作为key也会覆盖c1。导致出现只有一个元素的结果。如果c2元素变成其他类型的dom节点，转换为string类型时就会不一样，例如将c2改为ul，还是上面的js代码，输出结果为：

```
Object {[object HTMLDivElement]: 1, [object HTMLUListElement]: 2}
```

当使用object时，需要注意key的类型会被转换为string。

