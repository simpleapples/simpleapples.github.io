---
date: "2013-10-30T13:30:00+00:00"
title: "Do Not Name LiteIDE Project Folder 'go'"
categories:
  - Golang
---

When writing Go programs in LiteIDE, using Ctrl+R to compile and run, the Console outputs the same content every time, even if the code has changed. It still shows the content of the initial code, meaning the new code is not being compiled at all.

Initially, I suspected it was an issue with LiteIDE, so I restarted LiteIDE and even the system, but the problem persisted. Creating a new project in a different location allowed for normal compilation and execution, but when I copied the source files created elsewhere back to the original project location, the issue of not being able to compile reappeared.

So, I looked into the project folder for issues and suddenly discovered that the compiled executable file was named go.exe! This was the root of the problem.

![Alt text](/images/liteide-go.png)

Before solving the problem, it's necessary to understand what LiteIDE does during the compile and execute process.

Step 1: Call `go build` to compile the source files, and output the executable file with the same name as the project.

Step 2: Execute the output executable file.

The problem mainly arises because LiteIDE names the compiled executable file the same as the project folder, and I had named my project folder `go`. When the file is compiled a second time, LiteIDE ends up calling the program that was just compiled, resulting in the program being compiled based on the earliest code, even if the code has changed.

Now that the problem is identified, here are the solutions:

1. LiteIDE should call the `go build` command using the full path, such as `C:/go/bin/go.exe build`.
2. LiteIDE should delete the previously compiled file before compiling.
3. Do not name the project folder `go`.

The first two points are improvements that should be made on the LiteIDE side, while the last point is a way to avoid this issue before LiteIDE is improved.
