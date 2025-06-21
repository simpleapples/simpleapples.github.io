---
date: "2012-10-22T13:15:00+00:00"
title: "A Little Understanding of Constructor and Prototype in Javascript"
categories:
  - Javascript&CSS
---

Constructor and prototype, as the names suggest, mean the builder (constructor) and the prototype.  

From a semantic perspective, if object A constructs object B, then A is the constructor of B. If the form of object A comes from object B, then object B is the prototype of A.  

Let's look at a piece of code:  

```javascript
function Person() {
    Person.prototype.name = "myname";
    Person.prototype.age = 18;
    Person.prototype.sayName = function () { alert(this.name); };
}
var person1 = new Person();
person1.sayName();
```

Here, Person is the constructor of Person.prototype. Why? Because Person constructed Person.prototype. However, the prototype of person1 is not Person.prototype. When person1 is initialized, it can be understood as a copy of Person (i.e., a new instance) is given to person1. Every time Person is instantiated, it inherits (just called inheritance for convenience) a copy of name, age, and sayName from its prototype. person1 is a copy of Person, but the prototype is not copied, so the prototype of person1 is undefined.  

It is easy to understand person1 as being constructed by Person. In this case, wouldn't person1.constructor be Person? Now we need to distinguish between constructor and prototype. We understand construction as creating an object from a framework, while prototype means that all the object's properties (data) are inherited from the prototype.  

Let's look at another function:  

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
    this.sayName = function() { alert(this.name); };
}
var person2 = new Person("myname", 18);
person2.sayName();
```

Compared to the previous Person, the earlier Person not only built a framework but also filled it with data, while the latter Person only built the framework. Now it's easy to distinguish between constructor and prototype. person1 inherited data and framework from an object, while person2 only obtained the structure from an object (we understand this process as Person constructing person2), so the constructor of person2 is naturally Person.

Now it should be easier to understand the meaning of constructor and prototype.

### update1: ###

Here's another example that illustrates the issue well:

```javascript
var arrayTest = new Array();
alert(arrayTest.constructor); // Outputs Array
```

### update2: ###
Here's another potential issue you might encounter, consider the following code:

```javascript
var person3 = new Person();
person3.prototype.name = "name3";
```

The error here is quite obvious. person3 is an instance of Person, and you cannot define a prototype for an instance.