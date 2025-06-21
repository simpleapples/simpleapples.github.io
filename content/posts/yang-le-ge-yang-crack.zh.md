---
date: "2022-09-20T18:52:00+00:00"
title: "羊了个羊科技通关攻略"
categories:
  - Life
---

最近羊了个羊比较火，但是难度非常高，打了几天几十盘都通不过，所以犯了职业病，想看看有没有科技手段，实践有效后整理出来方便大家科技通关。

# 原理

科技通关的原理比较简单，游戏每天都有两幅地图，第一个地图是练手的可以无脑通过，第二个是难度爆表的版本，所以只要能够把第二个地图改成第一个，就可以实现通关。

# 准备工作

实现科技通关需要一个 Web 调试代理 App，在 iOS 上可以用 HTTP Catcher（需要内购），Storm Sniffer（三天试用），Android 上也可以找类似的软件。以 HTTP Catcher 为例，安装好之后需要安装并启用 Root 证书，以实现 HTTPS 解密。

# 步骤

首先需要启动 HTTP Catcher，打开羊了个羊进入游戏开始挑战，然后返回 HTTP Catcher，筛选 JSON 类型的请求，找到包含 map_info_ex 的请求。

<center>{{< figure src="/images/20220920_01.png" width="50%">}}</center>

点进这个请求里的 Response，可以看到返回内容里有个 map_md5 的列表，里面有两个 md5 值，分别对应第一个地图和第二个地图，我们要做的就是把返回值里第二个地图的 md5 替换成第一个的。

<center>{{< figure src="/images/20220920_02.png" width="50%">}}</center>

接下来返回上一个界面，左滑选择更多，新建重写，在弹出的界面中新增规则。

<center>{{< figure src="/images/20220920_03.png" width="50%">}}</center>

按下图的选择 Response 和 Body，将第二张地图的 md5（可以提前复制好）填入 Find，将第二张地图的 md5 填入 Replace，然后一路保存。

<center>{{< figure src="/images/20220920_04.png" width="50%">}}</center>

接下来重新启动 HTTP Catcher，回到羊了个羊重新开始游戏，第二关就变成和第一关一样简单的地图了。

<center>{{< figure src="/images/20220920_05.png" width="50%">}}</center>
