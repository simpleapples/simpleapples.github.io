---
layout: post
title: "使用TestFlight进行应用的Beta测试"
date: 2014-10-30 15:43
comments: true
categories: Mobile
---

TestFlight已经被Apple集成到iTunes Connect中，现在使用TestFlight可以很方便的进行应用的Beta测试。下面就来介绍一下如何使用TestFlight进行测试，已经其中的一些小问题。

首先需要在iTunes Connect中启用TestFlight，可以针对每个App的某一版本，决定是否启用TestFlight。进入iTunes Connect -> My Apps -> 某个App -> Prerelease，在上传的Build右上角，打开TestFlight的开关，接下来就针对这个版本启动了TestFlight。

->![图1](/upload/testflight-1.png)<-

有了可以测试的应用，接下来还要有测试用户，TestFlight测试用户有两种，一种是内测用户InternalTester，最多25个，一种是公测用户ExternalTester，最多1000个，内测用户需要首先成为iTunes Connect User，而公测用户只需要知道他的Apple Id就可。要进行公测需要先经过Apple Review团队的审核。我们以添加一个内测用户为例，进入iTunes Connect -> Users and Roles -> iTunes Connect Users，首先添加一个iTunes Connect User，之所以要添加iTunes Connect User，是因为TestFlight的测试用户必须是一个iTunes Connect User，并且这个用户的角色必须是Admin或者Technical。添加后，用户的邮箱里会收到一封邀请邮件，点击邮件中的链接可以激活成为iTunes Connect User。进入iTunes Connect -> Users and Roles -> TestFlight Beta Testers，激活的iTunes Connect User会出现在这里，选中点击右上角的保存，这个用户就成为一个内测用户了。

->![图2](/upload/testflight-2.png)<-

有了内测用户和测试App，下一步就要将两者关联了，进入iTunes Connect -> My Apps -> 某个App -> Prerelease -> Internal Testers中，这里会显示可用的内测用户，勾选用户并点击右上角的Invite，Apple就会给这个邮箱发送一封邀请邮件。接下来需要在要测试的手机上安装TestFlight，安装好后，TestFlight会自动绑定当前手机的Apple Id登录，这里你会发现TestFlight里并没有出现测试App，经过测试，*必须要在iOS的自带邮件客户端上点击邀请邮件中的链接，才会跳转到TestFlight中安装应用。*这是TestFlight让人非常不爽的一点。你可以将收到的邀请邮件转发到自带的邮件客户端所绑定的邮箱上，让后在自带邮件客户端中点击邀请链接打开TestFlight。

->![图3](/upload/testflight-3.png)<-

点击链接后会自动跳转到TestFlight中，点击Install安装应用，再次进入TestFlight中就可以看到已安装的测试应用了。