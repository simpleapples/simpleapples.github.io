---
layout: post
title: MySQL 子查询中order by不生效问题
date: 2021-07-29 21:19
comments: true
categories: MySQL
---

一个偶然的机会，发现一条SQL语句在不同的MySQL实例上执行得到了不同的结果。

# 问题描述

创建商品表product_tbl和商品操作记录表product_operation_tbl两个表，来模拟下业务场景，结构和数据如下：

![](/upload/20210729_01.png)

![](/upload/20210729_02.png)

接下来需要查询所有商品最新的修改时间，使用如下语句：

```sql
select t1.id, t1.name, t2.product_id, t2.created_at  from product_tbl t1 left join (select * from product_operation_log_tbl order by created_at desc) t2 on t1.id = t2.product_id group by t1.id;
```

通过结果可以看到，子查询先将product_operation_log_tbl里的所有记录按创建时间(created_at)逆序，然后和product_tbl进行join操作，进而查询出的商品的最新修改时间。

![](/upload/20210729_03.png)

在区域A的MySQL实例上，查询商品最新修改时间可以得到正确结果，但是在区域B的MySQL实例上，得到的修改时间并不是最新的，而是最老的。通过对语句进行简化，发现是子查询中的order by created_at desc语句在区域B的实例上没有生效。

# 排查过程

难道区域会影响MySQL的行为？经过DBA排查，区域A的MySQL是5.6版，区域B的MySQL是5.7版，并且找到了这篇文章：

[mysql 5.7 5.6排序_mysql 5.6升级到5.7之后 子查询里面的order排序无效_火锅与理想的博客-CSDN博客](https://blog.csdn.net/weixin_42121058/article/details/113588551?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control)

根据文章的描述，MySQL 5.7版会忽略掉子查询中的order by语句，可令人疑惑的是，我们模拟业务场景的MySQL是8.0版，并没有出现这个问题。使用docker分别启动MySQL 5.6、5.7、8.0三个实例，来重复上面的操作，结果如下：

![](/upload/20210729_04.png)

可以看到，只有MySQL 5.7版忽略了子查询中的order by。有没有可能是5.7引入了bug，后续版本又修复了呢？

# 问题根因

继续搜索文档和资料，发现官方论坛中有这样一段描述：

> A "table" (and subquery in the FROM clause too) is - according to the SQL standard - an unordered set of rows. Rows in a table (or in a subquery in the FROM clause) do not come in any specific order. That's why the optimizer can ignore the ORDER BY clause that you have specified. In fact, SQL standard does not even allow the ORDER BY clause to appear in this subquery (we allow it, because ORDER BY ... LIMIT ... changes the result, the set of rows, not only their order).
You need to treat the subquery in the FROM clause, as a set of rows in some unspecified and undefined order, and put the ORDER BY on the top-level SELECT.

问题的原因清晰了，原来SQL标准中，table的定义是一个未排序的数据集合，而一个SQL子查询是一个临时的table，根据这个定义，子查询中的order by会被忽略。同时，官方回复也给出了解决方案：将子查询的order by移动到最外层的select语句中。

# 总结

- 在SQL标准中，子查询中的order by是不生效的
- MySQL 5.7由于在这个点上遵循了SQL标准导致问题暴露，而在MySQL 5.6/8.0中这种写法依然是生效的

# 参考文档

[https://stackoverflow.com/questions/26372511/mysql-mariadb-order-by-inside-subquery](https://stackoverflow.com/questions/26372511/mysql-mariadb-order-by-inside-subquery)

[https://mariadb.com/kb/en/why-is-order-by-in-a-from-subquery-ignored/](https://mariadb.com/kb/en/why-is-order-by-in-a-from-subquery-ignored/)