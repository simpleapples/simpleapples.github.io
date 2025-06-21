---
date: "2012-11-14T13:34:00+00:00"
title: "Compass WebApp"
categories:
  - Idea&Demo
---

A Compass WebApp has been created using JavaScript.

The app listens to the DeviceOrientation event, where the device generates three values: alpha, beta, and gamma when it changes orientation. The alpha value represents the current angle.

```javascript
window.addEventListener('deviceorientation', function(event) {
    target.style.transform = 'rotate(' + event.alpha + ')';
}, false);
```

The alpha value is 0° at true north and increases clockwise to 360°, corresponding to the rotation angle of the compass needle.

The CSS3 transform property is used to rotate the needle.

Finally, the compass degrees are evaluated to determine the direction (e.g., XX degrees east of north, XX degrees west of south, etc.).

This can only be used normally on browsers that support DeviceOrientation (mobile Safari, Android 4.0+ browser, mobile).

Demo URL: [http://labs.simpleapples.com/compass](http://labs.simpleapples.com/compass)

GitHub: [http://github.com/simpleapples/compass](http://github.com/simpleapples/compass)

### Update 1: ###

It was discovered that this application has an issue on iPhone where the initial orientation of the phone is mistakenly recognized as true north. = =!

The solution is to use webkitCompassHeading to obtain the angle instead of the alpha value. webkitCompassHeading provides the angle difference between the device orientation and magnetic north, whereas the alpha value represents the rotation angle of the device. Refer to Apple's documentation:

[http://developer.apple.com/library/safari/#documentation/SafariDOMAdditions/Reference/DeviceOrientationEventClassRef/DeviceOrientationEvent/DeviceOrientationEvent.html](http://developer.apple.com/library/safari/#documentation/SafariDOMAdditions/Reference/DeviceOrientationEventClassRef/DeviceOrientationEvent/DeviceOrientationEvent.html)

On the Android platform's Opera browser, the alpha value represents the angle difference between the device and the north pole, possibly due to Opera's better support for HTML5.