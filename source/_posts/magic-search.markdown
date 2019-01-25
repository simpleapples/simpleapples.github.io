---
layout: post
title: MagicSearch
date: 2012-12-01 13:49
comments: true
categories: Idea&Demo
---

晚上看到一个OSX上的应用，叫[Alfred](http://www.alfredapp.com/)，是一个类似spotlight的工具，但比spotlight要强大很多。  
不仅可以在里面搜本地程序，而且在搜索的内容前加“>”就可以输命令，可以直接输入算式，也可以自定义搜索引擎，采用诸如“google 你好世界”的方式搜索。  
突发奇想，是不是用Javascript也可以实现？  
于是，首先实现了多搜索引擎集成的功能。  
不想用以前那种下拉菜单的形式，想用自动补全的形式，着实忙活了好长时间，算是把功能做出来了。  
例如，输入“douban 平凡的世界”就可以在豆瓣搜索“平凡的世界”，输入“weibo 前端”就可以搜索“前端”相关的微博。  
还可以输入“t”+回车，然后再输入关键字，就可以搜索淘宝了。  
目前只加入了简单的几个搜索工具（因为帮我设计界面的AlisterTT同学只给我了这几个图标= =!）：  
微博、google、豆瓣、淘宝、亚马逊。  
我给他起了个响亮的名字，MagicSearch，将来如果能做到手机客户端上当然更好了，应该会很有用。  
还有很多东西和细节有待修改。而且计算器的功能也没有加进去，电脑快没电了，只能等到明天了。  
先放个截图：

![Alt text](/upload/magicsearch1.png)

对了，还有演示地址（初步版本，轻拍）：
[http://labs.simpleapples.com/magicsearch](http://labs.simpleapples.com/magicsearch)
### update1: ###
昨天晚上犯懒，没有把搜索引擎的图标和到一张图上，导致输入amazon等搜索引擎名字敲回车之后，右边的图标因为网速没有出来，现在和到一张上了。  
另外放出github地址：
[http://github.com/simpleapples/magicsearch](http://github.com/simpleapples/magicsearch)

至于进入其它搜索引擎之后如何不能返回默认的google搜索的时候，只要点击右边的搜索引擎图标就可以了。
### update2: ###
添加字典、发电子邮件和计算四则运算功能。
字典功能：输入dict 加上要查的单词或词。
发电子邮件功能：输入mail 加上电子邮件地址。
四则运算功能：直接输入算式，见图。

![Alt text](/upload/magicsearch2.png)
