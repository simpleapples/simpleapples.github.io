---
layout: post
title: "在Linux上搭建Actionscript开发环境"
date: 2013-08-04 12:36
comments: true
categories: Mac&Linux
---

Actionscript的开发通常使用Flash Pro和Flash Builder完成，但这两款软件都没有Linux版本，在Linux下我们可以自己手动搭建一个Actionscript的开发环境。  
Actionscript的开发环境主要有三个方面，分别是IDE、SDK和Flash Player Debugger。  
### IDE  ###
Adobe为Actionscript的开发专门提供了Flash Builder，Flash Builder是基于Eclipse开发的，而Eclipse提供了Linux版本，所以我们只要在Eclipse上安装Actionscript插件就可以在Linux上实现Flash Builder的功能。  
首先在Eclipse官网下载Eclipse IDE，目前的最新版为4.3。安装过程不再赘述。Eclipse的运行需要Java环境，没有预装Java的Linux发行版用户可以访问Oracle网站下载对应安装包。  
Eclipse安装完成后，就要安装Flash Builder的插件了，官方没有为Linux提供插件，所以我们使用一个名为fb4linux的开源Flash Builder 4.5的Lniux插件，项目地址：[http://code.google.com/p/fb4linux/](http://code.google.com/p/fb4linux/)。访问该地址下载FB4.5ForLinuxaa和FB4.5ForLinuxab两个安装包。下载完成后使用命令```cat FB45ForLinux* >FB45ForLinux.tar.bz2```将两个包和成为一个压缩包，并将其解压。  
接下来在Eclipse中安装FB45ForLinux插件，在Eclipse中选择Help->Install New Software，点击Add，在弹出窗口中选择Local，定位到FB45Forinux.tar.bz2解压后的目录后，点击OK，此时列表中并没有出现可以安装的插件，将Group items by category选项去掉，即可显示出可安装的软件。全选所有可安装的项目，点击Next进行安装。  
插件安装完成后，IDE部分的配置就结束了。接下来是SDK的安装。  
### SDK ###
SDK的配置和在Windows下基本一样，首先在Adobe或Apache官网上下载Flex SDK安装包，将包解压，在Eclipse中选择Window->Preference->Flash Builder->Installed Flex SDKs，点击Add添加解压好的SDK目录。
### Flash Player Debugger ###
Flash Player 的Debugger版本的安装最为复杂，Adobe已经停止对Linux平台Flash Player的开发，目前Linux平台最新版的Flash Player是11.2。所以Debug版的Flash Player最新版也是11.2，Adobe在[http://www.adobe.com/support/flashplayer/downloads.html](http://www.adobe.com/support/flashplayer/downloads.html)上提供了Linux版的下载。  
这里需要注意的是，Adobe提供的Debug版Flash Player只有32位版本，而64的Linux中的Firefox是无法直接使用该插件的。  
在64位Firefox下使用Flash Player debugger，需要通过nspluginwrapper将其转换为可在64位Firefox下使用的插件。使用apt-get或yum等安装nspluginwrapper，并将Flash Player debugger压缩包中的libflashplugin.so拷贝到```/usr/lib/mozilla/plugin```下，启动Firefox，nspluginwrapper会自动将libflashplugin.so转换为64位插件，保存在```/usr/lib64/mozilla/plugin-wrapped```下。打开Firefox在地址栏中输入```about:plugins```，查看flash player是否安装正确。  
在Eclipse中新建一个Actionscript Project，编译运行，如果能够编译并debug，表明配置正确，如果Firefox出现播放Flash就崩溃的情况，可能由于转换后的Flash Player造成的，Firefox默认开启了插件的防崩溃机制，导致debug版本崩溃。在Firefox地址栏中输入```about:config```搜索```dom.ipc.plugins.enabled```，将其值设置为false，重启Firefox，Flash Player debugger即可正常运行。

->![Alt text](/upload/linux-as-env.png)<-

至此，Linux上Actionscript开发环境就搭建完成了。