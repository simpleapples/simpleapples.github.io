---
date: "2013-08-04T12:36:00+00:00"
title: "在Linux上搭建Actionscript开发环境"
categories:
  - Mac&Linux
---

Actionscript 的开发通常使用 Flash Pro 和 Flash Builder 完成，但这两款软件都没有 Linux 版本，在 Linux 下我们可以自己手动搭建一个 Actionscript 的开发环境。  
Actionscript 的开发环境主要有三个方面，分别是 IDE、SDK 和 Flash Player Debugger。

### IDE

Adobe 为 Actionscript 的开发专门提供了 Flash Builder，Flash Builder 是基于 Eclipse 开发的，而 Eclipse 提供了 Linux 版本，所以我们只要在 Eclipse 上安装 Actionscript 插件就可以在 Linux 上实现 Flash Builder 的功能。  
首先在 Eclipse 官网下载 Eclipse IDE，目前的最新版为 4.3。安装过程不再赘述。Eclipse 的运行需要 Java 环境，没有预装 Java 的 Linux 发行版用户可以访问 Oracle 网站下载对应安装包。  
Eclipse 安装完成后，就要安装 Flash Builder 的插件了，官方没有为 Linux 提供插件，所以我们使用一个名为 fb4linux 的开源 Flash Builder 4.5 的 Lniux 插件，项目地址：[http://code.google.com/p/fb4linux/](http://code.google.com/p/fb4linux/)。访问该地址下载 FB4.5ForLinuxaa 和 FB4.5ForLinuxab 两个安装包。下载完成后使用命令`cat FB45ForLinux* >FB45ForLinux.tar.bz2`将两个包和成为一个压缩包，并将其解压。  
接下来在 Eclipse 中安装 FB45ForLinux 插件，在 Eclipse 中选择 Help->Install New Software，点击 Add，在弹出窗口中选择 Local，定位到 FB45Forinux.tar.bz2 解压后的目录后，点击 OK，此时列表中并没有出现可以安装的插件，将 Group items by category 选项去掉，即可显示出可安装的软件。全选所有可安装的项目，点击 Next 进行安装。  
插件安装完成后，IDE 部分的配置就结束了。接下来是 SDK 的安装。

### SDK

SDK 的配置和在 Windows 下基本一样，首先在 Adobe 或 Apache 官网上下载 Flex SDK 安装包，将包解压，在 Eclipse 中选择 Window->Preference->Flash Builder->Installed Flex SDKs，点击 Add 添加解压好的 SDK 目录。

### Flash Player Debugger

Flash Player 的 Debugger 版本的安装最为复杂，Adobe 已经停止对 Linux 平台 Flash Player 的开发，目前 Linux 平台最新版的 Flash Player 是 11.2。所以 Debug 版的 Flash Player 最新版也是 11.2，Adobe 在[http://www.adobe.com/support/flashplayer/downloads.html](http://www.adobe.com/support/flashplayer/downloads.html)上提供了 Linux 版的下载。  
这里需要注意的是，Adobe 提供的 Debug 版 Flash Player 只有 32 位版本，而 64 的 Linux 中的 Firefox 是无法直接使用该插件的。  
在 64 位 Firefox 下使用 Flash Player debugger，需要通过 nspluginwrapper 将其转换为可在 64 位 Firefox 下使用的插件。使用 apt-get 或 yum 等安装 nspluginwrapper，并将 Flash Player debugger 压缩包中的 libflashplugin.so 拷贝到`/usr/lib/mozilla/plugin`下，启动 Firefox，nspluginwrapper 会自动将 libflashplugin.so 转换为 64 位插件，保存在`/usr/lib64/mozilla/plugin-wrapped`下。打开 Firefox 在地址栏中输入`about:plugins`，查看 flash player 是否安装正确。  
在 Eclipse 中新建一个 Actionscript Project，编译运行，如果能够编译并 debug，表明配置正确，如果 Firefox 出现播放 Flash 就崩溃的情况，可能由于转换后的 Flash Player 造成的，Firefox 默认开启了插件的防崩溃机制，导致 debug 版本崩溃。在 Firefox 地址栏中输入`about:config`搜索`dom.ipc.plugins.enabled`，将其值设置为 false，重启 Firefox，Flash Player debugger 即可正常运行。

![Alt text](/images/linux-as-env.png)

至此，Linux 上 Actionscript 开发环境就搭建完成了。
