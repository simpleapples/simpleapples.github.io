---
date: "2021-12-12T16:45:00+00:00"
title: "Practicing Go Project Architecture with Clean Architecture"
categories:
  - Golang
---

Over the years, Go has become a widely used programming language across various fields. From foundational components like k8s and Docker to microservices in the business domain, Go can be used to build them all. When constructing these Go projects, the choice of architecture pattern and code layout is subjective. Those with Java Spring experience might opt for the MVC pattern, while those familiar with Python Flask might choose the MTV pattern. Moreover, since there is no mainstream enterprise-level development framework in the Go language domain, many projects lack a clear architectural pattern.

# Clean Architecture

![](/images/20211212_01.png)

Clean Architecture, proposed by Uncle Bob, is an architectural pattern suitable for complex business systems. Its core idea is to decouple business complexity from technical complexity. Compared to patterns like MVC and MTV, Clean Architecture not only involves layering but also clarifies the interaction with external dependencies and the boundaries between external dependencies and business logic through dependency rules. Interested readers can refer to the original article by the author [here](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).

Due to its flexibility in being language and framework agnostic, the author did not specify implementation details when proposing Clean Architecture, making its application challenging. The following example illustrates how to apply the principles of Clean Architecture in a Go project.

# Layout

For a Go project, regardless of the architecture pattern used, it is recommended to establish `app` and `scripts` directories. The `app` directory contains the entry file for starting the Go project, usually `main.go`. The `scripts` directory can hold scripts used during build and deployment.

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

Next is the code section, divided into `entities`, `usecases`, and `adapters`.

- `entities`: Stores domain entities. For example, in a blogging system, domain entities might include users and articles.
- `usecases`: Stores business logic. In a blogging system, this might include user-related business logic (e.g., signup_user, signin_user, add_user, delete_user) and article-related business logic (e.g., add_article, show_article, delete_article).
- `adapters`: Stores adapter logic. Adapters connect business logic with external dependencies. For a blog providing services in a web form, an `http_adapter` is needed to encapsulate web services; to save articles to a database, a `db_adapter` is needed to connect.

Below is the project layout structure.

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

# Data Flow

Let's describe the call chain using a request to query an article.

- The user calls the `ShowArticleHandler` method of `WebAdapter` through the HTTP service.
- Since it involves article-related logic, `ShowArticleHandler` calls the `ShowArticle` method of `ArticleUsecase`.
- To query the article from the DB, `ArticleUsecase` calls the `GetArticle` method of `DBAdapter`.
- `DBAdapter`'s `GetArticle` queries the article content from MySQL and returns it to `ArticleUsecase`.
- `ArticleUsecase` returns to `WebAdapter`.
- `WebAdapter` returns the result to the user through the HTTP service.

![](/images/20211212_02.png)

# Code Example

To more clearly illustrate layering and architecture, I have published a sample project on GitHub. Interested readers can view the source code here: [https://github.com/simpleapples/go-clean-architecture](https://github.com/simpleapples/go-clean-architecture)

# Conclusion

Since Clean Architecture does not specify implementation details, the above layering and layout approach is just a reference, and there are numerous ways to practice it. For example, the Adapter layer can be subdivided into parallel Presenter+Gateway layers based on the type of external dependencies. In complex projects, more detailed layering can further refine the code. You can adjust the layering and layout according to your project's scale, and I won't elaborate further here.