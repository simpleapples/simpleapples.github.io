---
date: "2014-09-19T16:40:00+00:00"
title: "Exploring Push Notification Registration Failures in iOS8"
categories:
  - Mobile
---

Apple officially released iOS8 on September 18th. Upon updating, I discovered that my app could not launch on iOS8. The Console displayed the following message:

```
2014-09-19 16:26:20.369 demo[379:30506] registerForRemoteNotificationTypes: is not supported in iOS 8.0 and later.
```

Upon checking the documentation, I found that the method `registerForRemoteNotificationTypes` used for registering push notifications has been deprecated in iOS8. The documentation states:

![Alt text](/images/ios8-registerForRemoteNotificationTypes.png)

Following the documentation's guidance, I replaced it with the `registerForRemoteNotifications` method, which does not accept any parameters. However, this led to a new issue: **the app could successfully register on devices where it was already installed, but failed to register on newly installed iOS8 devices**. Neither `application:didRegisterForRemoteNotificationsWithDeviceToken:` nor `application:didFailToRegisterForRemoteNotificationsWithError:` responded, and on devices where registration was successful, push notifications were received without sound alerts. Further review of the documentation revealed the following:

```
If you want your app’s push notifications to display alerts, play sounds, or perform other user-facing actions, you must call the registerUserNotificationSettings: method to request the types of notifications you want to use.
```

In other words, to use push services, you also need to call the `registerUserNotificationSettings` method, which, like the `registerForRemoteNotificationTypes` method in iOS7, accepts parameters. Why did iOS8 split one method into two? The documentation for `registerForRemoteNotifications` includes this statement:

```
Call this method to initiate the registration process with Apple Push Service. If registration succeeds, the app calls your app delegate object’s application:didRegisterForRemoteNotificationsWithDeviceToken: method and passes it a device token.
```

Apple might have considered that some apps register for notifications just to obtain the deviceToken, so they separated the deviceToken acquisition into its own method. To receive push notifications, you must call another method, thereby refining the logic to accommodate different development needs. However, during real device testing on a freshly reset iPhone 5c running iOS8, calling the `registerForRemoteNotifications` method did not trigger any success or failure callbacks, contrary to Apple's documentation, suggesting there might be a bug in the SDK.

Below is the code for registering push notifications compatible with both iOS7 and iOS8:

```objective-c
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
