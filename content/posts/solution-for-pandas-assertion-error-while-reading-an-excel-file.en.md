---
date: "2019-08-22T15:50:00+00:00"
title: "Exploring Pandas Read Excel File Error"
categories:
  - Python
---

### Problem Description

Using Pandas' `read_excel` method to read an Excel file with 160,000 rows results in an `AssertionError`:

```
  "/Users/XXX/excel_test/venv/lib/python3.7/site-packages/xlrd/xlsx.py", line 637, in do_row
    assert 0 <= self.rowx < X12_MAX_ROWS
AssertionError
```

<!-- more --> 

### Underlying Principle

Excel files come in two default formats. Before Excel 2007, files used the `.xls` format, a specific binary format supporting up to 65,536 rows (16,384 rows before Excel 97) and 256 columns. Starting with Excel 2007, a new XML-based format `.xlsx` was adopted, supporting up to 1,048,576 rows and 16,384 columns. Note that when converting a `.xlsx` file to `.xls`, data beyond 65,536 rows and 256 columns will be lost.

Version|Max Rows|Max Columns|File Format
--|--|--|--
Before Excel 97|16,384|256|.xls
Excel 97 to Excel 2003|65,536|256|.xls
Excel 2007 and later|1,048,576|16,384|.xlsx

Pandas uses `xlrd` as the engine to read Excel files. In `xlrd`, the file [`xlrd/xlsx.py`](https://github.com/python-excel/xlrd/blob/master/xlrd/xlsx.py) at line 637 asserts that the row number is within the range of 0 - 1,048,576 (the maximum number of rows supported by Excel). The code is as follows:

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

The code retrieves the row_number from the Excel file. Normally, row numbers start from 1, but in the problematic file, they start from 0, causing an out-of-bounds issue when entering the else statement.

### Solution

Besides `xlrd`, Pandas also supports `openpyxl` (from version 0.25), a Python library specifically for handling `.xlsx` files. While `openpyxl` is slower than `xlrd`, it does not encounter the aforementioned issue. Here is the code handling rows in `openpyxl`'s [`reader/excel.py`](https://bitbucket.org/openpyxl/openpyxl/src/default/openpyxl/reader/excel.py):

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

`openpyxl` does not assert the row number, so even if the first row number is 0, it won't cause an error. **However, this will result in the loss of the first row of data, requiring additional handling.**

### Using Pandas + openpyxl to Read Excel Files

First, install `openpyxl`:

```bash
pip install openpyxl
```

In Pandas' `read_excel` method, there is an `engine` parameter to specify the engine for processing Excel files. Set it to `openpyxl` to read the file.

```python
import pandas as pd

df = pd.read_excel('./data.xlsx', engine='openpyxl')
print(len(df))  # 160000
```

### References

[https://office-watch.com/2010/excel-a-history-of-rows-and-columns/](https://office-watch.com/2010/excel-a-history-of-rows-and-columns/)

[https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html)

[https://github.com/python-excel/xlrd/](https://github.com/python-excel/xlrd/)

[https://bitbucket.org/openpyxl/openpyxl/src](https://bitbucket.org/openpyxl/openpyxl/src)