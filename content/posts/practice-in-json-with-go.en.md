---
date: "2018-12-24T10:43:00+00:00"
title: "Pitfalls Encountered in Go JSON Practice"
categories:
  - Golang
---

![](/images/20181224_01.png)

During the development process using the Go language, the `json` package is often used for mutual conversion between JSON and structs. In the process, I encountered some areas that require extra attention, which I have documented below.

<!-- more -->

### Integer to Float Conversion Issue

Suppose there is a `Person` structure that contains two fields: `Age int64` and `Weight float64`. Now, let's convert the `Person` structure to `map[string]interface{}` using the `json` package. The code is as follows:

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

At this point, everything seems normal, but printing the `map[string]interface{}` reveals something unusual.

```go
fmt.Println(reflect.TypeOf(r["Age"]).Name())  // float64
fmt.Println(reflect.TypeOf(r["Weight"]).Name())  // float64
```

After converting to `map[string]interface{}`, the original `int64` and `float64` types have both been converted to `float64`, which is clearly not what we expected.

![](/images/20181224_02.png)

Upon reviewing the JSON specification, we see that there is no distinction between integer and floating-point types in JSON. Therefore, we can understand why the `Unmarshal` method in the `json` package converts number types to `float64`. According to the JSON specification, numbers are of the same type, and the closest corresponding Go type is `float64`.

The `json` package provides a better solution for this issue, but it requires using `json.Decoder` instead of the `json.Unmarshal` method. Replace `json.Unmarshal` as follows:

```go
var personFromJSON interface{}

decoder := json.NewDecoder(bytes.NewReader(jsonBytes))
decoder.UseNumber()
decoder.Decode(&personFromJSON)

r := personFromJSON.(map[string]interface{})
```

This method first creates a `jsonDecoder` and then calls the `UseNumber` method. According to the documentation, using the `UseNumber` method causes the `json` package to convert numbers into a built-in `Number` type (instead of `float64`). This `Number` type provides methods for conversion to `int64`, `float64`, and others.

![](/images/20181224_03.png)

### Time Format

In JSON format, there is no time type. When storing dates and times in JSON format, they need to be converted to string type. This brings up a problem: there are various string representations of date and time. Which one does the Go `json` package support?

Use the following code to output the format after the `json.Marshal` method converts the `Time` type to a string.

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

Based on the output, we can determine that the Go `json` package uses the format defined in the RFC3339 standard. Next, let's test which date and time formats are supported by the `json.Unmarshal` method.

```go
dateStr := "2018-10-12"

var person Person
jsonStr := fmt.Sprintf("{\"name\":\"Wang Wu\", \"Birth\": \"%s\"}", dateStr)
json.Unmarshal([]byte(jsonStr), &person)

fmt.Println(person.Birth)  // 0001-01-01 00:00:00 +0000 UTC
```

For strings like "2018-10-12", the `json` package did not successfully parse them. Next, let's try all the formats supported by the `time` package.

![](/images/20181224_04.png)

After testing, we found that the `json.Unmarshal` method only supports conversion of RFC3339 and RFC3339Nano formats. Another point to note is that the time generated using `time.Now()` includes a Monotonic Time. During the `json.Marshal` conversion, since there is no place to store Monotonic Time in the RFC3339 specification, this part will be lost.

### Handling Empty Fields

Handling empty values is an area where the `json` package can easily lead to errors. Consider the following code:

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

When the fields in a struct have no values, using the `json.Marshal` method does not automatically ignore these fields. Instead, it outputs their default empty values based on the field types, which often does not align with our expectations. The `json` package provides control over fields, allowing us to add the `omitempty` tag to fields. This tag will ignore the field when its value is zero (the zero value for int and float types is 0, for string types is "", and for object types is nil).

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

As you can see, this time the output JSON only contains the `Birth` field. The fields of string, int, and object types were ignored because they were not assigned values and defaulted to zero values. For date and time types, since they cannot be set to zero value (i.e., 0000-00-00 00:00:00), they are not ignored.

Be cautious of this situation: if a person's age is 0 (which is reasonable for a newborn), it coincides with the zero value for the int field. With the `omitempty` tag added, the age field will be ignored.

If you want a specific field to be ignored by the `json` package under any circumstances, use the following syntax:

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

As you can see, fields with the `json:"-"` tag are all ignored.