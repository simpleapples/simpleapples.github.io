---
date: "2014-10-25T13:20:00+00:00"
title: "Perfect Combination of LaunchImage and LaunchScreen in iOS8"
categories:
  - Mobile
---

In iOS8, Apple introduced LaunchScreen.xib to replace the previous LaunchImage as the app's launch interface. Compared to LaunchImage, LaunchScreen.xib is undoubtedly more convenient with AutoLayout, especially as iOS device screen sizes become increasingly diverse. Otherwise, an app compatible with iPhone5 to iPhone6Plus would require four different sizes of LaunchImages.

However, LaunchScreen is only supported in iOS8, so some developers still choose the traditional LaunchImage method. There's also a way to combine LaunchImage and LaunchScreen: using LaunchScreen for larger iPhones (iPhone6 and iPhone6Plus, which both run iOS8) and LaunchImage for iOS7 (since iOS7 phones only include 4-inch and 5.5-inch iPhones, only two images are needed).

First, go to the Target configuration and find App Icons and Launch Images. In Xcode6, LaunchScreen.xib is used by default, while LaunchImage is not.

![Image 1](/images/launch-screen-1.png)

Next, click on Use Assets Catalog. Xcode will then generate a LaunchImage in Images.xcassets. Here, we only need to provide two LaunchImages for the 4-inch Retina display and the 3.5-inch 2x display.

In iOS8, the system will prioritize LaunchScreen as the launch interface, while iOS7, which does not support LaunchScreen, will use the images in LaunchImage as the launch interface.

![Image 2](/images/launch-screen-2.png)

Project running effect in iOS7 simulator (using LaunchImage)

![Image 3](/images/launch-screen-3.png)

Project running effect in iOS8 simulator (using the default LaunchScreen.xib)
