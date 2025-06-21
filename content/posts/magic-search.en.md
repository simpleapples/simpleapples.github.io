---
date: "2012-12-01T13:49:00+00:00"
title: "MagicSearch"
categories:
  - Idea&Demo
---

This evening, I came across an OSX application called [Alfred](http://www.alfredapp.com/), which is a tool similar to Spotlight but much more powerful.  
Not only can you search local programs with it, but by adding ">" before the search content, you can input commands, directly enter calculations, and customize search engines using a format like "google Hello World".  
I suddenly wondered if this could be implemented using JavaScript.  
So, I first implemented the multi-search engine integration feature.  
I didn't want to use the old dropdown menu style; instead, I wanted to use an autocomplete format, which took quite a bit of effort, but I managed to get the functionality working.  
For example, typing "douban The Ordinary World" allows you to search "The Ordinary World" on Douban, and typing "weibo frontend" lets you search for "frontend"-related content on Weibo.  
You can also type "t" + Enter, then input a keyword to search on Taobao.  
Currently, I've only added a few simple search tools (because my friend AlisterTT, who helped design the interface, only gave me these icons = =!):  
Weibo, Google, Douban, Taobao, and Amazon.  
I've given it a catchy name, MagicSearch, and it would be even better if it could be developed for mobile clients in the future, as it should be quite useful.  
There are still many things and details to be modified. Also, the calculator function hasn't been added yet, and my computer is running out of battery, so I'll have to wait until tomorrow.  
Here's a screenshot for now:

![Alt text](/images/magicsearch1.png)

Oh, and here's the demo link (preliminary version, please be gentle):
[http://labs.simpleapples.com/magicsearch](http://labs.simpleapples.com/magicsearch)

### update1:

Last night, I was lazy and didn't combine the search engine icons into one image, which caused the icon on the right to not load due to internet speed when entering an engine name like amazon and pressing Enter. Now, they are combined into one image.  
Additionally, here's the GitHub link:
[http://github.com/simpleapples/magicsearch](http://github.com/simpleapples/magicsearch)

As for how to return to the default Google search after entering other search engines, just click the search engine icon on the right.

### update2:

Added dictionary, email sending, and basic arithmetic calculation functions.
Dictionary function: input "dict" followed by the word or phrase you want to look up.
Email sending function: input "mail" followed by the email address.
Basic arithmetic function: directly input the equation, see the image.

![Alt text](/images/magicsearch2.png)
