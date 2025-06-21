---
date: "2012-11-12T13:30:00+00:00"
title: "Decrypting Thunder Links"
categories:
  - Idea&Demo
---

You often come across Thunder links starting with thunder:// on the internet, which cannot be downloaded by other software.

In fact, Thunder links are the result of base64 encryption. By decrypting them, you can retrieve the original link address.

Let's take the link to the Baidu logo image as an example. The original link is:

>http://www.baidu.com/img/baidu_sylogo1.gif

Thunder adds "AA" at the beginning and "ZZ" at the end of the original link, forming a new string:

>AAhttp://www.baidu.com/img/baidu_sylogo1.gifZZ

Then, the string is encrypted using base64 and prefixed with thunder:// to complete the process. If you're interested, you can use the following command in Linux to encrypt the string:

	$echo AAhttp://www.baidu.com/img/baidu_sylogo1.gifZZ | base64

The result is:
>QUFodHRwOi8vd3d3LmJhaWR1LmNvbS9pbWcvYmFpZHVfc3lsb2dvMS5naWZaWg==

Other download software uses similar methods. FlashGet adds ```[FLASHGET]``` at the beginning and end of the string before base64 encryption, while QQ Xuanfeng directly encrypts the link.

Here is an online Thunder link decryption tool: [http://labs.simpleapples.com/thunderurl](http://labs.simpleapples.com/thunderurl)