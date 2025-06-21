---
date: "2014-02-27T14:37:00+00:00"
title: "Installing Flash Builder Plugin in Eclipse 4.3"
categories:
  - Actionscript
---

Flash Builder is an Eclipse-based IDE. In the utilities directory of the Flash Builder folder, Adobe has provided an installation program for the plugin version, named Adobe Flash Builder 4.7 Plug-in Utility. This plugin version allows you to integrate Flash Builder into an already installed Eclipse as a view, enabling you to develop AS programs within Eclipse.

After running the plugin installation program and following the prompts, you will find that the current latest version of Eclipse is 4.3. However, the Flash Builder 4.7 plugin version only supports Eclipse 3.7 or 4.2 and cannot be installed on 4.3.

![Alt text](/images/flashbuilder4.7plugin.png)

The solution is to download Eclipse 4.2, first install the Flash Builder plugin version into Eclipse 4.2, and then copy the dropins directory from the Eclipse folder to overwrite the dropins directory of Eclipse 4.3. When you start Eclipse 4.3, the first launch will be very slow, but after starting, the Flash Builder plugin version will be installed in Eclipse 4.3.
