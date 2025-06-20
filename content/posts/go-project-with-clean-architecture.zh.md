---
date: "2021-12-12T16:45:00+00:00"
title: "基于Clean Architecture的Go项目架构实践"
categories:
  - Golang
---

经过这些年的发展，Go 语言已经成为一门被广泛使用在各个领域的编程语言。从 k8s、docker 等基础组件，到业务领域的微服务，都可以用 Go 构建。在构建这些 Go 项目时，采用哪种架构模式和代码布局，是一个仁者见仁智者见智的事情。有 Java Spring 经验的可能会采用 MVC 模式，有 Python Flask 经验的可能会采用 MTV 模式。加上 Go 语言领域并没有出现主流的企业级开发框架，很多项目甚至没有明确的架构模式。

# Clean Architecture

![](/images/20211212_01.png)

Clean Architecture 是 Uncle Bob 提出的适用于复杂业务系统的架构模式，其核心思想是将业务复杂度与技术复杂度解藕，相比于 MVC、MTV 等模式，Clean Architecture 除了进行分层，还通过约定依赖原则，明确了与外部依赖的交互方式，以及外部依赖与业务逻辑的边界。感兴趣的朋友可以直接阅读作者原文[https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)。

由于 Clean Architecture 具有脱离语言和框架的灵活性，作者在提出时也没有规定实现细节，给 Clean Architecture 的落地带来了困难，接下来以一个例子来说明如何在 Go 项目中应用 Clean Architecture 的思想。

# 布局

作为一个 Go 项目，不管用哪种架构模式，建议都建立 app 和 scripts 这两个路径。app 存放启动 Go 项目的入口文件，通常是 main.go。而 scripts 可以放一些构建和部署时候用到的脚本。

```bash
clean_architecture_demo
├── README.md
├── app
│   └── main.go
├── scripts
│   ├── build.sh
│   └── run.sh
├── go.mod
├── go.sum
└── usecases
```

接下来是代码部分，分为 entities、usecases、adapters 三个部分。

- entities：存储领域实体。用一个博客系统举例，领域实体可能有用户（user）和文章（article）
- usecases：存储业务逻辑。用博客系统举例，可能会有用户相关的业务逻辑（signup_user、signin_user、add_user、delete_user)和文章相关的业务逻辑（add_article、show_article、delete_article）
- adapters：存储适配器逻辑。适配器是连接业务逻辑与外部依赖的层，博客以 Web 形式提供服务，就需要一个 http_adapter 来封装 Web 服务；同时保存文章到数据库，需要封装一个 db_adapter 来连接。

下面是项目的布局结构。

```python
clean_architecture_demo
├── README.md
├── adapters
│   ├── api
│   ├── db
│   └── log
├── app
│   └── main.go
├── scripts
│   ├── build.sh
│   └── run.sh
├── entities
│   ├── article.go
│   └── user.go
├── go.mod
├── go.sum
└── usecases
```

# 数据流向

用一个查询文章的请求来描述一下调用链路。

- 用户通过 HTTP 服务的调用 WebAdapter 的 ShowArticleHandler 方法
- 由于是文章相关的逻辑，ShowArticleHandler 调用 ArticleUsecase 的 ShowArticle 方法
- 需要从 DB 中查询文章，ArticleUsecase 会调用 DBAdapter 的 GetArticle 方法
- DBAdapter 的 GetArticle 从 MySQL 中查询出文章内容返回给 ArticleUsecase
- ArticleUsecase 返回给 WebAdapter
- WebAdapter 通过 HTTP 服务返回给用户

![](/images/20211212_02.png)

# 代码示例

为了更清晰的说分层和架构，我在 Github 上发布了一个示例项目，感兴趣的朋友可以直接去看源码：[https://github.com/simpleapples/go-clean-architecture](https://github.com/simpleapples/go-clean-architecture)

# 结论

由于 Clean Architecture 没有规定实现细节，所以上述的分层和布局方式只是一种参考，还有众多的实践方式。例如 Adapter 层可以根据外部依赖的类型细分成平行的 Presenter+Gateway 层，在复杂项目中，更细致的分层可以把代码拆的更细致，大家可以根据自己的项目规模来调整分层和布局，这里就不做赘述了。
