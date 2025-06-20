---
date: "2019-10-28T10:55:00+00:00"
title: "Docker COPY 复制文件夹的诡异行为"
categories:
  - DevOps
---

### 问题现象

在制作 docker 镜像时，有复制某一个路径下所有文件和文件夹到镜像的需求，写下了如下 dockerfile：

```dockerfile
FROM alpine
WORKDIR /root/test_docker_proj
COPY * ./
```

原始目录结构是这样的：

```bash
/projects/test_docker_proj
├── Dockerfile
├── dir1
│   ├── dir11
│   │   └── file11
│   └── file1
└── file2
```

然而复制到 docker 镜像里的目录结构变成了这样：

```bash
/root/test_docker_proj
├── Dockerfile
├── dir11
│   └── file11
├── file1
└── file2
```

<!-- more -->

可以看到 dir1 这个文件夹并没有被复制到镜像里，但是 dir1 中的子文件夹和文件都被复制进来了，和 dir1 同级的文件也被复制了。也就是说，在 COPY 执行的过程中，第一层文件夹被「解包」了。

### COPY/ADD 行为逻辑

为了确定 COPY 和相似的 ADD 命令的行为，做了以下测试：

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

通过测试可以发现 `COPY/ADD` 命令有这么几个规则：

1. `ADD` 命令和 `COPY` 命令在复制文件时行为一致
2. 使用 `*` 作为 `COPY/ADD` 命令的源时候表示的是 `./*`
3. `COPY/ADD` 命令的源如果是文件夹，复制的是文件夹的内容而不是其本身
4. `COPY ./* target` 中的 `*` 会被翻译成如下的逻辑：

```dockerfile
COPY ./sub_dir1 target
COPY ./sub_dir2 target
COPY ./file1 target
COPY ./file2 target
```

文件系统里的文件夹和文件，本质上都是文件，我们熟悉的操作系统的 `cp` 命令在执行 `cp * target` 时会把文件夹当成文件一股脑的复制到目标路径下，可以认为复制了文件本身，而 docker 的 `COPY/ADD` **在复制文件夹时复制的是其内容**。

docker 的这种「奇怪」的逻辑已经被诟病许久了，但是似乎还没有要改变的意思，最新的进展可以参考下面两个 issue，在 docker 做出修改之前，只能在写 dockerfile 时候注意一下了。

![](/images/20191028_01.png)

### 参考文档

[https://stackoverflow.com/questions/30256386/how-to-copy-multiple-files-in-one-layer-using-a-dockerfile](https://stackoverflow.com/questions/30256386/how-to-copy-multiple-files-in-one-layer-using-a-dockerfile)

[https://github.com/moby/moby/issues/15858](https://github.com/moby/moby/issues/15858)

[https://github.com/moby/moby/issues/29211](https://github.com/moby/moby/issues/29211)
