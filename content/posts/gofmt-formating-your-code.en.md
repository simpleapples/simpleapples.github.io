---
date: "2018-07-17T14:13:00+00:00"
title: "Using gofmt to Format Code"
categories:
  - Golang
---

![](/images/20180717_01.png)

For a programming language, code formatting is often a contentious issue. Different developers may have varying coding styles and habits. However, if all developers can use a unified format to write code, they can focus their valuable time on solving the problems the language is meant to address.

# Introduction to gofmt

The Golang development team has established an official code style and introduced the gofmt tool (gofmt or go fmt) to help developers format their code to this unified style. gofmt is a CLI program that prioritizes reading from standard input. If a file path is provided, it will format that file. If a directory is provided, it will format all .go files in the directory. If no parameters are provided, it will format all .go files in the current directory.

By default, gofmt does not simplify code. You can enable code simplification with the -s flag, which performs the following transformations:

- Removes unnecessary type declarations during array, slice, or map initialization:

```go
For slice expressions like:
    []T{T{}, T{}}
It will be simplified to:
    []T{{}, {}}
```

- Removes unnecessary index specifications in array slice operations:

```go
For slice expressions like:
    s[a:len(s)]
It will be simplified to:
    s[a:]
```

- Removes unnecessary variable assignments during iteration:

```go
For iterations like:
    for x, _ = range v {...}
It will be simplified to:
    for x = range v {...}
For iterations like:
    for _ = range v {...}
It will be simplified to:
    for range v {...}
```

The list of gofmt command parameters is as follows:

```bash
usage: gofmt [flags] [path ...]
  -cpuprofile string
        write cpu profile to this file
  -d    display diffs instead of rewriting files
  -e    report all errors (not just the first 10 on different lines)
  -l    list files whose formatting differs from gofmt's
  -r string
        rewrite rule (e.g., 'a[b:len(a)] -> a[b:]')
  -s    simplify code
  -w    write result to (source) file instead of stdout
```

As you can see, the gofmt command also supports custom rewrite rules using the -r parameter, which takes rules in the format pattern -> replacement.

Consider the following Golang program stored in a file named main.go.

```go
package main

import "fmt"

func main() {
   a := 1
   b := 2
   c := a + b
   fmt.Println(c)
}
```

Use the following rule to format the code above.

```bash
gofmt -r "a + b -> b + a"
```

The formatted result is as follows.

```go
package main

import "fmt"

func main() {
   a := 1
   b := 2
   c := b + a
   fmt.Println(c)
}
```

**\*Note: Gofmt uses tabs for indentation and has no restrictions on line width. If the code is manually broken into lines, gofmt will not force it back into a single line.**

# go fmt and gofmt

gofmt is an independent CLI program, while Go also includes a go fmt command, which is a simple wrapper around gofmt.

```bash
usage: go fmt [-n] [-x] [packages]

Fmt runs the command 'gofmt -l -w' on the packages named
by the import paths. It prints the names of the files that are modified.
For more about gofmt, see 'go doc cmd/gofmt'.
For more about specifying packages, see 'go help packages'.
The -n flag prints commands that would be executed.
The -x flag prints commands as they are executed.
To run gofmt with specific options, run gofmt itself.

See also: go fix, go vet.
```

The go fmt command itself has only two optional parameters: -n and -x. The -n flag prints the commands that would be executed internally by go fmt, while the -x flag prints and executes the go fmt command. For more detailed configuration, you need to run the gofmt command directly.

When calling gofmt, go fmt adds the -l -w parameters, equivalent to executing `gofmt -l -w`.

# Configuring gofmt in Goland

Goland, developed by JetBrains, is a powerful and user-friendly IDE for the Go language.

In Goland, you can add a File Watcher to automatically call gofmt for code formatting when files change. To do this, go to Preferences -> Tools -> File Watchers, click the plus sign to add a go fmt template. The default go fmt template in Goland uses the go fmt command. Replace it with gofmt and add the -l -w -s parameters to enable code simplification. Once configured, Goland will format the code upon saving the source file.

![](/images/20180717_02.png)

# Reference Articles

[https://golang.org/cmd/gofmt/](https://golang.org/cmd/gofmt/)

[https://golang.org/doc/effective_go.html](https://golang.org/doc/effective_go.html)

[https://openhome.cc/Gossip/Go/gofmt.html](https://openhome.cc/Gossip/Go/gofmt.html)

[https://github.com/hyper0x/go_command_tutorial/blob/master/0.9.md](https://github.com/hyper0x/go_command_tutorial/blob/master/0.9.md)