---
layout: post
title: "破解Google Doodle小游戏"
date: 2013-09-27 07:30
comments: true
categories: 生活
---

今天貌似是Google十五周年纪念日，照例他们在首页上挂了一个JS小游戏，用棒子打一个五角星（十次机会），时机控制的好的话，会掉下糖果。各种刷分之后，最高分停留在了173分。

->![Alt text](/upload/googledoodle1.jpg)<-

本以为这是一个很高的分数了，可上微博一查竟然有不少180分以上的，并且180分以上有彩蛋，这不能忍，于是又是一通刷，不过一直没能达到173以上。  
无奈之下，想从程序上下手。既然是JS游戏，理论上只要修改可以打的次数，就能提高分数。  
去Google首页找JS文件，很容易发现一个[https://www.google.com.hk/logos/2013/bday13/bday13.js](https://www.google.com.hk/logos/2013/bday13/bday13.js)文件，在这里查找数字10，可以发现很多搜索结果，经过直觉判断，感觉```bd=10```这个赋值比较可疑，于是改之。刷新，成功！  
下面是改为99次之后的分数：

->![Alt text](/upload/googledoodle2.png)<-