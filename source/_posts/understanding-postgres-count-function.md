---
layout: post
title: 理解 PostgreSQL 的 count 函数的行为
date: 2019-04-19 11:25
comments: true
categories: DevOps
---

关于 count 函数的使用一直存在争议，尤其是在 MySQL 中，作为流行度越来越高的 PostgreSQL 是否也有类似的问题呢，我们通过实践来理解一下 PostgreSQL 中 count 函数的行为。

### 构建测试数据库

创建测试数据库，并创建测试表。测试表中有自增 ID、创建时间、内容三个字段，自增 ID 字段是主键。

```sql
create database performance_test;

create table test_tbl (id serial primary key, created_at timestamp, content varchar(512));
```

### 生成测试数据

使用 generate_series 函数生成自增 ID，使用 now() 函数生成 created_at 列，对于 content 列，使用了 repeat(md5(random()::text), 10) 生成 10 个 32 位长度的 md5 字符串。使用下列语句，插入 1000w 条记录用于测试。

```sql
performance_test=# insert into test_tbl select generate_series(1,10000000),now(),repeat(md5(random()::text),10);
INSERT 0 10000000
Time: 212184.223 ms (03:32.184)
```

### 由 count 语句引发的思考

默认情况下 PostgreSQL 不开启 SQL 执行时间的显示，所以需要手动开启一下，方便后面的测试对比。

```sql
\timing on
```

count(\*) 和 count(1) 的性能区别是经常被讨论的问题，分别使用 count(\*) 和 count(1) 执行一次查询。

```sql
performance_test=# select count(*) from test_tbl;
  count
----------
 10000000
(1 row)

Time: 115090.380 ms (01:55.090)

performance_test=# select count(1) from test_tbl;
  count
----------
 10000000
(1 row)

Time: 738.502 ms
```

可以看到两次查询的速度差别非常大，count(1) 真的有这么大的性能提升？接下来再次运行查询语句。

```sql
performance_test=# select count(*) from test_tbl;
  count
----------
 10000000
(1 row)

Time: 657.831 ms

performance_test=# select count(1) from test_tbl;
  count
----------
 10000000
(1 row)

Time: 682.157 ms
```

可以看到第一次查询时候会非常的慢，后面三次速度非常快并且时间相近，这里就有两个问题出现了：

- 为什么第一次查询速度这么慢？
- count(\*) 和 count(1) 到底存不存在性能差别？

### 查询缓存

使用 explain 语句重新执行查询语句

```sql
explain (analyze,buffers,verbose) select count(*) from test_tbl;
```

可以看到如下输出：

```
 Finalize Aggregate  (cost=529273.69..529273.70 rows=1 width=8) (actual time=882.569..882.570 rows=1 loops=1)
   Output: count(*)
   Buffers: shared hit=96 read=476095
   ->  Gather  (cost=529273.48..529273.69 rows=2 width=8) (actual time=882.492..884.170 rows=3 loops=1)
         Output: (PARTIAL count(*))
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=96 read=476095
         ->  Partial Aggregate  (cost=528273.48..528273.49 rows=1 width=8) (actual time=881.014..881.014 rows=1 loops=3)
               Output: PARTIAL count(*)
               Buffers: shared hit=96 read=476095
               Worker 0: actual time=880.319..880.319 rows=1 loops=1
                 Buffers: shared hit=34 read=158206
               Worker 1: actual time=880.369..880.369 rows=1 loops=1
                 Buffers: shared hit=29 read=156424
               ->  Parallel Seq Scan on public.test_tbl  (cost=0.00..517856.98 rows=4166598 width=0) (actual time=0.029..662.165 rows=3333333 loops=3)
                     Buffers: shared hit=96 read=476095
                     Worker 0: actual time=0.026..661.807 rows=3323029 loops=1
                       Buffers: shared hit=34 read=158206
                     Worker 1: actual time=0.030..660.197 rows=3285513 loops=1
                       Buffers: shared hit=29 read=156424
 Planning time: 0.043 ms
 Execution time: 884.207 ms
```

注意里面的 shared hit，表示命中了内存中缓存的数据，这就可以解释为什么后面的查询会比第一次快很多。接下来去掉缓存，并重启 PostgreSQL。

```bash
service postgresql stop
echo 1 > /proc/sys/vm/drop_caches
service postgresql start
```

重新执行 SQL 语句，速度慢了很多。

```
 Finalize Aggregate  (cost=529273.69..529273.70 rows=1 width=8) (actual time=50604.564..50604.564 rows=1 loops=1)
   Output: count(*)
   Buffers: shared read=476191
   ->  Gather  (cost=529273.48..529273.69 rows=2 width=8) (actual time=50604.508..50606.141 rows=3 loops=1)
         Output: (PARTIAL count(*))
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared read=476191
         ->  Partial Aggregate  (cost=528273.48..528273.49 rows=1 width=8) (actual time=50591.550..50591.551 rows=1 loops=3)
               Output: PARTIAL count(*)
               Buffers: shared read=476191
               Worker 0: actual time=50585.182..50585.182 rows=1 loops=1
                 Buffers: shared read=158122
               Worker 1: actual time=50585.181..50585.181 rows=1 loops=1
                 Buffers: shared read=161123
               ->  Parallel Seq Scan on public.test_tbl  (cost=0.00..517856.98 rows=4166598 width=0) (actual time=92.491..50369.691 rows=3333333 loops=3)
                     Buffers: shared read=476191
                     Worker 0: actual time=122.170..50362.271 rows=3320562 loops=1
                       Buffers: shared read=158122
                     Worker 1: actual time=14.020..50359.733 rows=3383583 loops=1
                       Buffers: shared read=161123
 Planning time: 11.537 ms
 Execution time: 50606.215 ms
```
shared read 表示没有命中缓存，通过这个现象可以推断出，上一小节的四次查询中，第一次查询没有命中缓存，剩下三次查询都命中了缓存。

#### count(1) 和 count(\*) 的区别

接下来探究 count(1) 和 count(\*) 的区别是什么，继续思考最开始的四次查询，第一次查询使用了 count(\*)，第二次查询使用了 count(1) ，却依然命中了缓存，不正是说明 count(1) 和 count(\*) 是一样的吗？

事实上，PostgreSQL 官方对于 is there a difference performance-wise between select count(1) and select count(\*)? 问题的回复也证实了这一点：

> Nope. In fact, the latter is converted to the former during parsing.[2]

既然 count(1) 在性能上没有比 count(\*) 更好，那么使用 count(\*) 就是更好的选择。

### sequence scan 和 index scan

接下来测试一下，在不同数据量大小的情况下 count(\*) 的速度，将查询语句写在 count.sql 文件中，使用 pgbench 进行测试。

```bash
pgbench -c 5 -t 20 performance_test -r -f count.sql
```

分别测试 200w - 1000w 数据量下的 count 语句耗时

数据大小|count耗时(ms)
--|--
200w|738.758
300w|1035.846
400w|1426.183
500w|1799.866
600w|2117.247
700w|2514.691
800w|2526.441
900w|2568.240
1000w|2650.434

绘制成耗时曲线

![](/upload/20190416_01.png)

曲线的趋势在 600w - 700w 数据量之间出现了转折，200w - 600w 是线性增长，600w 之后 count 的耗时就基本相同了。使用 explain 语句分别查看 600w 和 700w 数据时的 count 语句执行。

700w：

```sql
 Finalize Aggregate  (cost=502185.93..502185.94 rows=1 width=8) (actual time=894.361..894.361 rows=1 loops=1)
   Output: count(*)
   Buffers: shared hit=16344 read=352463
   ->  Gather  (cost=502185.72..502185.93 rows=2 width=8) (actual time=894.232..899.763 rows=3 loops=1)
         Output: (PARTIAL count(*))
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=16344 read=352463
         ->  Partial Aggregate  (cost=501185.72..501185.73 rows=1 width=8) (actual time=889.371..889.371 rows=1 loops=3)
               Output: PARTIAL count(*)
               Buffers: shared hit=16344 read=352463
               Worker 0: actual time=887.112..887.112 rows=1 loops=1
                 Buffers: shared hit=5459 read=118070
               Worker 1: actual time=887.120..887.120 rows=1 loops=1
                 Buffers: shared hit=5601 read=117051
               ->  Parallel Index Only Scan using test_tbl_pkey on public.test_tbl  (cost=0.43..493863.32 rows=2928960 width=0) (actual time=0.112..736.376 rows=2333333 loops=3)
                     Index Cond: (test_tbl.id < 7000000)
                     Heap Fetches: 2328492
                     Buffers: shared hit=16344 read=352463
                     Worker 0: actual time=0.107..737.180 rows=2344479 loops=1
                       Buffers: shared hit=5459 read=118070
                     Worker 1: actual time=0.133..737.960 rows=2327028 loops=1
                       Buffers: shared hit=5601 read=117051
 Planning time: 0.165 ms
 Execution time: 899.857 ms
```

600w：

```sql
 Finalize Aggregate  (cost=429990.94..429990.95 rows=1 width=8) (actual time=765.575..765.575 rows=1 loops=1)
   Output: count(*)
   Buffers: shared hit=13999 read=302112
   ->  Gather  (cost=429990.72..429990.93 rows=2 width=8) (actual time=765.557..770.889 rows=3 loops=1)
         Output: (PARTIAL count(*))
         Workers Planned: 2
         Workers Launched: 2
         Buffers: shared hit=13999 read=302112
         ->  Partial Aggregate  (cost=428990.72..428990.73 rows=1 width=8) (actual time=763.821..763.821 rows=1 loops=3)
               Output: PARTIAL count(*)
               Buffers: shared hit=13999 read=302112
               Worker 0: actual time=762.742..762.742 rows=1 loops=1
                 Buffers: shared hit=4638 read=98875
               Worker 1: actual time=763.308..763.308 rows=1 loops=1
                 Buffers: shared hit=4696 read=101570
               ->  Parallel Index Only Scan using test_tbl_pkey on public.test_tbl  (cost=0.43..422723.16 rows=2507026 width=0) (actual time=0.053..632.199 rows=2000000 loops=3)
                     Index Cond: (test_tbl.id < 6000000)
                     Heap Fetches: 2018490
                     Buffers: shared hit=13999 read=302112
                     Worker 0: actual time=0.059..633.156 rows=1964483 loops=1
                       Buffers: shared hit=4638 read=98875
                     Worker 1: actual time=0.038..634.271 rows=2017026 loops=1
                       Buffers: shared hit=4696 read=101570
 Planning time: 0.055 ms
 Execution time: 770.921 ms
```

根据以上现象推断，PostgreSQL 似乎在 count 的数据量小于数据表长度的某一比例时，才使用 index scan，通过查看官方 wiki 也可以看到相关描述：

> It is important to realise that the planner is concerned with minimising the total cost of the query. With databases, the cost of I/O typically dominates. For that reason, "count(\*) without any predicate" queries will only use an index-only scan if the index is significantly smaller than its table. This typically only happens when the table's row width is much wider than some indexes'.[3]

根据 Stackoverflow 上的回答，count 语句查询的数量大于表大小的 3/4 时候就会用使用全表扫描代替索引扫描[4]。

### 结论

1. 不要用 count(1) 或 count(列名) 代替 count(\*)
2. count 本身是非常耗时的
3. count 可能是 index scan 也可能是 sequence scan，取决于 count 数量占表大小的比例


### 参考资料

[1] [深入理解Postgres中的cache](https://www.cnblogs.com/flying-tiger/p/7885478.html)

[2] [Re: performance difference in count(1) vs. count(*)?](https://www.postgresql.org/message-id/11471.1027875769%40sss.pgh.pa.us)

[3] [Is "count(\*)" much faster now?](https://wiki.postgresql.org/wiki/Index-only_scans#Is_.22count.28.2A.29.22_much_faster_now.3F)

[4] [PostgreSQL not using index during count(\*)](https://dba.stackexchange.com/questions/126997/postgresql-not-using-index-during-count)
