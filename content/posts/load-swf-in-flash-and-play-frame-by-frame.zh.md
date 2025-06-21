---
date: "2012-11-22T13:36:00+00:00"
title: "在Flash中载入swf文件并逐帧播放"
categories:
  - Actionscript
---

在 Flash 中导入 swf 并且播放，使用 ActionScript 中的 loadMovie()函数就可以完成，但是如果要逐帧播放就比较麻烦了。因为逐帧播放时，要么给每帧定一个播放时间，要么然手动设置按钮控制。

这里以按时间逐帧播放为例，介绍一下如何使用 ActionScript 控制。

控制逐帧播放的代码如下：

    var currentPage = _root._currentframe;  //设定当前页变量
    var i = 0;
    function timer() {
    	if(currentPage == _root._currentframe) {  //如果播放到当前页则跳到下一页
    		gotoAndPlay(currentPage + 1);
    		currentPage = _root._currentframe;
    	}
    }
    timeInter = setInterval(timer, 3000);  //设置定时器3000ms

载入影片代码：

    loadMovie("XXX.swf",_root);

具体效果图：

![Alt text](/images/flash.png)

Interval 层第一帧为计时器代码，Interval 最后一帧代码非常重要：

    ClearInterval(timeInter);

最后一帧清除掉计时器，是防止循环播放后重复添加多个计时器。
Stop 层每一帧添加 stop();命令。Content 层为具体内容。
