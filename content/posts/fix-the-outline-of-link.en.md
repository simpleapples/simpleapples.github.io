---
date: "2012-10-20T13:03:00+00:00"
title: "Solving the Issue of Dotted Outline Around Hyperlinks After Clicking"
categories:
  - Javascript&CSS
---

In Firefox or IE browsers, when you click on an `<a>` tag, a dotted outline appears around the tag (as shown in the image), which affects the aesthetics.

![Alt text](/images/outline.png)

To solve this issue for IE browsers, add

    hidefocus="hidefocus"

to the `<a>` tag.

For Firefox browsers, the solution is to add the CSS property

    outline:none
