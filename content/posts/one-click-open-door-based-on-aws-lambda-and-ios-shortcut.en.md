---
date: "2021-10-19T22:30:00+00:00"
title: "Using AWS Lambda and iOS Shortcuts for One-Tap Access to Community Gates"
categories:
  - Python
---

The residential community where I live uses a smart access control system called "Watchful Domain (守望领域)" which allows opening community and unit gates via a mobile app. However, using the app to open gates involves several steps: open the app → navigate to the gate control interface → find the gate you want to open → tap to open.

<center><img style="margin: 0 10px" src="/images/20211019_01.png" width="200"/><img style="margin: 0 10px" src="/images/20211019_02.png" width="200"/><img style="margin: 0 10px" src="/images/20211019_03.png" width="200"/></center>

Moreover, unlocking the phone with a mask on requires entering a password, making the process quite time-consuming. Often, I find myself standing at the community or unit entrance for a while. At one point, I even got into the habit of carrying a physical access card, which is much quicker for opening gates.

Recently, I started forgetting to bring my access card again. Frustrated, I discovered that iOS allows swiping right on the lock screen to access the Spotlight interface without unlocking the phone. This interface can add shortcuts. If I could write a shortcut to call the Watchful Domain (守望领域) app's API to open gates, I could achieve one-tap gate access without unlocking the phone.

<center><img src="/images/20211019_04.gif" width="300"/></center>

# Finding the API

First, I needed to find the API called by the app using software like Charles. I won't go into the details of configuring Charles to view app requests; a quick Google search will yield many tutorials. Looking directly at the results from Charles, you can see that api.lookdoor.cn is the API domain requested by the software.

![](/images/20211019_05.png)

The app sends numerous requests, but by comparing operations and requests, you can see that the API called to send the open gate command is: /func/hjapp/house/v1/pushOpenDoorBySn.json?equipmentId=xxxxxx.

Upon examining this request, it's clear that equipmentId refers to the gate's ID, and the interface uses cookies for authentication. By including the cookie, you can simulate the open gate command.

# First Attempt

Open the iOS Shortcuts app and create a new shortcut. The app uses a POST request to call the API, so search for the "Get contents of" action to send a POST request.

Use Charles to find the URL for the gate you want to open, select POST as the method, and enter the cookie in the headers for authentication. You can copy the content directly from Charles. Try running it, and it works!

<center><img src="/images/20211019_06.jpeg" width="300"/></center>

Next, add this shortcut to the Spotlight interface. Swipe right on the lock screen and tap once to achieve one-tap gate access, which is indeed more time-saving and efficient compared to the four or five steps of opening the app. I took the newly configured shortcut to work, and when I returned to the community, I wanted to try the one-tap gate opening, but I got stuck at the entrance again. The shortcut that worked fine in the morning suddenly failed, and upon checking, the API reported a login timeout, possibly due to an expired SESSION_ID in the cookie.

<center><img src="/images/20211019_07.jpeg" width="300"/></center>

# Analyzing the Login Process

Using Charles to capture packets again and analyze the login-related APIs, I found these two:

- /func/hjapp/user/v2/getPasswordAndKey.json: API to get the AES Key
- /func/hjapp/user/v2/login.json?password=xxxxxx: Login API

By analyzing, I can represent this part of the interaction logic with a sequence diagram:

![](/images/20211019_08.png)

The login process is clear, but the configuration for encrypting the password with AES_KEY is still unclear. I used a tool to try decrypting with the ciphertext and AES_KEY: [http://tool.chacuo.net/cryptaes](http://tool.chacuo.net/cryptaes)

![](/images/20211019_09.png)

Enter the key and ciphertext, and try decrypting with various configurations. When the content can be decrypted, it proves we've found the encryption configuration. You can see BlockSize=128, the padder used is pkcs7padding, and the encryption mode is ECB. The decrypted characters are not our password; they look like they've been MD5 hashed. Using echo -n xxxxxx | md5sum to hash the password with MD5 matches. It seems the server verifies the password after a single MD5 hash.

![](/images/20211019_10.png)

At this point, the login logic is clear, but iOS Shortcuts cannot perform AES encryption, making it impossible to achieve gate opening solely through shortcuts. A backend service is needed to compute the ciphertext. Since setting up a service is unavoidable, why not place the entire login and gate opening process on the service? This way, the iOS shortcut only needs one request to complete the gate opening action.

Considering the login and gate opening logic is simple, involving just three HTTP requests and AES encryption, setting it up from scratch on a bare server is cumbersome and costly. It requires applying for a virtual machine, deploying an HTTP server, a web app, and applying for an SSL certificate. Not only does the initial setup take a day or two, but maintaining the machine and certificate also requires significant time and cost.

Ideally, there would be a service that can directly host a piece of Python code. The first service that comes to mind is Leancloud, a Serverless service provider. However, during practical use, I found that due to policy requirements, Leancloud no longer provides domain names, and binding your domain requires filing. This means I can only choose an overseas Serverless service provider. After some consideration, AWS Lambda seems to meet the requirements, so let's give it a try.

# Using AWS Lambda to Set Up the Service

AWS Lambda is a Serverless service that can directly host a function, saving the hassle of configuring services and infrastructure. Setting up a Python Serverless service requires these steps:

- Create a function and write the code
- Add an API Gateway Trigger to ensure the function can be called via HTTP requests
- Configure the function's runtime environment by adding a layer that packages the cryptography needed for AES encryption and requests needed for HTTP requests

## 1. Function Code

First, the code needs to be written. Fill in your phone number, MD5 hashed password, and device ID (which can be obtained using Charles), and paste it into the Lambda online editor.

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

The code first obtains the AES_KEY and SESSION_ID via an API, then encrypts the password using the AES_KEY. Next, it calls the login interface to bind the obtained SESSION_ID to the current account, and finally sends the open gate command based on the device ID (gate ID) passed in the request.

Click Deploy to deploy, then run a test. A timeout error will occur because the default memory size for the Lambda function executor is 128MB, and the timeout is 3 seconds. On the configuration page, increase the memory size and set the timeout to 10 seconds.

![](/images/20211019_11.png)

## 2. Add API Gateway Trigger

A Lambda function can be triggered in various ways. Since we want to call it via HTTP requests using shortcuts, add an API Gateway Trigger. After adding, a URL will be automatically generated for the function, allowing direct calls to the function via this URL.

![](/images/20211019_12.png)

## 3. Add a Layer with Dependencies

The code uses two third-party libraries, requests and cryptography. Lambda does not support installing these dependencies directly with pip; instead, we need to package the dependencies into a zip file and upload it as a layer, adding it to the function image. Note that the Lambda function execution environment is Linux, so the cryptography library needs to be packaged in its Linux version to be used properly.

Since I use a Mac daily, I applied for an Ubuntu 20 EC2 instance on AWS. After logging into the instance, use the following commands to install dependencies and package them into a zip file:

```python
mkdir python
pip install -t python cryptography
pip install -t python requests
zip -r python/*
```

Create a new Layer on AWS and upload the generated python.zip to the Layer. Try accessing the written Lambda function via the URL, and you can see the open gate command has been successfully issued.

![](/images/20211019_13.png)

# Configuring iOS Shortcuts

Open the iOS Shortcuts app and create a new shortcut. Search for the "Get contents of" action, enter the Lambda function's URL and the gate's ID. Since the API Gateway is not configured with authentication, other parameters can be left as default. If there are security concerns, you can implement a simple token authentication or add JWT authentication provided by Lambda. Click to execute, and the interface returns success, proving the entire process has been completed. You can now use this shortcut to open the gate for yourself and delivery personnel.

<center><img src="/images/20211019_14.png" width="300"/></center>

# Summary

Initially, I intended to achieve one-tap gate access by customizing an iOS shortcut. However, to achieve automatic SESSION_ID updates, I had to set up a backend service using AWS Lambda to simulate the app's behavior. Fortunately, AWS Lambda provides a low-cost solution, including setting up the service and configuring the SSL certificate, which can be done at almost zero cost. The free tier policy also allows this service to run long-term without incurring any actual expenses.
