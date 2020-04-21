---
layout: post
title: "用Python批量提取Win10锁屏壁纸"
date: 2018-03-26 22:21
comments: true
categories: Python
---

使用Win10的朋友会发现，每次开机锁屏界面都会有不一样的漂亮图片，这些图片通常选自优秀的摄影作品，十分精美。

![](/upload/20180326_01.jpg)

但是由于系统会自动更换这些图片，所以就算再好看的图片，也许下次开机之后就被替换掉了。

借助Python，我们可以用简单的几行代码，批量提取这些精美的锁屏图片。把喜欢的图片设置成桌面背景，就不用担心被替换掉啦。

# 提取原理

Win10系统会自动下载最新的锁屏壁纸，并将他们保存在一个系统文件夹中，路径是`C:\Users\[用户名]\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets`

![随机命名的锁屏图片](/upload/20180326_02.png)

直接打开这个文件夹，里面会有随机命名的多个文件，每一个文件就是一张图片。但是由于文件没有扩展名，所以并不能预览。为了不搞坏系统文件，并且把这些文件变成可以预览的格式，我们用Python把这些文件复制出来，加上JPG作为扩展名。

# 实现代码

```python
import os, shutil
from datetime import datetime


# 把这个文件所在目录wallpapers文件夹作为保存图片的目录
save_folder = dir_path = os.path.dirname(
	os.path.realpath(__file__)) + '\wallpapers'
# 动态获取系统存放锁屏图片的位置
wallpaper_folder = os.getenv('LOCALAPPDATA') + (
	'\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy'
	'\LocalState\Assets')
# 列出所有的文件
wallpapers = os.listdir(wallpaper_folder)
for wallpaper in wallpapers:
	wallpaper_path = os.path.join(wallpaper_folder, wallpaper)
	# 小于150kb的不是锁屏图片
	if (os.path.getsize(wallpaper_path) / 1024) < 150:
		continue
	wallpaper_name = wallpaper + '.jpg'
	save_path = os.path.join(save_folder, wallpaper_name)
	shutil.copyfile(wallpaper_path, save_path)
	print('Save wallpaper ' + save_path)
```

首先确定系统存放锁屏图片的文件夹位置，由于文件夹位于用户的个人文件夹内，每个用户的用户名是不一样的，所以我们需要通过系统的`LOCALAPPDATA`变量动态的获取路径。代码会把提取出来的图片保存在wallpapers文件夹下，所以代码文件所在的目录没有wallpapers文件夹，需要手工创建一个。

![在代码文件旁新建一个wallpapers文件夹](/upload/20180326_03.png)

执行上面这段Python代码，再打开wallpapers文件夹，就可以看到提取出的锁屏图片了。

![](/upload/20180326_04.png)

