---
date: "2014-01-08T13:30:00+00:00"
title: "Object Keys in Javascript"
categories:
  - Javascript&CSS
---

Let's take a look at a piece of code:

```html
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

What will this code output? The answer is:

```
Object {[object HTMLDivElement]: 2}
```

Why does it output only one element when we assigned two elements to `obj`? Could it be that `c1` and `c2` point to the same element? First, `c1` and `c2` are two different DOM nodes, and by outputting `c1 === c2`, you'll find the result is false. However, the result of `obj[c1] === obj[c2]` is true. From the above results, we can initially deduce that when `c1` and `c2` are used as object keys, their values might be the same. An object's key can only be a string, so when the DOM element `c1` is used as a key, it is converted to a string. Since both `c1` and `c2` are div elements, they are converted to the same string value, and `c2` as a key will overwrite `c1`. This results in only one element being present. If `c2` is changed to a different type of DOM node, it will be converted to a different string value. For example, if `c2` is changed to a `ul`, using the same JavaScript code, the output will be:

```
Object {[object HTMLDivElement]: 1, [object HTMLUListElement]: 2}
```

When using objects, it's important to note that the key type will be converted to a string.