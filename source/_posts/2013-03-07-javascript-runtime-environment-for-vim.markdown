---
layout: post
title: "为vim打造javascript运行环境"
date: 2013-03-07 12:24
comments: true
categories: Mac&Linux
---

平时测试javascript代码都是写一个html页面，放到body里面，再在浏览器中执行网页，然后看javascript控制台。突然想到可以使用javascript引擎直接执行js。ok，说干就干。  
google了一下，有Mozilla的引擎SpiderMonkey和google的v8引擎，嗯，既然公认v8引擎比较快，那就用v8吧。不过看了一下网上的文章，安装v8引擎好麻烦 = .=  
忽然想起来nodeJS使用的好像是v8引擎，那么直接用nodeJS执行js就好了。  
上[nodeJS官网](http://nodejs.org)下载最新版，有针对mac的pkg安装包，安装完成后就要让vim使用nodeJS执行js文件了。接下来修改.vimrc文件。  
在.vimrc中为javascript文件添加编译命令：node filename.js，如图。  
完成这些步骤，就可以在vim中直接运行javascript了。