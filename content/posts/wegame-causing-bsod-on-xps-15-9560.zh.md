---
date: "2018-06-20T14:00:00+00:00"
title: "大毒瘤！卸载WeGame解决XPS 15蓝屏问题"
categories:
  - Tech
---

# 潜伏期

去年 4 月底买了一台美版 XPS 15 9560，用了几个月之后就会偶尔出现蓝屏问题，由于之前就在论坛上看到很多吐槽 XPS 品控的帖子，以为自己也中了枪，好在蓝屏也不频繁，不影响使用也就没管。

# 上升期

进入今年 5 月，升级了 Win10 1803 后（基本上软件有更新我都会第一时间升级，体验最新的改进），蓝屏的次数开始多了起来，开始变得影响使用，于是开始着手查找问题。

由于心急，并没有看转储文件，而是直接 Google 了 XPS 15 的蓝屏问题，希望能尽快找到方案。很快发现具有类似问题的人不在少数，也有很大一部分人以此说 XPS 15 品控不好，看了很多内容后，把怀疑的方向放在了驱动层面（Dell 有一个 Dell Update 软件，一有更新提示我就会更新驱动），于是从更新频率最高的显卡驱动入手，降级显卡驱动到上一个版本，然而并没有什么用。于是又降级了 Wifi 驱动，因为 Wifi 驱动也是最近更新的，并且 XPS 15 的 Killer 显卡兼容性似乎没有那么好。

![XPS 15的驱动列表，可以看到Wifi和显卡驱动都是最近发布的](/images/20180620_01.png)

降级完驱动之后，电脑进入了短暂的回光返照阶段，用了几个小时都没有蓝屏，然而紧接着更加不幸的问题就要发生了。

# 爆发期

用 QQ 接收一个大文件，大概 1G，进行到一半的时候忽然蓝屏，重启后重新接收，准备传完之后再解决蓝屏问题，然而不幸的是传了一半又蓝屏了... 这时我把怀疑的方向转向了硬盘，于是降级了 Intel RST 驱动，心想降级要是没用的话，有可能是 SSD 跪了... 降级后怀着忐忑的心情再次重试，竟然...又蓝屏了...

这次把怀疑的方向转到了 QQ 或者 Wifi 上，毕竟是一用 QQ 接收大文件就出问题，那么不是 QQ 就是 Wifi 了，于是卸载 QQ，用迅雷下载一个大文件，果不其然，又跪了...

![](/images/20180620_02.png)

然而已经降级了 Wifi 驱动，之前也一直没有什么问题，难道真的是硬件出了问题？这个时候，我内心已经有点放弃 PC，转而在京东上看 MBP 的价格了...

然而 MBP 高企的售价让我冷静了下来，回来死马当活马医，继续找问题吧。

既然自己怀疑的方向都不对，只能信仰科学了，安装了 WinDbg 和 BlueScreenView 这两款软件来查看和分析转储文件（具体过程不再赘述，可以参考文末的相关资源）。

![从BlueScreenView里可以看到，机器以近乎疯狂的频率蓝屏](/images/20180620_03.jpeg)

从 BlueScreenView 里并没有看到太多信息，现在只剩下 WinDbg 这一根救命稻草了。

![](/images/20180620_04.jpeg)

不过好在 WinDbg 非常给力，分析了几个不同时间的转储文件，都提示问题可能是由 tdx.sys 文件造成的。

![](/images/20180620_05.png)

tdx 是 TDI Translation Driver 的意思，TDI 是传输层驱动接口的意思，那么可以肯定问题来自于网络，这也印证了每次使用网络传输大文件就会蓝屏的现象。紧接着，看到了另外一段话：

> WARNING: Unable to verify timestamp for QMTgpNetFlow764.sys

这个 QMTgpNetFlow764.sys 又是什么，看前缀似乎像第三方的文件，先 Google 一下。

# 真相大白

Google 了一下这个 QMTgpNetFlow764.sys，终于拨云见日。

![原来早有人发现了QMTgpNetFlow764.sys引发蓝屏问题的秘密](/images/20180620_06.png)

根据网友们的分析（具体可以查看文末的相关资源），这 5 个文件来自于腾讯的游戏平台 WeGame，于是卸载了腾讯系的游戏，并且重启删除了 C:\Windows\system32\drivers 目录下以 QMT 开头的 5 个文件，没关机使用至今（大约半个月）再也没有出现过蓝屏的情况，至此可以证明，腾讯 WeGame 平台是引起蓝屏的主要原因。

![毒瘤们](/images/20180620_07.png)

# 相关资源

BlueScreenView 下载地址：[https://www.nirsoft.net/utils/blue_screen_view.html](https://www.nirsoft.net/utils/blue_screen_view.html)

WinDbg 下载地址：[https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools)

WinDbg 使用说明：[https://jingyan.baidu.com/article/9f7e7ec0b0aea36f281554df.html](https://jingyan.baidu.com/article/9f7e7ec0b0aea36f281554df.html)

知乎用户[Weasley Frank](https://www.zhihu.com/people/weasley-frank)的专栏文章[TGP/WeGame 驱动导致 WSL 网络服务异常
](https://zhuanlan.zhihu.com/p/33723838)对这个问题进行了简单分析
