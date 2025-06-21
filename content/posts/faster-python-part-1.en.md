---
date: "2018-10-08T18:15:00+00:00"
title: "Translation | Faster Python (Part 1)"
categories:
  - Python
---

![](/images/20181008_11.png)

Faster Python ([Python Faster Way](http://pythonfasterway.org)) uses code examples to demonstrate how writing Python code can achieve higher performance. This article explains the code, selecting the most suitable approach from the perspectives of performance and readability.

### Example 1: String Formatting

![](/images/20181008_01.png)

- Worst/Best Time Ratio: **1.95**
- Recommendation: Use f-string for Python 3.7 or above, and the format method for other versions.
- Explanation: String formatting is a common scenario in code. Although using the + operator is optimal for concatenating a small number of strings, it results in the least readable code. If using Python 3.7 or above, f-string can solve this issue, offering better performance than both the format method and the % operator, while also being more readable than the + operator.

### Example 2: Dictionary Initialization

![](/images/20181008_02.png)

- Worst/Best Time Ratio: **1.83**
- Recommendation: Use literal initialization for dictionaries (and other collection types).
- Explanation: When initializing collection types in Python using literals, the interpreter directly calls bytecode like BUILD_MAP to create them. If using a constructor, it first needs to look up and execute the constructor method. Using literal initialization also makes Python code more concise.

### Example 3: Built-in Sorting Methods

![](/images/20181008_03.png)

- Worst/Best Time Ratio: **1.26**
- Recommendation: Decide which method to use based on whether you need to modify the original value.
- Explanation: The sorted and list.sort methods are built-in sorting methods in Python. The sorted method does not modify the original value, while list.sort sorts directly on the original value, modifying it. Comparing the performance difference between these two methods is not very meaningful.

### Example 4: Initializing Multiple Variables

![](/images/20181008_04.png)

- Worst/Best Time Ratio: **1.01**
- Recommendation: Prefer the second method.
- Explanation: From the bytecode, both methods are essentially the same except for the execution order, so their performance is very similar.

### Example 5: Comparing Multiple Variables

![](/images/20181008_05.png)

- Worst/Best Time Ratio: **1.11**
- Recommendation: Prefer the second method.
- Explanation: The first method offers a slight performance boost, but it's limited. In practice, it's rare to compare multiple variables consecutively, and the first method is not very Pythonic, so the second method is recommended.

### Example 6: Conditional Check for True

![](/images/20181008_06.png)

- Worst/Best Time Ratio: **1.17**
- Recommendation: Prefer the first method.
- Explanation: From the bytecode, the first method has the highest performance and is also more concise in syntax.

### Example 7: Conditional Check for False

![](/images/20181008_07.png)

- Worst/Best Time Ratio: **1.10**
- Recommendation: Prefer the first method.
- Explanation: From the bytecode, the first method has the highest performance. From a syntax perspective, writing if not as in the second and third methods is not recommended.

### Example 8: Checking if a List is Empty

![](/images/20181008_08.png)

- Worst/Best Time Ratio: **1.55**
- Recommendation: Prefer the first two methods based on specific needs.
- Explanation: The first two methods have higher performance and are more concise. An empty list a is not equal to None, so using if a is None cannot determine if a list is empty.

### Example 9: Checking if an Object is Empty

![](/images/20181008_09.png)

- Worst/Best Time Ratio: **1.00**
- Recommendation: Prefer the first two methods based on specific needs.
- Explanation: The reasoning is the same as the previous example.

### Example 10: Iterating Over Iterable Objects

![](/images/20181008_10.png)

- Worst/Best Time Ratio: **1.12**
- Recommendation: Choose based on specific circumstances.
- Explanation: The performance difference between the two is minimal. Using the enumerate method allows you to obtain the index directly without needing to get the object's length.

### Reference Articles

- [Python Faster Way](http://pythonfasterway.org)