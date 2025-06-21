---
date: "2014-03-27T17:10:00+00:00"
title: "Differences Between Air SDK and Flex SDK"
categories:
  - Actionscript
---

Recently, I upgraded the SDK for AS development from Flex SDK 4.9.1 to Air SDK 4.0, which caused a previously written FLV player to stop playing videos. Eventually, I discovered the bug was due to a variable name in a method being the same as a get method in the class. The situation is similar to what is shown in the image below:

![Alt text](/images/air-and-flex-sdk.png)

In the image, the variable `time` and the get method `time` have the same name. The compiler handles this naming conflict differently in Flex SDK and Air SDK.

Under Flex SDK, the context determines that the second `time` in `var time:int = time;` is treated as the get method. However, in Air SDK, both instances of `time` in this line are considered the same variable, meaning it is self-assigned. Since an `int` type is initialized to 0, the output using Air SDK is 0, while using Flex SDK, the output is 1000.

It seems Air SDK is not as smart as Flex SDK :)
