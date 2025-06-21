---
date: "2012-12-02T13:59:00+00:00"
title: "Exploring the 'new' Operator in Javascript"
categories:
  - Javascript&CSS
---

In Javascript, there's an interesting operator called `new`. In [JavaScript: The Good Parts](http://book.douban.com/subject/3590768/), `new` is listed as a not recommended operator. Let's explore the usage of `new`.  
Consider the following code:

```javascript
function test() {
    var foo1 = new function () {
        this.i = 1;
    }
    var foo2 = function () {  
        this.i = 2;
    }
    M.dis(foo1.i);        // 1
    M.dis(foo2.i);        // undefined
    M.dis(this.i);        // undefined
    foo2();
    M.dis(foo2.i);        // undefined
    M.dis(this.i);        // 2
    M.dis(foo1.prototype); // undefined
    M.dis(foo2.prototype); // [object Object]
}
```

*In the code, `M.dis()` is equivalent to `document.writeln()`.*  
The above code clearly illustrates the difference between using and not using the `new` operator.  
Below are my understandings based on the results of using and not using the `new` operator.

1. Functions with the `new` operator are executed immediately. Without `new`, functions execute when called.  
   `foo1` is executed upon definition, hence `foo1.i = 1` is outputted. Since `foo2` is not executed upon definition, its output is `undefined`. The definition `var foo2 = function () {}` is equivalent to `function foo2 () {}`.

2. With the `new` operator, `this` is bound to the function itself.  

   This is straightforward. In the definition of `foo1`, it is executed immediately, so you can think of `foo1` as the execution context of the function, and `this` naturally binds to `foo1`, i.e., the function itself. Therefore, `foo1.i` outputs a result. Without `new`, the function is not executed immediately, and when the function (i.e., `foo2`) is called, the execution context is the `test()` function. Thus, `this.i` in `test()` outputs a result. The `undefined` result for `foo2.i` is understandable since it's akin to executing `foo2().i`, which is not a valid usage.

3. Prototype differences between using and not using the `new` operator.

   When using `new`, a constructor function is instantiated, so its prototype is naturally `undefined`.  
   Without `new`, `foo2` is just a function, and its prototype is the function's prototype.  
   For more on prototype issues with and without `new`, refer to an article by the Taobao UED team:

   [http://ued.taobao.com/blog/2007/05/15/](http://ued.taobao.com/blog/2007/05/15/) Do You Really Know How to Write JavaScript?

### update1: ###
The exploration of the `new` operator is currently limited to `new function`. As for the differences between `new Array()` and `[]`, as well as `new Object()` and `{}`, I believe the differences are not as significant as between `new function` and function. However, some argue there are differences between `new Array()` and `[]` (see comments in "Do You Really Know How to Write JavaScript?").

### update2: ###
There is a significant difference between `new Array()` and array literals. For example, to define an array with a single element `3`, consider the code:

```javascript
var a = new Array(3); // This defines an array with a length of 3
var b = [3]; // Correct!
```

Clearly, only literals can define an array with a single element.