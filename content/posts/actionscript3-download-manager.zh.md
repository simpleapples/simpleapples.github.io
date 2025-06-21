---
date: "2013-04-24T12:25:00+00:00"
title: "AS3下载管理器"
categories:
  - Idea&Demo
---

工作中需要一个应用内的全局下载管理器，于是使用 AS3 实现了一个。  
使用一个数组来存储下载列表，当向列表中添加一个新的下载项时，会检查列表，如果有未下载项，则下载该项，下载完成后再次检查列表，当目前有进行中的下载时，不添加新的下载进程，以保证同时只有一个下载进程。  
github: [https://github.com/simpleapples/AS3DownloadManager](https://github.com/simpleapples/AS3DownloadManager)
