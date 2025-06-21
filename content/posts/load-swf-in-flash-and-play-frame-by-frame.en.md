---
date: "2012-11-22T13:36:00+00:00"
title: "Loading SWF Files in Flash and Playing Frame by Frame"
categories:
  - Actionscript
---

In Flash, importing and playing SWF files can be easily done using the `loadMovie()` function in ActionScript. However, playing them frame by frame is a bit more complex. When playing frame by frame, you either need to set a play time for each frame or manually control it with buttons.

Here, we'll take an example of playing frame by frame based on time, and explain how to control it using ActionScript.

The code to control frame-by-frame playback is as follows:

```actionscript
var currentPage = _root._currentframe;  // Set the current page variable
var i = 0;
function timer() {
    if(currentPage == _root._currentframe) {  // If it plays to the current page, jump to the next page
        gotoAndPlay(currentPage + 1);
        currentPage = _root._currentframe;
    }
}
timeInter = setInterval(timer, 3000);  // Set the timer to 3000ms
```

Code to load the movie:

```actionscript
loadMovie("XXX.swf",_root);
```

Sample effect image:

![Alt text](/images/flash.png)

The first frame of the Interval layer contains the timer code, and the last frame of the Interval layer is very important:

```actionscript
ClearInterval(timeInter);
```

Clearing the timer in the last frame prevents multiple timers from being added after looping playback.

Each frame in the Stop layer includes the `stop();` command. The Content layer contains the specific content.
