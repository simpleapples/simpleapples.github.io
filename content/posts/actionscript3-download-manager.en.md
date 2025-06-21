---
date: "2013-04-24T12:25:00+00:00"
title: "AS3 Download Manager"
categories:
  - Idea&Demo
---

In my work, I needed a global download manager within an application, so I implemented one using AS3.  
An array is used to store the download list. When a new download item is added to the list, it checks the list. If there are items not yet downloaded, it downloads that item. Once the download is complete, it checks the list again. When there is a download in progress, no new download processes are added to ensure that there is only one download process at a time.  
GitHub: [https://github.com/simpleapples/AS3DownloadManager](https://github.com/simpleapples/AS3DownloadManager)