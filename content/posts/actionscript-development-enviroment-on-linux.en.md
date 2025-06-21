---
date: "2013-08-04T12:36:00+00:00"
title: "Setting Up an Actionscript Development Environment on Linux"
categories:
  - Mac&Linux
---

Actionscript development is typically done using Flash Pro and Flash Builder, but neither of these software has a Linux version. On Linux, we can manually set up an Actionscript development environment.  
The Actionscript development environment mainly consists of three components: the IDE, SDK, and Flash Player Debugger.

### IDE

Adobe provides Flash Builder specifically for Actionscript development, which is based on Eclipse. Since Eclipse offers a Linux version, we can achieve Flash Builder functionality on Linux by installing the Actionscript plugin on Eclipse.  
First, download the Eclipse IDE from the Eclipse official website. The latest version is 4.3. The installation process is not detailed here. Eclipse requires a Java environment to run. Users of Linux distributions without pre-installed Java can visit the Oracle website to download the appropriate installation package.  
After installing Eclipse, you need to install the Flash Builder plugin. Since there is no official plugin for Linux, we use an open-source Flash Builder 4.5 Linux plugin called fb4linux. The project can be found at: [http://code.google.com/p/fb4linux/](http://code.google.com/p/fb4linux/). Visit this link to download the FB4.5ForLinuxaa and FB4.5ForLinuxab packages. Once downloaded, use the command `cat FB45ForLinux* >FB45ForLinux.tar.bz2` to combine the two packages into a single compressed file and then extract it.  
Next, install the FB45ForLinux plugin in Eclipse. In Eclipse, go to Help->Install New Software, click Add, and in the pop-up window, select Local. Navigate to the directory where FB45ForLinux.tar.bz2 was extracted, and click OK. If no installable plugins appear in the list, uncheck the Group items by category option to display the available software. Select all available items and click Next to install.  
Once the plugin installation is complete, the IDE configuration is done. Next is the SDK installation.

### SDK

Configuring the SDK is essentially the same as on Windows. First, download the Flex SDK package from the Adobe or Apache website, extract the package, and in Eclipse, go to Window->Preference->Flash Builder->Installed Flex SDKs, click Add to add the extracted SDK directory.

### Flash Player Debugger

Installing the Debugger version of Flash Player is the most complex part. Adobe has stopped developing Flash Player for the Linux platform, and the latest version available for Linux is 11.2. Therefore, the latest Debug version of Flash Player is also 11.2, which Adobe provides for download at [http://www.adobe.com/support/flashplayer/downloads.html](http://www.adobe.com/support/flashplayer/downloads.html).  
It's important to note that Adobe only provides a 32-bit version of the Debug Flash Player, which cannot be directly used by 64-bit Firefox on Linux.  
To use the Flash Player debugger on 64-bit Firefox, you need to convert it into a plugin usable by 64-bit Firefox using nspluginwrapper. Install nspluginwrapper using apt-get or yum, and copy libflashplugin.so from the Flash Player debugger package to `/usr/lib/mozilla/plugin`. Launch Firefox, and nspluginwrapper will automatically convert libflashplugin.so into a 64-bit plugin, saving it in `/usr/lib64/mozilla/plugin-wrapped`. Open Firefox and enter `about:plugins` in the address bar to check if the Flash Player is installed correctly.  
Create a new Actionscript Project in Eclipse, compile and run it. If you can compile and debug, the configuration is correct. If Firefox crashes when playing Flash, it may be due to the converted Flash Player. Firefox has a default crash protection mechanism for plugins, causing the debug version to crash. In the Firefox address bar, enter `about:config`, search for `dom.ipc.plugins.enabled`, set its value to false, restart Firefox, and the Flash Player debugger should run normally.

![Alt text](/images/linux-as-env.png)

With this, the Actionscript development environment on Linux is set up.
