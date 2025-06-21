---
date: "2013-01-06T12:15:00+00:00"
title: "Javascript Study Notes - Pseudo-classes and Inheritance"
categories:
  - Javascript&CSS
---

Inheritance in Javascript can be divided into two main categories (non-constructor inheritance and constructor inheritance). Let's start with the simpler one and get to know constructor-based inheritance.  
Javascript is a prototype-based language and does not have the concept of classes inherently, so we can only simulate class-based patterns to implement classes and class inheritance. We use constructor functions to simulate the concept of classes. For example, let's define a Person class.

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
}
```

The above defines a Person class with name and age properties. Let's call this class.

```javascript
var somebody = new Person("John", 18);
alert(somebody.name);  // John
alert(somebody.age);  // 18
```

OK, at this point, we have completed a simple class constructor function and its invocation method. Next, let's further understand class inheritance. For instance, we need a Developer class that should inherit from the Person class, and additionally include the languages (lang) and gender (sex) that an engineer knows. We will still use the constructor function method to write this class.

```javascript
function Developer(name, age, sex, lang) {
    this.person = Person;
    this.person(name, age);
    delete this.person;
    this.sex = sex;
    this.lang = lang;
}
```

The Developer class can inherit the properties from the Person class. Let's try calling it.

```javascript
var coder = new Developer("Bill", 22, "Male", "Javascript");
alert(coder.name);  // Bill
alert(coder.age);  // 22
alert(coder.sex);  // Male
alert(coder.lang);  // Javascript
```

The method of inheritance for the Person class in the Developer class is very easy to understand. Since Javascript is function-based, and the Person constructor function is essentially a function, we can use the method of calling Person to inherit it. At this point, some might ask, since inheritance can be achieved by calling the constructor function, why not directly use

```javascript
Person(name, age);
```

to call it? Here, we need to consider the scope of `this`. When calling Person directly, `this` will point to the global scope, not Developer. Try outputting `this.name` in the global scope when calling Person directly.  
Alright, since we understand the principle of this inheritance method, we can expand it because there are many ways to call a function. Here are a few examples.

```javascript
Person.call(this, name, age);
Person.apply(this, [name, age]);
```

At this point, we have completed the simplest class construction and inheritance in Javascript.