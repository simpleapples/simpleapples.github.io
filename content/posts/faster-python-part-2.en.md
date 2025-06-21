---
date: "2018-10-25T18:20:00+00:00"
title: "Translation | Faster Python (Part 2)"
categories:
  - Python
---

![](/images/20181025_11.png)

Faster Python ([Python Faster Way](http://pythonfasterway.org)) uses code examples to demonstrate how writing Python code can lead to higher performance. This article explains the code, choosing the most suitable approach from the perspectives of performance and readability.

<!-- more -->

### Example 11: String Concatenation

![](/images/20181025_01.png)

- Worst/Best Time Ratio: **1.15**
- Recommendation: Use `join` when concatenating multiple (more than 3) strings at once; otherwise, use the plus sign or f-string.
- Explanation: This is another string concatenation issue, but the example is not well chosen. `join` is suitable for scenarios where multiple strings are concatenated at once, which is much faster than using the plus sign to concatenate multiple strings (the plus sign is equivalent to concatenating one by one).

### Example 12: Number Formatting

![](/images/20181025_02.png)

- Worst/Best Time Ratio: **1.29**
- Recommendation: For complex formatting, it is recommended to use the `format` method; to convert numbers to strings, directly use the `str` method.
- Explanation: Converting numbers to strings using the `str` method is faster than using the `format` method, because the `format` method supports adding rules during conversion, such as converting numbers to currency format (adding a comma separator every three digits).

### Example 13: Getting the Length of Built-in List Types

![](/images/20181025_03.png)

- Worst/Best Time Ratio: **1.20**
- Recommendation: Use the `len()` method.
- Explanation: When calling the `len()` method, the system actually calls the object's built-in **len** method. From this perspective, directly calling **len** should be faster than the `len()` method. However, when `len()` is used on built-in list methods, the Python interpreter optimizes it by directly returning the variable storing the length information in the list object, without calling **len**.

### Example 14: Integer Type Operations

![](/images/20181025_04.png)

- Worst/Best Time Ratio: **2.63**
- Recommendation: Do not directly call magic methods like **add**.
- Explanation: For integer types, calling magic methods to perform operations is much slower than directly using operators. When using operators, the Python interpreter directly calls the operation methods in the C-implemented `operator` package, so the speed is very fast. Using magic methods involves additional operations at the Python level to call magic methods like **add**.

### Example 15: Operator Overloading for Custom Types

![](/images/20181025_05.png)

- Worst/Best Time Ratio: **1.06**
- Recommendation: Do not directly call magic methods like **add**.
- Explanation: For objects that have overloaded operators, there are no corresponding C-implemented operation methods, so directly calling magic methods will be faster.

### Example 16: Summing the Results of `range`

![](/images/20181025_06.png)

- Worst/Best Time Ratio: **2.95**
- Recommendation: The first method is recommended.
- Explanation: Compared to the first method, the third method iterates over `range` to first generate a list, then passes the list to `sum`, making it the slowest. The first method directly passes the iterator to `sum`, eliminating the process of iterating to generate a list. The second method, compared to the first, implements summation at the Python level, whereas `sum` implements it at the C level, so it is not as fast as the first method.

### Example 17: Difference Between `for` Loop and Expression for List Construction

![](/images/20181025_07.png)

- Worst/Best Time Ratio: **2.05**
- Recommendation: Expression construction is recommended.
- Explanation: Both methods logically appear the same, iterating over the `range` iterator to generate a list. However, the expression constructs a loop at the bytecode level to generate it, while the second method creates a list at the Python level and continuously appends, which is less performant than the first method.

### Example 18: Difference Between `for` Loop and Expression for Dictionary Construction

![](/images/20181025_08.png)

- Worst/Best Time Ratio: **1.49**
- Recommendation: Expression is recommended.
- Explanation: The `dict` update method is suitable for merging two dictionaries, meaning it can merge multiple keys at once, so it is slower than directly accessing keys. According to the test in the image, at the scale of 100, the speed of expression generation is slower, but at larger scales, the advantage of expressions becomes apparent and is more Pythonic. The expression method generates loops at the bytecode level, so theoretically it is faster than generating loops at the Python level to construct dictionaries. Why does bytecode not have an advantage in small-scale scenarios? According to the bytecode disassembled by `dis`, the expression construction first performs `MAKE_FUNCTION` and then `CALL_FUNCTION`, which incurs some basic overhead. When the scale is small, this basic overhead accounts for a high proportion. The larger the scale, the lower the proportion of this basic overhead, and the more apparent the advantage of the expression method becomes.

### Example 19: Difference Between `for` Loop and Expression for Dictionary Construction

![](/images/20181025_09.png)

- Worst/Best Time Ratio: **2.89**
- Recommendation: Expression construction is recommended.
- Explanation: The reason is the same as the previous example.

### Example 20: Conversion to Boolean Value

![](/images/20181025_10.png)

- Worst/Best Time Ratio: **N/A**
- Recommendation: Choose based on specific circumstances.
- Explanation: There seems to be nothing much to say about this comparison. The time difference is mainly due to the different costs of constructing the `a` object.

### Reference Articles

- [Python Faster Way](http://pythonfasterway.org)