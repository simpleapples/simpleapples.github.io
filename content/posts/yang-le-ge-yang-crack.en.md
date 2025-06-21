---
date: "2022-09-20T18:52:00+00:00"
title: "Sheep a Sheep Tech Walkthrough"
categories:
  - Life
---

Recently, "Sheep a Sheep" has become quite popular, but it's extremely difficult. After playing dozens of rounds over a few days without success, I succumbed to my professional habits and decided to see if there was a technological method to beat it. After finding an effective method, I organized it here to help others achieve a tech-based victory.

# Principle

The principle behind a tech-based victory is quite simple. The game presents two maps each day. The first map is a warm-up and can be completed easily, while the second map is extremely challenging. Therefore, if you can change the second map to be the same as the first, you can achieve victory.

# Preparation

To achieve a tech-based victory, you need a Web debugging proxy app. On iOS, you can use HTTP Catcher (requires in-app purchase) or Storm Sniffer (three-day trial). Similar software can be found for Android. Using HTTP Catcher as an example, after installing it, you need to install and enable the Root certificate to achieve HTTPS decryption.

# Steps

First, start HTTP Catcher, open "Sheep a Sheep," and begin the challenge. Then return to HTTP Catcher and filter for JSON-type requests to find the request containing `map_info_ex`.

<center>{{< figure src="/images/20220920_01.png" width="50%">}}</center>

Click into the Response of this request, and you'll see a list with `map_md5`. This list contains two md5 values corresponding to the first and second maps. Our task is to replace the md5 of the second map with that of the first in the returned values.

<center>{{< figure src="/images/20220920_02.png" width="50%">}}</center>

Next, return to the previous screen, swipe left to select more options, and create a new rewrite rule in the pop-up interface.

<center>{{< figure src="/images/20220920_03.png" width="50%">}}</center>

As shown below, select Response and Body, enter the md5 of the second map (which you can copy in advance) into Find, and enter the md5 of the first map into Replace. Then save all the way through.

<center>{{< figure src="/images/20220920_04.png" width="50%">}}</center>

Next, restart HTTP Catcher, return to "Sheep a Sheep," and start the game again. The second level will now be as simple as the first map.

<center>{{< figure src="/images/20220920_05.png" width="50%">}}</center>
