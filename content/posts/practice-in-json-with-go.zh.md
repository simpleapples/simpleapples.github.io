---
date: "2018-12-24T10:43:00+00:00"
title: "go json 实践中遇到的坑"
categories:
  - Golang
---

![](/images/20181224_01.png)

在使用 go 语言开发过程中，经常需要使用到 json 包来进行 json 和 struct 的互相转换，在使用过程中，遇到了一些需要额外注意的地方，记录如下。

<!-- more -->

### 整数变浮点数问题

假设有一个 Person 结构，其中包含 Age int64 和 Weight float64 两个字段，现在通过 json 包将 Person 结构转为 map[string]interface{}，代码如下。

```go
type Person struct {
	Name string
	Age int64
	Weight float64
}

func main() {
    person := Person{
        Name: "Wang Wu",
        Age: 30,
        Weight: 150.07,
    }

    jsonBytes, _ := json.Marshal(person)
    fmt.Println(string(jsonBytes))

    var personFromJSON interface{}
    json.Unmarshal(jsonBytes, &personFromJSON)

    r := personFromJSON.(map[string]interface{})
}
```

代码执行到这里看上去一切正常，但是打印一下 map[string]interface{} 就会发现不太对了。

```go
fmt.Println(reflect.TypeOf(r["Age"]).Name())  // float64
fmt.Println(reflect.TypeOf(r["Weight"]).Name())  // float64
```

转换成 map[string]interface{} 之后，原先的 uint64 和 float64 类型都被转换成了 float64 类型，这显然是不符合我们的预期的。

![](/images/20181224_02.png)

查看 json 的规范可以看到，在 json 中是没有整型和浮点型之分的，所以现在可以理解 json 包中的 Unmarshal 方法转出的数字类型为什么都是 float64 了，因为根据 json 规范，数字都是同一种类型，那么对应到 go 的类型中最接近的就是 float64 了。

json 包还针对这个问题提供了更好的解决方案，不过需要使用 json.Decoder 来代替 json.Unmarshal 方法，将 json.Unmarhsal 替换如下。

```go
var personFromJSON interface{}

decoder := json.NewDecoder(bytes.NewReader(jsonBytes))
decoder.UseNumber()
decoder.Decode(&personFromJSON)

r := personFromJSON.(map[string]interface{})
```

这种方法首先创建了一个 jsonDecoder，然后调用了 UseNumber 方法，从文档中可以知道，使用 UseNumber 方法后，json 包会将数字转换成一个内置的 Number 类型（而不是 float64），这个 Number 类型提供了转换为 int64、float64 等多个方法。

![](/images/20181224_03.png)

### 时间格式

对于 json 格式，是没有时间类型的，日期和时间以 json 格式存储时，需要转换为字符串类型。这就带来了一个问题，日期时间的字符串表示有多种多样，go 的 json 包支持的是哪一种呢？

使用下面的代码来输出 json.Marshal 方法将 Time 类型转换为字符串后的格式。

```go
type Person struct {
	Name string
	Birth time.Time
}

func main() {
	person := Person{
		Name: "Wang Wu",
		Birth: time.Now(),
	}

	jsonBytes, _ := json.Marshal(person)
	fmt.Println(string(jsonBytes))  // {"Name":"Wang Wu","Birth":"2018-12-20T16:22:02.00287617+08:00"}
}
```

根据输出可以判断，go 的 json 包使用的是 RFC3339 标准中定义的格式。接下来测试一下 json.Unmarshal 方法所支持的日期时间格式。

```go
dateStr := "2018-10-12"

var person Person
jsonStr := fmt.Sprintf("{\"name\":\"Wang Wu\", \"Birth\": \"%s\"}", dateStr)
json.Unmarshal([]byte(jsonStr), &person)

fmt.Println(person.Birth)  // 0001-01-01 00:00:00 +0000 UTC
```

对于形如 2018-10-12 的字符串，json 包并没有成功将其解析，接下来我们把 time 包中支持的所有格式都试一下。

![](/images/20181224_04.png)

经过试验，发现 json.Unmarshal 方法只支持 RFC3339 和 RFC3339Nano 两种格式的转换。还有一个需要注意的地方，使用 time.Now() 生成的时间是带有一个 Monotonic Time 的，经过 json.Marshal 转换时候，由于 RFC3339 规范里没有存放 Monotonic Time 的位置，会丢掉这一部分。

### 对于字段为空的处理

json 包对于空值的处理是一个非常容易出错的地方，看下面代码。

```go
type Person struct {
	Name     string
	Age      int64
	Birth    time.Time
	Children []Person
}

func main() {
	person := Person{}

	jsonBytes, _ := json.Marshal(person)
	fmt.Println(string(jsonBytes))  // {"Name":"","Age":0,"Birth":"0001-01-01T00:00:00Z","Children":null}
}
```

当 struct 中的字段没有值时，使用 json.Marshal 方法并不会自动忽略这些字段，而是根据字段的类型输出了他们的默认空值，这往往和我们的预期不一致，json 包提供了对字段的控制手段，我们可以为字段增加 omitempty tag，这个 tag 会在字段值为零值（int 和 float 类型零值是 0，string 类型零值是 ""，对象类型零值是 nil）时，忽略该字段。

```go
type PersonAllowEmpty struct {
	Name     string             `json:",omitempty"`
	Age      int64              `json:",omitempty"`
	Birth    time.Time          `json:",omitempty"`
	Children []PersonAllowEmpty `json:",omitempty"`
}

func main() {
	person := PersonAllowEmpty{}
	jsonBytes, _ := json.Marshal(person)
	fmt.Println(string(jsonBytes))  // {"Birth":"0001-01-01T00:00:00Z"}
}
```

可以看到，这次输出的 json 中只有 Birth 字段了，string、int、对象类型的字段，都因为没有赋值，默认是零值，所以被忽略，对于日期时间类型，由于不可以设置为零值，也就是 0000-00-00 00:00:00，不会被忽略。

需要注意这样的情况：如果一个人的年龄是 0 （对于刚出生的婴儿，这个值是合理的），刚好是 int 字段的零值，在添加 omitempty tag 的情况下，年龄字段会被忽略。

如果想要某一个字段在任何情况下都被 json 包忽略，需要使用如下的写法。

```go
type Person struct {
	Name     string `json:"-"`
	Age      int64 `json:"-"`
	Birth    time.Time `json:"-"`
	Children []string `json:"-"`
}

func main() {
    birth, _ := time.Parse(time.RFC3339, "1988-12-02T15:04:27+08:00")
	person := Person{
		Name: "Wang Wu",
		Age: 30,
		Birth: birth,
		Children: []string{},
	}

	jsonBytes, _ := json.Marshal(person)
    fmt.Println(string(jsonBytes))  // {}
}
```

可以看到，使用 json:"-" 标签的字段都被忽略了。
