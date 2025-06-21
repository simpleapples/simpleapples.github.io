---
date: "2014-01-08T13:30:00+00:00"
title: "Javscript中Object的Key"
categories:
  - Javascript&CSS
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

为什么给了 obj 两个元素，输出出来却变成了一个呢？难道 c1 和 c2 指向同一个元素？首先 c1 和 c2 是两个不同的 dom 节点，并且通过输出`c1 === c2`会发现结果为 false，而输出`obj[c1] === obj[c2]`的结果却为 true。通过上面结果可以初步推断，c1 和 c2 作为 object 的 key 时，值可能是一样的。object 的 key 所接受的值只有 string 一种，所以当 c1 这个 dom 元素作为 key 时，会被转换为 string 类型，而 c2 和 c1 由于都是 div，所以转换成 string 后，值都是一样的，c2 作为 key 也会覆盖 c1。导致出现只有一个元素的结果。如果 c2 元素变成其他类型的 dom 节点，转换为 string 类型时就会不一样，例如将 c2 改为 ul，还是上面的 js 代码，输出结果为：

```
Object {[object HTMLDivElement]: 1, [object HTMLUListElement]: 2}
```

当使用 object 时，需要注意 key 的类型会被转换为 string。
