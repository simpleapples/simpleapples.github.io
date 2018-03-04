---
layout: post
title: "Javascript学习笔记--伪类和继承"
date: 2013-01-06 12:15
comments: true
categories: Javascript&CSS
---

Javascript中继承可以分为两大类（非构造函数的继承和构造函数的继承），先从简单的说起，了解一下基于构造函数的继承。  
Javascript是一门基于原形的的语言，本身并没有类的概念，所以只能用模拟基于类的模式来实现类和类的继承。用构造函数来模拟类的概念。例如，我们定义一个Person类。  

	function Person(name, age) {
	    this.name = name;
	    this.age = age;
	}

上面就定义了一个Person类，包含name和age属性，下面来调用这个类。

	var somebody = new Person("John", 18);
	alert(somebody.name);  // John
	alert(somebody.age);  // 18

OK,到这里就完成了一个简单的类的构造函数和调用方法。接下来，进一步了解类的继承，比如需要一个Developer的类，Developer类需要继承Person类，此外还要包含工程师所会的语言（lang）和性别（sex）。还是用构造函数的方法来写这个类。

	function Developer(name, age, sex, lang) {
	    this.person = Person;
	    this.person(name, age);
	    delete this.person;
	    this.sex = sex;
	    this.lang = lang;
	}

Developer类就可以继承Person中的属性了，尝试调用一下。

	var coder = new Developer("Bill", 22, "Male", "Javascript");
	alert(coder.name);  // Bill
	alert(coder.age);  // 22
	alert(coder.sex);  // Male
	alert(coder.lang);  // Javascript

Developer类中对于Person类的继承方法非常好理解，由于Javascript是基于函数的，而Person这个构造函数本质上也是函数，那么就可以用调用Person的方法继承它。看到这里可能有人会问，既然通过对构造函数的调用可以实现继承，那么为什么不直接使用

	Person(name, age);

来调用呢？这里要考虑this的作用域了，当直接调用Person时候，this会指向全局，而不是Developer。直接调用Person，可以试试在全局中输出this.name。  
好，既然明白这种继承的调用方法的原理，那么就可以扩展开了，因为函数的调用方式有很多种，举几个例子。

	Person.call(this, name, age);
	Person.apply(this, [name, age]);

到这里就完成了Javascript中最简单的类的构造和继承。