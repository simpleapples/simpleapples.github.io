---
date: "2018-06-20T14:00:00+00:00"
title: "Major Issue! Uninstalling WeGame Solves XPS 15 Blue Screen Problem"
categories:
  - Tech
---

# Incubation Period

At the end of April last year, I bought a US version of the XPS 15 9560. After using it for a few months, it occasionally started to blue screen. I had seen many complaints about XPS quality control on forums before, so I thought I was just unlucky. Fortunately, the blue screens were infrequent and didn't affect usage, so I didn't pay much attention.

# Escalation Period

This May, after upgrading to Win10 1803 (I usually upgrade software immediately to experience the latest improvements), the blue screens became more frequent and started affecting usage. So, I began investigating the problem.

In my haste, I didn't check the dump files but directly Googled the XPS 15 blue screen issue, hoping to find a quick solution. I quickly found that many people had similar issues, with many attributing it to poor XPS 15 quality control. After reading a lot, I suspected the drivers (Dell has a Dell Update software that prompts me to update drivers). I started with the most frequently updated graphics driver, downgrading it to the previous version, but it didn't help. Then I downgraded the WiFi driver, as it was also recently updated, and the XPS 15's Killer card seemed to have compatibility issues.

![Driver list of XPS 15, showing recent updates for WiFi and graphics drivers](/images/20180620_01.png)

After downgrading the drivers, the computer had a brief period of stability, with no blue screens for a few hours. However, more unfortunate problems were about to occur.

# Outbreak Period

While using QQ to receive a large file, about 1GB, the computer blue screened halfway through. After restarting, I tried again, hoping to finish the transfer before addressing the blue screen issue. Unfortunately, it blue screened halfway again. I then suspected the hard drive and downgraded the Intel RST driver, thinking if downgrading didn't help, the SSD might be failing. After downgrading, I tried again with trepidation, and... it blue screened again...

This time, I suspected QQ or WiFi, as the issue occurred when using QQ to receive large files. I uninstalled QQ and used Thunder to download a large file, and sure enough, it crashed again...

![](/images/20180620_02.png)

Having already downgraded the WiFi driver and not previously encountering issues, could it really be a hardware problem? At this point, I was considering giving up on the PC and checking MBP prices on JD.com...

However, the high price of the MBP brought me back to my senses. I decided to give it one last try and continue troubleshooting.

Since my suspicions were incorrect, I turned to science, installing WinDbg and BlueScreenView to analyze the dump files (details omitted, refer to related resources at the end).

![BlueScreenView showing the machine blue screening at an alarming frequency](/images/20180620_03.jpeg)

BlueScreenView didn't reveal much, leaving WinDbg as my last hope.

![](/images/20180620_04.jpeg)

Fortunately, WinDbg was very helpful. Analyzing several dump files from different times, it suggested the issue might be caused by the tdx.sys file.

![](/images/20180620_05.png)

tdx stands for TDI Translation Driver, with TDI meaning Transport Driver Interface, confirming the issue was network-related. This matched the pattern of blue screens occurring during large network file transfers. Then, I saw another message:

> WARNING: Unable to verify timestamp for QMTgpNetFlow764.sys

What is this QMTgpNetFlow764.sys? It seemed like a third-party file from the prefix, so I Googled it.

# The Truth Unveiled

Googling QMTgpNetFlow764.sys finally cleared things up.

![Someone had already discovered the secret of QMTgpNetFlow764.sys causing blue screen issues](/images/20180620_06.png)

According to online analyses (see related resources at the end), these five files came from Tencent's gaming platform WeGame. I uninstalled Tencent's games and rebooted to delete the five QMT-prefixed files in the C:\Windows\system32\drivers directory. Since then (about half a month), I haven't experienced any blue screens, proving that Tencent's WeGame platform was the main cause of the blue screens.

![The culprits](/images/20180620_07.png)

# Related Resources

BlueScreenView download: [https://www.nirsoft.net/utils/blue_screen_view.html](https://www.nirsoft.net/utils/blue_screen_view.html)

WinDbg download: [https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools)

WinDbg usage guide: [https://jingyan.baidu.com/article/9f7e7ec0b0aea36f281554df.html](https://jingyan.baidu.com/article/9f7e7ec0b0aea36f281554df.html)

Zhihu user [Weasley Frank](https://www.zhihu.com/people/weasley-frank)'s article [TGP/WeGame Driver Causes WSL Network Service Issues](https://zhuanlan.zhihu.com/p/33723838) provides a simple analysis of this issue.