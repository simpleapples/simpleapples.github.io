---
date: "2013-03-05T12:18:00+00:00"
title: "iOS6 Text Centering Issue"
categories:
  - Mobile
---

After upgrading Xcode, I hadn't used it much until today when I tried to set the centering property for a label. I discovered that the previously used text centering property, `UITextAlignment`, is now deprecated. See the image below.

![Alt text](/images/ios6-text1.png)

Upon checking the documentation, I found that iOS6 introduced a new property, `NSTextAlignment`.

![Alt text](/images/ios6-text2.png)

![Alt text](/images/ios6-text3.png)

The new property includes `Justified` and `Natural`, so out of curiosity, I tried the `Natural` property on a label. It resulted in an error.

![Alt text](/images/ios6-text4.png)

The error message indicated that `NSTextAlignmentNatural` cannot be used with `textAlignment`. Naturally, `Justified` cannot be used either (=\_=). This means that for label text, only `center`, `left`, and `right` properties can be used, just like with `UITextAlignment`. So, in what situations can `Justified` and `Natural` be used?

I searched around but couldn't find an answer to this issue. However, from Apple's documentation, it seems that `Justified` and `Natural` might be intended for larger blocks of text. I haven't tested this, it's just a hypothesis. (⊙o⊙)…
