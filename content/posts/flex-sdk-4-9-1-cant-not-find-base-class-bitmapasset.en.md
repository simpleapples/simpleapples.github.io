---
date: "2013-08-27T12:41:00+00:00"
title: "Issue of Not Finding Base Class BitmapAsset After Upgrading to Flex SDK 4.9.1"
categories:
  - Actionscript
---

A project compiled using the Flex SDK encountered the following error after upgrading the SDK to 4.9.1:

> errors: 1017: The definition of base class BitmapAsset was not found.

After some Googling, I found that others have encountered this issue as well. See more details here: [http://mail-archives.apache.org/mod_mbox/flex-dev/201303.mbox/%3CCD596C86.4E4D3%25aharui@adobe.com%3E](http://mail-archives.apache.org/mod_mbox/flex-dev/201303.mbox/%3CCD596C86.4E4D3%25aharui@adobe.com%3E)

The core.swc in Flex SDK 4.9 is about half the size of the core.swc in 4.8, which suggests that some base classes have been moved out of core.swc, leading to the BitmapAsset not being found.

The solution is to right-click on the project — Properties — Actionscript Build Path — Add SWC, navigate to the framework/libs folder under the SDK installation path, and select framework.swc.

If you expand the framework.swc package, you can see the BitmapAsset class. Adding it to the build path resolves the issue of the base class not being found.

![Alt text](/images/frameworkswc.png)
