---
date: "2016-08-28T23:30:00+00:00"
title: "Attempting to Hack Scores in 'Snake Battle'"
categories:
  - Python
---

Yesterday, a classmate recommended a popular game called "Snake Battle," which has recently climbed to the second spot on the App Store's overall rankings. Whenever I had some free time over the past couple of days, I'd pull out my phone to play a few rounds. However, I hit a bottleneck in the endless mode around 3000 points, so I decided to take a closer look at the game's API purely out of curiosity...

![Image 1](/images/snake-1.png)

## Using Charles to Capture Requests

Since I'm investigating the API, the first step is to examine the URL and parameters of the requests and their responses. Enter the powerful tool, Charles.

![Image 2](/images/snake-2.png)

With Charles, you can clearly see the game's score submission API and its parameters. As for the response, it doesn't seem to be of much use. Next, let's delve into the request details. There are several parameters whose meanings and functions can be easily inferred.

```
device_id: Device ID
game_mode: 1 for endless mode, 2 for timed mode
kill: Number of kills
length: Length of the snake
market: I captured requests from an iOS device, so this is apple
platform: In the captured requests, it's 1, but its exact meaning is unclear
push_channel: Also 1, meaning unclear
push_id: Fixed value 111111111222222223333333344444444, later confirmed by reverse-engineering the APK
sid: Updates with each login
snake_sign: Signature
uid: User ID
version: The version I used is a fixed value of 2.1
```

## Obtaining the Signature Algorithm by Reverse-Engineering the APK

With the parameters clarified, we can now forge requests. However, before doing so, there's a tricky parameter: snake_sign, the request signature. From the content of snake_sign, it seems like a base64-encoded string, but base64 decoding it results in unreadable data. Instead of guessing the signature algorithm, let's consider other approaches.

"Snake Battle" also has an Android version, and the download page provides an APK. So, I downloaded the APK and used [jadx-gui](https://github.com/skylot/jadx) for reverse-engineering. Once opened with jadx-gui, the code is laid bare.

By examining the code, the logic for the snake_sign field's signature becomes clear. First, all parameters in the request are concatenated into a string in ASCII order. Then, prepend `POST& + [URL Path]` to the string. After that, encrypt it using SHA1 with a key that can also be found in the code. The result of the encryption needs to be base64-encoded to produce the final snake_sign field.

```
POST&top_list_v2/update_score&device_id=XXX&game_mode=1&kill=1&length=35&market=apple&platform=1&push_channel=1&push_id=111111111222222223333333344444444&sid=XXX&uid=XXX&version=2.1
```

![Image 3](/images/snake-3.png)

## Some Speculations about "Snake Battle"

With the signature method obtained, I thought I could safely hack the scores. However, I only successfully hacked a score of 4000 points with 160 kills once. I suspect that entering the leaderboard requires manual review. One reason is that it took a few minutes for the hacked score to appear on the leaderboard. Another reason is that after hacking a score of 4000 points with 169 kills, I quickly hacked an absurdly high score, but it never showed up on the leaderboard. No matter how many points I hacked afterward, they never appeared again, leading me to suspect manual blocking.

Additionally, the game's interaction with the API only involves logging in, retrieving user information, fetching the highest leaderboard scores, and submitting scores, so the game isn't truly real-time.

![Image 4](/images/snake-4.png)
