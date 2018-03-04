---
layout: post
title: "关于Javascript中constructor和prototype的一点理解"
date: 2012-10-22 13:15
comments: true
categories: Javascript&CSS
---

constructor和prototype，顾名思义，是构造者（构造器）和原型的意思。  

从语义的角度来看，对象A构造了对象B，则A就是B的constructor，如果对象A的形态来自对象B，则对象B是A的原型。  

看一段代码：  

	function Person() {
	    Person.prototype.name = "myname";
	    Person.prototype.age = 18;
	    Person.prototype.sayName = function () { alert(this.name); };
	}
	var person1 = new Person();
	person1.sayName();

这里Person就是Person.prototype的constructor，为什么？因为Person构造了Person.prototype。而person1的prototype不是Person.prototype。在person1初始化时，可以理解成把Person拷贝了一份（就是new了一份）扔给person1，而Person每new一次，都会从他的原形处继承（只是称为继承，方便理解）了一份name,age,sayName。person1是copy了Person，但是prototype并没有copy，所以说person1的prototype是undefined。  

这里person1很容易被理解成由Person构造，这样的话person1.constructor岂不成了Person，现在就要区别一下构造和原形，构造，我们把它理解成从一个框架里建立一个对象，而原形，则是说对象的所有东西（数据）都要从原形继承过来。  

再看一个函数：  

	function Person(name, age) {
	    this.name = name;
	    this.age = age;
	    this.sayName = function() { alert(this.name); };
	}
	var person2 = new Person( "myname", 18 );
	person2.sayName();

这里的Person和上面的Person想必相比，上面的Person不光构建了一个框架，而且填上了数据，而下面的Person只构建了框架，现在就很好区别constructor和prototype了，person1从一个对象继承了数据和框架，而person2从一个对象只获取了结构（我们把这个过程理解成Person构建了person2），那么person2的构造者自然就是Person。

现在应该比较容易弄清constructor和prototype的意义了。

### update1: ###

这里还有一个非常说明问题的例子：

	var arrayTest = new Array();
	alert(arrayTest.constructor); // 为Array

### update2: ###
还有一个可能遇到的问题，先看代码：
	
	var person3 = new Person();
	person3.prototype.name = "name3";

上面的错误非常明显，person3是Person的实例，不能为实例定义原型。