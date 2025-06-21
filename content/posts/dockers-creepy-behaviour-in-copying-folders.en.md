---
date: "2019-10-28T10:55:00+00:00"
title: "The Peculiar Behavior of Docker COPY When Copying Directories"
categories:
  - DevOps
---

### Problem Description

When creating a Docker image, there is a need to copy all files and directories from a certain path into the image. The following Dockerfile was written:

```dockerfile
FROM alpine
WORKDIR /root/test_docker_proj
COPY * ./
```

The original directory structure is as follows:

```bash
/projects/test_docker_proj
├── Dockerfile
├── dir1
│   ├── dir11
│   │   └── file11
│   └── file1
└── file2
```

However, the directory structure copied into the Docker image turns out like this:

```bash
/root/test_docker_proj
├── Dockerfile
├── dir11
│   └── file11
├── file1
└── file2
```

<!-- more -->

As you can see, the `dir1` folder was not copied into the image, but the subdirectories and files within `dir1` were copied, along with files at the same level as `dir1`. In other words, during the execution of the COPY command, the top-level directory was "unpacked."

### COPY/ADD Behavior Logic

To determine the behavior of the COPY command and the similar ADD command, the following tests were conducted:

```dockerfile
FROM alpine

WORKDIR /root/test_docker_proj_1
COPY * ./

WORKDIR /root/test_docker_proj_2
ADD * ./

WORKDIR /root/test_docker_proj_3
COPY ./ ./

WORKDIR /root/test_docker_proj_4
ADD ./ ./

WORKDIR /root/test_docker_proj_5
COPY ./dir* ./

WORKDIR /root/test_docker_proj_6
ADD ./dir* ./
```

The tests revealed several rules about the `COPY/ADD` commands:

1. The `ADD` command behaves the same as the `COPY` command when copying files.
2. Using `*` as the source in `COPY/ADD` commands represents `./*`.
3. If the source of `COPY/ADD` is a directory, the contents of the directory are copied, not the directory itself.
4. In `COPY ./* target`, the `*` is translated into the following logic:

```dockerfile
COPY ./sub_dir1 target
COPY ./sub_dir2 target
COPY ./file1 target
COPY ./file2 target
```

In file systems, both directories and files are essentially files. The `cp` command in operating systems, when executing `cp * target`, treats directories as files and copies them to the target path, effectively copying the files themselves. However, Docker's `COPY/ADD` **copies the contents of directories, not the directories themselves**.

This "strange" logic of Docker has been criticized for a long time, but there seems to be no intention to change it. The latest developments can be referenced in the two issues below. Until Docker makes changes, it's important to pay attention when writing Dockerfiles.

![](/images/20191028_01.png)

### Reference Documents

[https://stackoverflow.com/questions/30256386/how-to-copy-multiple-files-in-one-layer-using-a-dockerfile](https://stackoverflow.com/questions/30256386/how-to-copy-multiple-files-in-one-layer-using-a-dockerfile)

[https://github.com/moby/moby/issues/15858](https://github.com/moby/moby/issues/15858)

[https://github.com/moby/moby/issues/29211](https://github.com/moby/moby/issues/29211)