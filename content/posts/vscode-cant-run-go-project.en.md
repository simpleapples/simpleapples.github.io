---
date: "2020-04-20T15:35:00+00:00"
title: "Exploring the vscode debug process to resolve issues with running Go programs"
categories:
  - Golang
---

### Problem Description

VSCode cannot run Go projects in `run` mode (it can only debug in `debug` mode), and the following error occurs.

![](/images/20200420_01.png)

The obscured part in the image is a package within the project, not a third-party package. This means that when running a Go project in `run` mode, it cannot find other Go files, only the entry file.

### Initial Investigation

The first thought about not finding other files is an issue with the GO_PATH. However, the project uses Go modules, allowing the creation of projects outside the GO_PATH, so this suspicion is ruled out. Next, I suspected an issue with the VSCode configuration. Each VSCode project has a .launch.json file that configures the environment when running code. Below is the .launch.json from the project.

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch",
      "type": "go",
      "request": "launch",
      "mode": "auto",
      "program": "${workspaceRoot}/src/main.go",
      "env": {},
      "args": []
    }
  ]
}
```

You can see that the .launch.json does not specify the working directory of the program. Could it be that the default working paths for `debug` and `run` modes are different? So I used `os.Getwd()` in the main function to print the current path, and the results are as follows:

- `debug` mode: The project directory
- `run` mode: The user directory

It can be confirmed that the working path in `run` mode is incorrect, leading to the path not being found. Add the `cwd` parameter in .launch.json and manually enter the project path.

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch",
      "type": "go",
      "request": "launch",
      "mode": "auto",
      "program": "${workspaceRoot}/src/main.go",
      "cwd": "${workspaceRoot}",
      "env": {},
      "args": []
    }
  ]
}
```

However, after modifying .launch.json and running the program, the output working directory is still the user directory, indicating that the `cwd` parameter did not take effect.

### Exploring the VSCode Debug Process

At this point, the bug seems more evident, as the `cwd` parameter is not taking effect, indicating an issue!

I decided to take a closer look at the VSCode debugging process using a rather brute-force method to see how VSCode runs Go programs when the run button is clicked.

```go
package main
import "time"
func main() {
    time.Sleep(10000000000)
}
```

After running the program, use `ps -ef|grep go` to check the processes.

![](/images/20200420_02.jpg)

The three processes in the screenshot are in a parent-child relationship from top to bottom. This means that even when using `run` mode in VSCode, it does not directly execute `go run xxxx.go`, which is different from the behavior of other IDEs like Goland. VSCode first calls the node in the language server to execute a `goDebug.js` in the Go extension (installed to support Go language projects), which then calls `go run xxxx.go`. (The main file in the /tmp path is a binary file generated during the execution of go run)

Next, I checked the logic in `goDebug.js` and found the code that calls `go run`.

```js
this.debugProcess = spawn(getBinPathWithPreferredGopath("go", []), runArgs, {
  env,
});
```

Looking at the logic a few lines above, based on the parameter names, it can be inferred that the configuration in .launch.json can be accessed here. I then directly modified the js file for debugging to confirm the above inference. Since we cannot directly see the output of node goDebug.js, we debug by writing to a file.

```js
fs.writeFile('test.log', this.debugProcess.cwd(), function (err) {}
```

After adding this line and running again, we can see that the test.log file has printed the working path of this process, which is the working path of go run, the user directory. At this point, the issue can be narrowed down to: the `cwd` in the .launch.json file is not passed to the subprocess (go run) when node calls go run.

`spawn` is a function in Node.js. Looking at the spawn documentation, we find that spawn has three parameters `child_process.spawn(command[, args][, options])`. The third parameter options can specify the cwd working path. However, the code in `goDebug.js` that starts the subprocess does not set cwd, only the `env` parameter, which is why the `run` mode cannot run Go programs.

![](/images/20200420_03.jpg)

### Solution

When discovering this issue, the latest version of the VSCode Go extension was 0.13. This issue can temporarily be resolved by modifying the source code of goDebug.js. As shown in the image below, add the commented code to pass the `cwd` parameter to the subprocess, resolving the issue.

![](/images/20200420_04.png)

Additionally, this bug has been fixed. You can refer to [ISSUE #3096](https://github.com/microsoft/vscode-go/issues/3096). While solving another issue in this ISSUE, the programmer "incidentally" fixed the `cwd` issue. After the release of VSCode Go extension 0.14 (already released), updating the Go extension to the latest version will allow normal running and debugging of Go projects.

### References

[Debugging in Visual Studio Code](https://code.visualstudio.com/docs/editor/debugging)

[Node.js v13.13.0 Documentation](https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options)

[Debug: add "go run ." support #3096](https://github.com/microsoft/vscode-go/issues/3096)