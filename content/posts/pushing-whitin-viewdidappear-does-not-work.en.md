---
date: "2015-03-13T11:03:00+00:00"
title: "Issue with PushViewController in viewDidAppear"
categories:
  - Mobile
---

I needed to push another ViewController (SecondViewController) from the viewDidAppear method of a ViewController (FirstViewController), so I used the following code:

```objective-c
- (void)viewDidAppear:(BOOL)animated 
{
    [super viewDidAppear:animated];

    UIViewController *secondViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"secondViewController"];
    [self.navigationController pushViewController:secondViewController animated:YES];
}
```

In iOS 8, this code works well. When FirstViewController appears, SecondViewController is pushed immediately, and even if the animated parameter is YES, the push animation does not display. However, in iOS 7, the situation is different. It seems that the pushViewController method does not execute, and SecondViewController is not pushed. Breakpoints show that the pushViewController method is indeed executed, but there is no effect on the interface.

Since the pushViewController method is called in viewDidAppear, could it be that there are some UI actions in FirstViewController that are not yet completed, causing the immediate call to pushViewController to fail? If so, placing pushViewController in a dispatch_async block should solve the problem. The following code implements this:

```objective-c
- (void)viewDidAppear:(BOOL)animated 
{
    [super viewDidAppear:animated];

    UIViewController *secondViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"secondViewController"];
    dispatch_async(dispatch_get_main_queue(), ^{
        [self.navigationController pushViewController:secondViewController animated:YES];
    });
}
```

After using GCD, SecondViewController is successfully pushed. Although not certain, this somewhat confirms the above hypothesis.