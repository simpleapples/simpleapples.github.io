---
date: "2021-07-29T21:19:00+00:00"
title: "Issue with ORDER BY Not Working in MySQL Subqueries"
categories:
  - MySQL
---

By chance, I discovered that an SQL statement produced different results when executed on different MySQL instances.

# Problem Description

To simulate a business scenario, we create two tables: `product_tbl` for products and `product_operation_tbl` for product operation records. The structure and data are as follows:

![](/images/20210729_01.png)

![](/images/20210729_02.png)

Next, we need to query the latest modification time for all products using the following statement:

```sql
select t1.id, t1.name, t2.product_id, t2.created_at from product_tbl t1 left join (select * from product_operation_log_tbl order by created_at desc) t2 on t1.id = t2.product_id group by t1.id;
```

From the results, we can see that the subquery first sorts all records in `product_operation_log_tbl` in descending order by creation time (`created_at`), then performs a join with `product_tbl`, thus retrieving the latest modification time for the products.

![](/images/20210729_03.png)

On the MySQL instance in Region A, the query correctly retrieves the latest modification time for the products. However, on the MySQL instance in Region B, the modification time retrieved is the oldest instead of the latest. By simplifying the statement, it was found that the `order by created_at desc` in the subquery did not take effect on the instance in Region B.

# Investigation Process

Could the region affect MySQL's behavior? After investigation by the DBA, it was found that the MySQL in Region A is version 5.6, while the MySQL in Region B is version 5.7. Additionally, the following article was found:

[mysql 5.7 5.6 Sorting *mysql 5.6 upgrade to 5.7 causes ORDER BY in subquery to be ignored* Blog by Hotpot and Ideal - CSDN Blog](https://blog.csdn.net/weixin_42121058/article/details/113588551?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control)

According to the article, MySQL 5.7 ignores the `ORDER BY` clause in subqueries. Curiously, the MySQL version 8.0 used to simulate the business scenario did not exhibit this issue. Using Docker, MySQL instances of versions 5.6, 5.7, and 8.0 were started to repeat the operations, with results as follows:

![](/images/20210729_04.png)

It can be seen that only MySQL 5.7 ignored the `ORDER BY` in the subquery. Could it be that a bug was introduced in 5.7 and fixed in later versions?

# Root Cause

Further searching through documents and resources revealed the following description in the official forum:

> A "table" (and subquery in the FROM clause too) is - according to the SQL standard - an unordered set of rows. Rows in a table (or in a subquery in the FROM clause) do not come in any specific order. That's why the optimizer can ignore the ORDER BY clause that you have specified. In fact, SQL standard does not even allow the ORDER BY clause to appear in this subquery (we allow it, because ORDER BY ... LIMIT ... changes the result, the set of rows, not only their order).
> You need to treat the subquery in the FROM clause, as a set of rows in some unspecified and undefined order, and put the ORDER BY on the top-level SELECT.

The cause of the issue is clear: according to the SQL standard, a table is defined as an unordered set of data, and a SQL subquery is a temporary table. Based on this definition, the `ORDER BY` in a subquery is ignored. The official response also provides a solution: move the `ORDER BY` from the subquery to the outermost `SELECT` statement.

# Summary

- In the SQL standard, `ORDER BY` in subqueries is not effective.
- MySQL 5.7 exposed the issue by adhering to this aspect of the SQL standard, while in MySQL 5.6/8.0, this syntax still works.

# Reference Documents

[https://stackoverflow.com/questions/26372511/mysql-mariadb-order-by-inside-subquery](https://stackoverflow.com/questions/26372511/mysql-mariadb-order-by-inside-subquery)

[https://mariadb.com/kb/en/why-is-order-by-in-a-from-subquery-ignored/](https://mariadb.com/kb/en/why-is-order-by-in-a-from-subquery-ignored/)