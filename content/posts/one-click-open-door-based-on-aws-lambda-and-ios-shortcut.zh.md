---
date: "2021-10-19T22:30:00+00:00"
title: "利用AWS Lambda和iOS捷径实现手机一键开小区门禁"
categories:
  - Python
---

我住的小区使用了一个叫守望领域的智能门禁系统，可以通过手机 App 开小区门禁和单元门，但是用 App 开门需要经过四五步：打开 App→ 进入开门界面 → 找到需要开的门 → 点击开门。

<center><img style="margin: 0 10px" src="/images/20211019_01.png" width="200"/><img style="margin: 0 10px" src="/images/20211019_02.png" width="200"/><img style="margin: 0 10px" src="/images/20211019_03.png" width="200"/></center>

加上戴口罩时候解锁手机需要输入密码，导致整个流程非常耗时，经常需要站在小区门口和单元门口操作半天，有一段时间我甚至养成了携带实体门禁卡的习惯，实体门禁卡开门要快很多。

最近又开始忘带门禁卡，苦恼之余发现 iOS 在锁屏界面右划可以免解锁直接进入 spotlight 界面，这个界面可以添加捷径，如果能写一个捷径去调用守望领域 App 的 API 开门，就可以实现手机免解锁一键开门。

<center><img src="/images/20211019_04.gif" width="300"/></center>

# 查找 API

首先需要通过 Charles 之类的软件查找 App 调用的 API，配置 Charles 查看 App 请求的方式不再赘述，Google 一下可以看到很多教程。直接看结果 Charles 的结果，可以看到 api.lookdoor.cn 是这个软件所请求的 API 域名。

![](/images/20211019_05.png)

打开软件发的请求非常多，经过操作和请求的对比可以看到，发送开门指令调用的 API 是：/func/hjapp/house/v1/pushOpenDoorBySn.json?equipmentId=xxxxxx 这个路径。

详细查看这个请求可以发现，equipmentId 指的就是小区门的 Id，接口使用 cookie 做认证，只要将 cookie 带上就可以模拟开门指令。

# 第一次尝试

打开 iOS 捷径 App，创建一个新捷径，App 调用 API 使用了 POST 请求，搜索 Get contents of 这个动作来实现发送 POST 请求。

通过 Charles 找到要开的门的 URL 填入，Method 选择 POST，Headers 里填入 Cookie 进行认证，内容直接从 Charles 复制就可以，尝试运行，it works!

<center><img src="/images/20211019_06.jpeg" width="300"/></center>

接下来把这个捷径添加到 Spotlight 界面，锁屏界面右划点一下，就可以实现一键开小区门禁，和打开 App 的四五步操作相比，确实省时省力。拿着新配好的捷径去上班，下班回到小区想试一把一键开门，结果又被困到门口了，上午还正常的捷径竟然失效了，打开一看 API 报登录超时，有可能是 Cookie 里的 SESSION_ID 过期了。

<center><img src="/images/20211019_07.jpeg" width="300"/></center>

# 分析登录过程

再次用 Charles 抓包，分析登录相关的 API，会发现主要是这两个：

- /func/hjapp/user/v2/getPasswordAndKey.json：获取 AES Key 的 API
- /func/hjapp/user/v2/login.json?password=xxxxxx：登录 API

通过分析，用时序图来表示这部分的交互逻辑：

![](/images/20211019_08.png)

登录过程清楚了，但是其中使用 AES_KEY 对密码进行加密的配置还是不清楚的，使用一个工具来尝试通过密文和 AES_KEY 来解密：[http://tool.chacuo.net/cryptaes](http://tool.chacuo.net/cryptaes)

![](/images/20211019_09.png)

输入密钥和密文，使用各种配置进行解密，当能够解出内容的时候，证明我们找到了加密的配置，可以看到 BlockSize=128，padder 使用的是 pkcs7padding，加密模式是 ECB。解密出来的字符并不是我们的密码，看着像是 md5 过的，用 echo -n xxxxxx | md5sum 把密码 md5 一下，对上了。看来服务端校验的是单次 md5 后的密码。

![](/images/20211019_10.png)

到这里登录逻辑已经搞清了，但是 iOS 捷径无法实现 AES 加密，单纯依托捷径来实现开门已经不可行了，需要搭建一个后端服务来计算密文。既然躲不过麻烦要搭建服务，不如把登录、开门整个流程都放在服务上，这样 iOS 捷径只需要一个请求就可以完成开门动作了。

考虑到登录开门的逻辑很简单，也就是 3 个 HTTP 请求+AES 加密，直接在裸服务器上从 0 搭建步骤多成本高，要自己申请虚机、部署 HTTP Server、Web App，还需要申请 SSL 证书，不仅初次搭建要搞个一两天，后续对机器和证书的维护也需要大量时间，成本极高。

最好是有服务能直接托管一段 Python 代码，第一时间想到的是 Leancloud，一个 Serverless 服务提供商，但是实操过程中发现，由于政策要求 Leancloud 已经不提供域名了，绑定自己的域名也需要进行备案。这意味着只能选择一家海外 Serverless 服务商，看来看去 AWS Lambda 应该可以满足要求，试一下。

# 使用 AWS Lambda 搭建服务

AWS Lambda 是一个 Serverless 服务，可以直接托管一段函数，省去配置服务和基础设施的麻烦。搭建一个 Python 的 Serverless 服务需要准备这么几件事：

- 新建函数，编写代码
- 添加 API Gateway Trigger，确保函数可以通过 HTTP 请求调用
- 配置函数的运行环境，增加一个层（Layer），这个层里打包进 AES 加密需要的 cryptography 和 HTTP 请求需要的 requests

## 1. 函数代码

首先上代码，需要填写自己的手机号、md5 后的密码、设备 ID（可以用 Charles 获取）等字段，粘贴到 Lambda 的在线编辑器中。

```python
import json
import requests
import base64
import urllib.parse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

PHONE = ''
PASSWORD_MD5 = ''
DEVICE_ID = ''

def encrypt(key, msg):
    cipher = Cipher(algorithms.AES(str.encode(key)), modes.ECB())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    msg = padder.update(str.encode(msg)) + padder.finalize()
    ct = encryptor.update(msg) + encryptor.finalize()
    return base64.b64encode(ct)

def lambda_handler(event, context):
    resp = requests.post('https://api.lookdoor.cn:443/func/hjapp/user/v2/getPasswordAesKey.json?')
    cookie = resp.headers['set-cookie']
    aes_key = resp.json()['data']['aesKey']
    password_encypted = urllib.parse.quote_plus(encrypt(aes_key, PASSWORD_MD5))

    url = f'https://api.lookdoor.cn:443/func/hjapp/user/v2/login.json?password={password_encypted}&deviceId={DEVICE_ID}&loginNumber={PHONE}&equipmentFlag=1'
    requests.post(url, headers={'cookie': cookie})

    equipment_id = event['queryStringParameters']['equipment_id']
    url = f'https://api.lookdoor.cn:443/func/hjapp/house/v1/pushOpenDoorBySn.json?equipmentId={equipment_id}'
    resp = requests.post(url, headers={'cookie': cookie})
    return resp.json()
```

代码首先通过 API 获取 AES_KEY 和 SESSION_ID，然后使用 AES_KEY 对密码进行加密，接下来调用登录接口将获取的 SESSION_ID 绑定到当前账户，接下来根据请求传入的设备 ID（门的 ID）来发送开门指令。

点击 Deploy 部署，然后运行测试，会出现超时的报错，这是因为 Lambda 函数默认的执行器内存大小是 128MB，超时时间是 3s，在配置页面把内存改大一些，超时时间设置为 10s 就可以了。

![](/images/20211019_11.png)

## 2. 添加 API Gateway Trigger

一个 Lambda 函数可以被多种形式触发执行，因为要使用捷径通过 HTTP 请求调用，所以加一个 API Gateway Trigger，添加后会自动为函数生成一个 URL，通过这个 URL 就可以直接调用函数。

![](/images/20211019_12.png)

## 3. 添加包含依赖的 Layer

代码中使用了 requests 和 cryptography 这两个第三方库，Lambda 不支持使用 pip 直接安装这些依赖，而是需要我们在把依赖打成 zip 包上传成为容器的一层 Layer，添加到函数镜像中。需要注意的是，Lambda 函数执行的环境是 Linux，对于 cryptography 这个库需要打包 Linux 版的才可以正常使用。

由于日常使用的是 Mac，所以在 AWS 上申请一台 Ubuntu 20 的 EC2 实例，登录实例后使用如下命令安装依赖，并打包成 zip 文件：

```python
mkdir python
pip install -t python cryptography
pip install -t python requests
zip -r python/*
```

在 AWS 上创建一个新的 Layer，并将生成的 python.zip 上传到 Layer 上。尝试通过 URL 访问写好的 Lambda 函数，可以看到开门指令已经成功下发。

![](/images/20211019_13.png)

# 配置 iOS 捷径

打开 iOS 捷径 App，创建一个新捷径，搜索 Get contents of 这个动作，填入 Lambda 函数的 URL 和门的 ID。由于 API Gateway 并没有配置认证，所以其他参数默认即可。如果有安全方面的顾虑，可以自己实现一个简单的 Token 认证或添加 Lambda 提供的 JWT 认证。点击执行，接口返回成功，证明整个流程已经跑通，以后就可以用这个捷径给自己和外卖小哥开门了。

<center><img src="/images/20211019_14.png" width="300"/></center>

# 总结

一开始本想用自定义一个 iOS 捷径的方式来实现一键开门禁，但为了实现 SESSION_ID 自动更新，不得不基于 AWS Lambda 搭了一个后端服务来模拟 App 的行为，所幸 AWS Lambda 提供了低成本的构建方案，包括搭建服务和配置 SSL 证书都可以几乎 0 成本的完成，免费套餐政策也能让这个服务长期跑着而不产生任何实际花费。
