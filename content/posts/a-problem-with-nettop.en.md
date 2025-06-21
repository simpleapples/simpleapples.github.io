---
date: "2012-12-19T12:10:00+00:00"
title: "A Small Issue Triggered by the 'nettop' Command"
categories:
  - Mac&Linux
---

I came across a post online mentioning that Mac OSX 10.7 introduced a new command called `nettop`, which allows you to view current network connections and data flow in real-time. Here is the description of the `nettop` command:

> The nettop program displays a list of sockets or routes. The counts for network structures are updated periodically.

I decided to give it a try in Terminal.  
After experimenting with it, I didn't pay much attention to it. However, about a minute or two after closing Terminal, the fan on my Mac suddenly started spinning wildly. According to iStatMenu, it reached around 5300rpm. Typically, the fan only spins up like this when playing games or watching Flash content, but when I checked the dock, I found that only Chrome, iMessage, and iTunes were open, and no services like Apache were running. Opening Activity Monitor, I discovered that all four CPU cores were maxed out, and two `nettop` processes were consuming almost all CPU resources.

![Alt text](/images/nettop1.png)

After closing `nettop`, CPU usage quickly dropped, and the fan gradually calmed down.

![Alt text](/images/nettop2.png)

Reflecting on this, it might have been caused by not exiting `nettop` properly before closing Terminal. After some testing, I confirmed that the issue indeed stemmed from not exiting `nettop` correctly. This might be a small oversight in the design.  
Using `man nettop` to check the documentation, it states that you should exit `nettop` using 'q', but it doesn't specify that this is mandatory. Moreover, many people, like myself, often close Terminal directly out of habit. :)
