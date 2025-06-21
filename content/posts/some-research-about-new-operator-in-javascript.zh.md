---
date: "2012-12-02T13:59:00+00:00"
title: "Javascript中new操作符的探究"
categories:
  - Javascript&CSS
---

Javascript 中有一个很有意思的 new 操作符，在[《Javascript 语言精粹》（Javascript:The Good Parts）](http://book.douban.com/subject/3590768/)中，new 被列为了不推荐的操作符。下面对于 new 的使用进行一些探究。  
先来一段代码：
function test() {
var foo1 = new function () {
this.i = 1;
}
var foo2 = function () {  
 this.i = 2;
}
M.dis(foo1.i); //1
M.dis(foo2.i); //undefined
M.dis(this.i); //undefined
foo2();
M.dis(foo2.i); //undefined
M.dis(this.i); //2
M.dis(foo1.prototype); //undefined
M.dis(foo2.prototype); //[object Object]
} \*代码中的`M.dis() = document.writeln()`  
上面代码很能说明使用 new 操作符和不使用 new 操作符的区别。  
以下是本人根据以上结果对使用 new 操作符和不使用 new 操作符的一些理解。

1. 使用 new 操作符函数会被立刻执行。不使用 new 操作符，函数会在被调用时执行。  
   foo1 在定义的时候就被执行了，所以输出`foo1.i = 1`，而`foo2`在定义时未被执行，所以输出`foo2`的结果为`undefined`，
   `foo2`中`var foo2 = function () {}`的定义形式和` function foo2 () {}`的效果是一样的。

2. 使用 new 操作符后`this`会被绑定到函数本身。

这一点很好理解，首先`foo1`的定义方式中，`foo1`是立刻执行的，那么为了方便理解可以看成`foo1`是 function 的执行空间，`this`自然就会绑定到`foo1`上，也就是绑定到 function 自身上。于是输出`foo1.i`可以得到结果。而不使用 new 操作符时，函数没有立即执行，当调用该函数（即`foo2`）时，执行空间是`test()`函数，所以在`test()`中输出 this.i 才能得到结果。至于`foo2.i`为 `undefined`的情况也好理解，这样的执行方式相当于执行`foo2().i`，显然，没有这种用法。

3.使用 new 操作符和不使用 new 操作符的原型差异。

使用 new 操作符时，相当于讲一个构造函数实例化了，那么它的 prototype 自然是`undefined`的。  
而不使用 new 操作符时，`foo2`就是一个 function，`foo2`的 prototype 就是 function 的 prototype。  
关于使用 new 和不使用 new 的原型问题，请参考淘宝 UED 团队的一篇文章：

[http://ued.taobao.com/blog/2007/05/15/](http://ued.taobao.com/blog/2007/05/15/)你真的会写 javascript 吗？

### update1:

对于 new 操作符的探究目前仅限于 new function，而对于 new Array()和[] 的区别以及 new Object()和{}的区别，本人认为并没有 new function 和 function 的区别这么大，但也有人说 new Array()和[]是有区别的（见《你真的会写 javascript 吗？》评论）。

### update2:

new Array()和字面量定义 Array 还有一个很重要的区别，比如想定义一个只有一个元素 3 的数组，看代码：

    var a = new Array(3); //这样只能定义一个长度为3的数组
    var b = [3]; //正确！

可见，只有字面量可以定义一个元素的数组。
