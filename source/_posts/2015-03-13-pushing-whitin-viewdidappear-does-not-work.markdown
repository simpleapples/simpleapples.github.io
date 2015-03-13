---
layout: post
title: "在viewDidAppear中PushViewController失败的问题"
date: 2015-03-13 11:03
comments: true
categories: Mobile
---

需要在ViewController(FirstViewController)的viewDidAppear中Push另一个ViewController()SecondViewController)，于是使用如下代码：

	- (void)viewDidAppear:(BOOL)animated 
	{
    	[super viewDidAppear:animated];
    
    	UIViewController *secondViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"secondViewController"];
    	[self.navigationController pushViewController:secondViewController animated:YES];
    }
    
在iOS8中，这段代码工作良好，当FirstViewController出现时，由于立刻Push了SecondViewController，即使animated参数是YES，Push的动画都没有显示出来。但是在iOS7中却出现了不一样的情况，pushViewController方法似乎没有执行，SecondViewController也没有被推出。打断点可以发现pushViewController方法是被执行了的，但是界面上没有任何效果。

由于pushViewController方法是在viewDidAppear中被调用的，会不会是因为viewDidAppear时FirstViewController还有什么UI上的动作没有处理完，导致立即调用pushViewController失败？那么将pushViewController放入dispatch_async中应该就能解决这个问题。使用如下代码实现：

	- (void)viewDidAppear:(BOOL)animated 
	{
    	[super viewDidAppear:animated];
    
    	UIViewController *secondViewController = [self.storyboard instantiateViewControllerWithIdentifier:@"secondViewController"];
    	dispatch_async(dispatch_get_main_queue(), ^{
    		[self.navigationController pushViewController:secondViewController animated:YES];
   		});
    }
    
使用GCD后，SecondViewController被成功的Push了出来。虽然不能确定，但是也在一定程度上印证了上面的猜测。