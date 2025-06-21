---
date: "2013-09-27T07:30:00+00:00"
title: "Cracking the Google Doodle Game"
categories:
  - Life
---

Today seems to be Google's fifteenth anniversary, and as usual, they have a JS game on their homepage. The game involves hitting a star with a stick (ten attempts), and if you time it right, candies will drop. After various attempts, my highest score was 173.

![Alt text](/images/googledoodle1.jpg)

I initially thought this was a high score, but after checking on Weibo, I found that quite a few people scored over 180, and there’s an Easter egg for scores above 180. I couldn't let this go, so I kept trying but couldn't surpass 173.  
Out of options, I decided to approach it programmatically. Since it's a JS game, theoretically, by modifying the number of attempts, I could increase the score.  
I went to the Google homepage to find the JS file and easily discovered a file at [https://www.google.com.hk/logos/2013/bday13/bday13.js](https://www.google.com.hk/logos/2013/bday13/bday13.js). Searching for the number 10, I found many results. Using intuition, I suspected that the assignment `bd=10` was the key, so I changed it. Refreshed, and success!  
Below is the score after changing it to 99 attempts:

![Alt text](/images/googledoodle2.png)
