---
date: "2014-10-30T15:43:00+00:00"
title: "使用TestFlight进行应用的Beta测试"
categories:
  - Mobile
---

TestFlight 已经被 Apple 集成到 iTunes Connect 中，现在使用 TestFlight 可以很方便的进行应用的 Beta 测试。下面就来介绍一下如何使用 TestFlight 进行测试，已经其中的一些小问题。

首先需要在 iTunes Connect 中启用 TestFlight，可以针对每个 App 的某一版本，决定是否启用 TestFlight。进入 iTunes Connect -> My Apps -> 某个 App -> Prerelease，在上传的 Build 右上角，打开 TestFlight 的开关，接下来就针对这个版本启动了 TestFlight。

![图1](/images/testflight-1.png)

有了可以测试的应用，接下来还要有测试用户，TestFlight 测试用户有两种，一种是内测用户 InternalTester，最多 25 个，一种是公测用户 ExternalTester，最多 1000 个，内测用户需要首先成为 iTunes Connect User，而公测用户只需要知道他的 Apple Id 就可。要进行公测需要先经过 Apple Review 团队的审核。我们以添加一个内测用户为例，进入 iTunes Connect -> Users and Roles -> iTunes Connect Users，首先添加一个 iTunes Connect User，之所以要添加 iTunes Connect User，是因为 TestFlight 的测试用户必须是一个 iTunes Connect User，并且这个用户的角色必须是 Admin 或者 Technical。添加后，用户的邮箱里会收到一封邀请邮件，点击邮件中的链接可以激活成为 iTunes Connect User。进入 iTunes Connect -> Users and Roles -> TestFlight Beta Testers，激活的 iTunes Connect User 会出现在这里，选中点击右上角的保存，这个用户就成为一个内测用户了。

![图2](/images/testflight-2.png)

有了内测用户和测试 App，下一步就要将两者关联了，进入 iTunes Connect -> My Apps -> 某个 App -> Prerelease -> Internal Testers 中，这里会显示可用的内测用户，勾选用户并点击右上角的 Invite，Apple 就会给这个邮箱发送一封邀请邮件。接下来需要在要测试的手机上安装 TestFlight，安装好后，TestFlight 会自动绑定当前手机的 Apple Id 登录，这里你会发现 TestFlight 里并没有出现测试 App，经过测试，*必须要在 iOS 的自带邮件客户端上点击邀请邮件中的链接，才会跳转到 TestFlight 中安装应用。*这是 TestFlight 让人非常不爽的一点。你可以将收到的邀请邮件转发到自带的邮件客户端所绑定的邮箱上，让后在自带邮件客户端中点击邀请链接打开 TestFlight。

![图3](/images/testflight-3.png)

点击链接后会自动跳转到 TestFlight 中，点击 Install 安装应用，再次进入 TestFlight 中就可以看到已安装的测试应用了。
