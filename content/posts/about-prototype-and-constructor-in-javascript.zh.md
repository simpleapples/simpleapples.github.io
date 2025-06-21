---
date: "2012-10-22T13:15:00+00:00"
title: "关于Javascript中constructor和prototype的一点理解"
categories:
  - Javascript&CSS
---

constructor 和 prototype，顾名思义，是构造者（构造器）和原型的意思。

从语义的角度来看，对象 A 构造了对象 B，则 A 就是 B 的 constructor，如果对象 A 的形态来自对象 B，则对象 B 是 A 的原型。

看一段代码：

    function Person() {
        Person.prototype.name = "myname";
        Person.prototype.age = 18;
        Person.prototype.sayName = function () { alert(this.name); };
    }
    var person1 = new Person();
    person1.sayName();

这里 Person 就是 Person.prototype 的 constructor，为什么？因为 Person 构造了 Person.prototype。而 person1 的 prototype 不是 Person.prototype。在 person1 初始化时，可以理解成把 Person 拷贝了一份（就是 new 了一份）扔给 person1，而 Person 每 new 一次，都会从他的原形处继承（只是称为继承，方便理解）了一份 name,age,sayName。person1 是 copy 了 Person，但是 prototype 并没有 copy，所以说 person1 的 prototype 是 undefined。

这里 person1 很容易被理解成由 Person 构造，这样的话 person1.constructor 岂不成了 Person，现在就要区别一下构造和原形，构造，我们把它理解成从一个框架里建立一个对象，而原形，则是说对象的所有东西（数据）都要从原形继承过来。

再看一个函数：

    function Person(name, age) {
        this.name = name;
        this.age = age;
        this.sayName = function() { alert(this.name); };
    }
    var person2 = new Person( "myname", 18 );
    person2.sayName();

这里的 Person 和上面的 Person 想必相比，上面的 Person 不光构建了一个框架，而且填上了数据，而下面的 Person 只构建了框架，现在就很好区别 constructor 和 prototype 了，person1 从一个对象继承了数据和框架，而 person2 从一个对象只获取了结构（我们把这个过程理解成 Person 构建了 person2），那么 person2 的构造者自然就是 Person。

现在应该比较容易弄清 constructor 和 prototype 的意义了。

### update1:

这里还有一个非常说明问题的例子：

    var arrayTest = new Array();
    alert(arrayTest.constructor); // 为Array

### update2:

还有一个可能遇到的问题，先看代码：
var person3 = new Person();
person3.prototype.name = "name3";

上面的错误非常明显，person3 是 Person 的实例，不能为实例定义原型。
