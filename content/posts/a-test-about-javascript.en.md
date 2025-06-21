---
date: "2012-12-03T21:25:00+00:00"
title: "A Small Test About Javascript"
categories:
  - Javascript&CSS
---

I came across a small test called "Do You Really Understand Javascript?" on SAE's microblog. Although it consists of only a few lines of code, it highlights some easily overlooked issues.  
Here's the original image from the microblog:

![Alt text](/images/weibocode.jpg)

Result of the first code snippet: 1  
Javascript does not provide block-level scope, so the variable `a` inside the `if` statement's `{}` is visible outside.  
Result of the second code snippet: 1  
Here, the function name and the variable name are the same, but

    var b = function a () {};

in this usage, `a` is ignored. This means the function `a` does not affect the value of the variable `a`.  
Result of the third code snippet: Outputs the function itself  
It should be noted that people generally wouldn't write code like this = =!, but since it's written this way, first

    function a() {};

after execution, the value of `a` is the function itself,

    var a;

after execution, `a` is not actually assigned a value, so `a` remains itself. If you execute

    var a = 1;

and then output `a`, it would be 1.  
Result of the fourth code snippet: 10  
When a function receives parameters, they are stored in the `arguments` array, and the parameter definitions `x, y, a` point to the 0th, 1st, and 2nd positions of `arguments`, respectively.  
So, changing `arguments` naturally changes the output of `a`.  
Result of the fifth code snippet: window  
When using

    function.call(null);

or

    function.call(undefined);

the `this` of the function is bound to `window`. Therefore, the output of `this` is `window`.
