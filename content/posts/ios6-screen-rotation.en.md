---
date: "2013-05-21T12:26:00+00:00"
title: "iOS6 Screen Rotation Issue"
categories:
  - Mobile
---

When creating xib files using the iOS6 SDK, AutoLayout is enabled by default. AutoLayout is a new feature introduced in iOS6 that allows for automatic layout through relative positioning, adapting to various screen resolutions (as iOS device resolutions are likely to become more diverse).  
If a project using AutoLayout is run on systems below iOS6, the program will encounter errors. Therefore, by disabling the AutoLayout option in all xib files and running the project again, it was found that projects originally set to display in landscape mode had switched to portrait mode, rendering all landscape settings ineffective.  
The solution is to add the following code in the Controller where landscape mode is needed. It's best to set `self.window` as a RootViewController and then add the following code in the RootViewController:

	// Screen rotation for iOS5
	- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
	    return UIInterfaceOrientationIsLandscape(interfaceOrientation);
	}
	
	// Screen rotation for iOS6
	-(BOOL)shouldAutorotate {
	    return YES;
	}