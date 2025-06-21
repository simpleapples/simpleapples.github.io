---
date: "2012-10-20T13:13:00+00:00"
title: "Solution for Browsers Not Supporting removeAttribute()"
categories:
  - Javascript&CSS
---

Today, while working on a webpage, I wanted to implement a feature where a background image is applied to a `li` element on mouse over, and removed on mouse out.  
Implemented using JavaScript:  

```javascript
if(action == 0) {
    btn.style.backgroundImage = "url(images/index_nav1_07.jpg)";
    btn.style.backgroundRepeat = "repeat-x";
} else {
    btn.removeAttribute("style");
}
```

I found that this worked for Firefox and Internet Explorer, but the mouse out action did not execute in Chrome.

I then discovered that Chrome might not support `removeAttribute()`, so I added a compatibility fix:

```javascript
if(action == 0) {
    btn.style.backgroundImage = "url(images/index_nav1_07.jpg)";
    btn.style.backgroundRepeat = "repeat-x";
} else {
    btn.style.backgroundImage = "";
    btn.style.backgroundRepeat = "";
    btn.removeAttribute("style");
}
```

This method ensures compatibility across Firefox, Internet Explorer, and Chrome.