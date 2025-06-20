---
date: "2019-08-22T15:50:00+00:00"
title: "探究 Pandas 读取 Excel 文件报错问题"
categories:
  - Python
---

### 问题描述

使用 Pandas 的 `read_excel` 方法读取一个 16 万行的 Excel 文件报 `AssertionError` 错误：

```
  "/Users/XXX/excel_test/venv/lib/python3.7/site-packages/xlrd/xlsx.py", line 637, in do_row
    assert 0 <= self.rowx < X12_MAX_ROWS
AssertionError
```

<!-- more --> 

### 背后原理

Excel 文件有两种默认格式，在 Excel 2007 以前，使用扩展名为 `.xls` 格式的文件，这种文件格式是一种特定的二进制格式，最多支持 65,536 行（在 Excel 97 之前支持的最大行数是 16,384），256 列表格。从 Excel 2007 版开始，默认采用了基于 XML 的新的文件格式 `.xlsx`，支持的表格行数达到了 1,048,576，列数达到了 16,384。需要注意的是，将 `.xlsx` 格式的文件转换为 `.xls` 格式的文件时，65,536 行和 256 列之后的数据都会被丢弃。

版本|最大行数|最大列数|文件格式
--|--|--|--
Excel 97 之前|16,384|256|.xls
Excel 97 到 Excel 2003|65,536|256|.xls
Excel 2007 及以后版本|1,048,576|16,384|.xlsx

Pandas 读取 Excel 文件的引擎是 `xlrd`，`xlrd` 在读取 Excel 文件时，[`xlrd/xlsx.py`](https://github.com/python-excel/xlrd/blob/master/xlrd/xlsx.py) 文件的 637 行会对行号做断言，判断行号是否在 0 - 1,048,576（Excel支持的最大行数） 的范围内。这段代码是这样的：

```python
row_number = row_elem.get('r')
if row_number is None: # Yes, it's optional.
    self.rowx += 1
    explicit_row_number = 0
    if self.verbosity and not self.warned_no_row_num:
        self.dumpout("no row number; assuming rowx=%d", self.rowx)
        self.warned_no_row_num = 1
else:
    self.rowx = row_number - 1
    explicit_row_number = 1
assert 0 <= self.rowx < X12_MAX_ROWS
```

代码会从 Excel 文件中获取 row_number，这个 row_number 是每一行的行号，正常文件行号从 1 开始，而出现问题的文件行号从 0 开始，当行号为 0，进入 else 语句，导致越界问题。

### 解决办法

除了 `xlrd`， Pandas 还支持 `openpyxl`（0.25 版），`openpyxl` 是一个专门用来操作 `.xlsx` 格式文件的 Python 库，和 `xlrd` 相比它的速度会慢一些，但是不会碰到上面所说的问题。这是 openpyxl 中 [`reader/excel.py`](https://bitbucket.org/openpyxl/openpyxl/src/default/openpyxl/reader/excel.py) 文件处理行的代码：

```python
def parse_row(self, row):
    attrs = dict(row.attrib)

    if "r" in attrs:
        self.max_row = int(attrs['r'])
    else:
        self.max_row += 1
    keys = set(attrs)
    for key in keys:
        if key.startswith('{'):
            del attrs[key]

    keys = set(attrs)
    if keys != set(['r', 'spans']) and keys != set(['r']):
        # don't create dimension objects unless they have relevant information
        self.row_dimensions[attrs['r']] = attrs

    cells = [self.parse_cell(el) for el in row]
    return self.max_row, cells
```

openpyxl 在处理行时，并没有对行号进行断言，即使行号第一位是 0，也不会导致报错，**但这会导致第一行数据的缺失，需要进行额外处理**。

### 使用 Pandas + openpyxl 读取 Excel 文件

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

[https://office-watch.com/2010/excel-a-history-of-rows-and-columns/](https://office-watch.com/2010/excel-a-history-of-rows-and-columns/)

[https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html)

[https://github.com/python-excel/xlrd/](https://github.com/python-excel/xlrd/)

[https://bitbucket.org/openpyxl/openpyxl/src](https://bitbucket.org/openpyxl/openpyxl/src)
