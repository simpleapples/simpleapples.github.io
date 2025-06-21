---
date: "2015-03-13T11:03:00+00:00"
title: "在viewDidAppear中PushViewController失败的问题"
categories:
  - Mobile
---

需要在 ViewController(FirstViewController)的 viewDidAppear 中 Push 另一个 ViewController()SecondViewController)，于是使用如下代码：

    - (void)viewDidAppear:(BOOL)animated
    {
    	[super viewDidAppear:animated];

    	UIViewController *secondViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"secondViewController"];
    	[self.navigationController pushViewController:secondViewController animated:YES];
    }

在 iOS8 中，这段代码工作良好，当 FirstViewController 出现时，由于立刻 Push 了 SecondViewController，即使 animated 参数是 YES，Push 的动画都没有显示出来。但是在 iOS7 中却出现了不一样的情况，pushViewController 方法似乎没有执行，SecondViewController 也没有被推出。打断点可以发现 pushViewController 方法是被执行了的，但是界面上没有任何效果。

由于 pushViewController 方法是在 viewDidAppear 中被调用的，会不会是因为 viewDidAppear 时 FirstViewController 还有什么 UI 上的动作没有处理完，导致立即调用 pushViewController 失败？那么将 pushViewController 放入 dispatch_async 中应该就能解决这个问题。使用如下代码实现：

    - (void)viewDidAppear:(BOOL)animated
    {
    	[super viewDidAppear:animated];

    	UIViewController *secondViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"secondViewController"];
    	dispatch_async(dispatch_get_main_queue(), ^{
    		[self.navigationController pushViewController:secondViewController animated:YES];

});
}

使用 GCD 后，SecondViewController 被成功的 Push 了出来。虽然不能确定，但是也在一定程度上印证了上面的猜测。
