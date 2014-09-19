---
layout: post
title: "iOS8注册推送失败的探究"
date: 2014-09-19 16:40
comments: true
categories: Mobile
---

Apple在9月18日正式发布了iOS8，在收到更新的同时，也发现自己的应用在iOS8下无法启动。
并且在Console中收到如下提示：

```
2014-09-19 16:26:20.369 demo[379:30506] registerForRemoteNotificationTypes: is not supported in iOS 8.0 and later.
```

查询文档可以知道，在iOS8中注册推送的方法```registerForRemoteNotificationTypes```已经被废弃，文档中是这样描述的：

->![Alt text](/upload/ios8-registerForRemoteNotificationTypes.png)<-

按照文档中的提示，使用```registerForRemoteNotifications```方法代替，这个方法不接受参数。紧接着问题就来了，**程序在安装过这个应用的iOS8机器上可以成功注册，而在新安装的iOS8机器上则无法注册**，```application:didRegisterForRemoteNotificationsWithDeviceToken:```和```application:didFailToRegisterForRemoteNotificationsWithError:```都无法响应，并且在成功注册的机器上，收到的推送消息也没有声音提示。再次查看文档后发现这么一段话：

```
If you want your app’s push notifications to display alerts, play sounds, or perform other user-facing actions, you must call the registerUserNotificationSettings: method to request the types of notifications you want to use.
```

换句话说，如果要使用推送服务，还需要再调用```registerUserNotificationSettings```方法，而这个方法是和iOS7上的```registerForRemoteNotificationTypes```方法一样接受参数的。为什么iOS8下要把一个方法变成两个方法呢？```registerForRemoteNotifications```方法的文档中有这么一句话：

```
Call this method to initiate the registration process with Apple Push Service. If registration succeeds, the app calls your app delegate object’s application:didRegisterForRemoteNotificationsWithDeviceToken: method and passes it a device token.
```

苹果可能考虑到一些应用注册提醒可能只是为了获取deviceToken，所以将获取deviceToken单独提成一个方法，而要接收推送还需要单独调用别的方法，这样就细化了逻辑，方便不用的开发需求。不过在真机调试中，一台刚重置过的搭载iOS8系统的iPhone5c，调用registerForRemoteNotifications方法后，并没有收到任何失败或成功的回调，和Apple文档中描述的不符，怀疑是SDK在这部分也有bug。

下面贴一下兼容iOS7和iOS8的注册推送代码：

```
#define IS_OS_8_OR_LATER ([[[UIDevice currentDevice] systemVersion] floatValue] >= 8.0)
if (IS_OS_8_OR_LATER) {
    [[UIApplication sharedApplication] registerForRemoteNotifications];
    UIUserNotificationSettings *settings = [UIUserNotificationSettings settingsForTypes: (UIRemoteNotificationTypeBadge | UIRemoteNotificationTypeAlert | UIRemoteNotificationTypeSound) categories:nil];
    [[UIApplication sharedApplication] registerUserNotificationSettings:settings];
} else {
    [application registerForRemoteNotificationTypes:
     UIRemoteNotificationTypeBadge |
     UIRemoteNotificationTypeAlert |
     UIRemoteNotificationTypeSound];
}
```