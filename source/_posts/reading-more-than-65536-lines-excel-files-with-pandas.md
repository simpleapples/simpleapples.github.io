---
layout: post
title: 使用 Pandas 读取超过 65536 行的 Excel 文件？
date: 2019-08-22 15:50
comments: true
categories: Python
---

### 问题描述

使用 Pandas 的 `read_excel` 方法读取一个 16 万行的 Excel 文件报 `AssertionError` 错误：

```
  "/Users/Zzy/Desktop/test/csv_test/venv/lib/python3.7/site-packages/xlrd/xlsx.py", line 637, in do_row
    assert 0 <= self.rowx < X12_MAX_ROWS
AssertionError
```

<!-- more -->

### 背后原理

Excel 文件的格式曾经发生过一次变化，在 Excel 2007 以前，使用扩展名为 `.xls` 格式的文件，这种文件格式是一种特定的二进制格式，最多支持 65,536 行，256 列表格。从 Excel 2007 版开始，默认采用了基于 XML 的新的文件格式 `.xlsx`，支持的表格行数达到了 1,048,576，列数达到了 16,384。需要注意的是，将 `.xlsx` 格式的文件转换为 `.xls` 格式的文件时，65536 行和 256 列之后的数据都会被丢弃。

版本|最大行数|最大列数|文件格式
--|--|--|--
早于 Excel 2007 的版本|65,536|256|.xls
Excel 2007 及以后版本|1,048,576|16,384|.xlsx

Pandas 读取 Excel 文件的引擎是 `xlrd`，`xlrd` 虽然同时支持 `.xlsx` 和 `.xls` 两种文件格式，但是在源码文件 [xlrd/sheet.py](https://github.com/python-excel/xlrd/blob/master/xlrd/sheet.py) 中限制了读取的 Excel 文件行数必须小于 65536，列数必须小于 256。

```python
if self.biff_version >= 80:
    self.utter_max_rows = 65536
else:
    self.utter_max_rows = 16384
self.utter_max_cols = 256
```

这就导致，即使是 `.xlsx` 格式的文件，`xlrd` 依然不支持读取 65536 行以上的 Excel 文件（源码中还有一个行数限制是 16384，这是因为 Excel 95 时代，`xls` 文件所支持的最大行数是 16384）。

### 解决办法

`openpyxl` 是一个专门用来操作 `.xlsx` 格式文件的 Python 库，和 `xlrd` 相比它对于最大行列数的支持和 `.xlsx` 文件所定义的最大行列数一致。

首先安装 `openpyxl`：

```bash
pip install openpyxl
```

Pandas 的 read_excel 方法中，有 `engine` 字段，可以指定所使用的处理 Excel 文件的引擎，填入 `openpyxl`，再读取文件就可以了。

```python
import pandas as pd


df = pd.read_excel('./data.xlsx', engine='openpyxl')
print(len(df))  # 160000
```

### 参考文档

[https://en.wikipedia.org/wiki/Microsoft_Excel](https://en.wikipedia.org/wiki/Microsoft_Excel)

[https://office-watch.com/2010/excel-a-history-of-rows-and-columns/](https://office-watch.com/2010/excel-a-history-of-rows-and-columns/)

[https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html)

[https://openpyxl.readthedocs.io](https://openpyxl.readthedocs.io)

[https://github.com/python-excel/xlrd/](https://github.com/python-excel/xlrd/)


