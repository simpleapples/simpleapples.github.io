---
date: "2012-11-10T13:26:00+00:00"
title: "WebApp for LBS Using JavaScript and HTML5"
categories:
  - Idea&Demo
---

A web app created using JavaScript, HTML5, and CSS3 that can display the current location and movement path.

It utilizes the Baidu Maps API to draw the day's path with a green line on the map.

A marker shows the current location.

The circle on the homepage is drawn using canvas, but I haven't managed to include text in it yet—still working on that.

The acquired data is stored in localStorage. Currently, it locates every 3 seconds. I'm unsure about the data volume; if it's large, localStorage might not be suitable.

I haven't thoroughly tested it yet, so there are likely several bugs.

![Alt text](/images/cellphonepreview.jpg)

This is how it runs on my mobile browser, though the location accuracy isn't very precise = =!

Demo link: [http://labs.simpleapples.com/liner](http://labs.simpleapples.com/liner)

### update1:

Fixed a few bugs and released it on GitHub.

GitHub: [https://github.com/simpleapples/liner](https://github.com/simpleapples/liner)
