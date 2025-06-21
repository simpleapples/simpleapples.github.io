---
date: "2013-03-07T12:24:00+00:00"
title: "为vim打造javascript运行环境"
categories:
  - Mac&Linux
---

平时测试 javascript 代码都是写一个 html 页面，放到 body 里面，再在浏览器中执行网页，然后看 javascript 控制台。突然想到可以使用 javascript 引擎直接执行 js。ok，说干就干。  
google 了一下，有 Mozilla 的引擎 SpiderMonkey 和 google 的 v8 引擎，嗯，既然公认 v8 引擎比较快，那就用 v8 吧。不过看了一下网上的文章，安装 v8 引擎好麻烦 = .=  
忽然想起来 nodeJS 使用的好像是 v8 引擎，那么直接用 nodeJS 执行 js 就好了。  
上[nodeJS 官网](http://nodejs.org)下载最新版，有针对 mac 的 pkg 安装包，安装完成后就要让 vim 使用 nodeJS 执行 js 文件了。接下来修改.vimrc 文件。  
在.vimrc 中为 javascript 文件添加编译命令：node filename.js，如图。

![图1](/upload/javascript-enviroment.png)

完成这些步骤，就可以在 vim 中直接运行 javascript 了。
