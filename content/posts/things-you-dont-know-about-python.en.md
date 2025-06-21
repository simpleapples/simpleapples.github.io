---
date: "2018-06-11T11:50:00+00:00"
title: "The Evolution of Python String Formatting You Didn't Know"
categories:
  - Python
---

![](/images/20180611_01.jpg)

String formatting is a fundamental and frequently used feature in every programming language. Those learning Python are likely familiar with using the % syntax for string formatting. However, to make this common feature more convenient, the language itself has iterated on string formatting methods.

# Before Python 2.6: % Operator

Before Python 2.6, there was only one method for string formatting: the % (also known as the modulo) operator. The % operator supports both unicode and str types of Python strings, similar to the sprintf() method in C. Here’s an example of using % to format a string:

```python
print("I'm %s. I'm %d years old" % ('Tom', 27))
```

A string is used as a template before the % symbol, with placeholder markers for formatting. After the %, a tuple or dict is used to pass the values to be formatted. The placeholders control the display format, as shown in the table below:

| Placeholder | Description                                               |
| ----------- | --------------------------------------------------------- |
| %d          | Decimal integer                                           |
| %i          | Decimal integer                                           |
| %o          | Octal integer                                             |
| %u          | Unsigned integer                                          |
| %x          | Unsigned hexadecimal (lowercase)                          |
| %X          | Unsigned hexadecimal (uppercase)                          |
| %e          | Floating point (scientific notation, lowercase)           |
| %E          | Floating point (scientific notation, uppercase)           |
| %f          | Floating point number                                     |
| %F          | Floating point number                                     |
| %g          | Floating point, uses scientific notation if > 4 decimals  |
| %G          | Floating point, uses scientific notation if > 4 decimals  |
| %c          | Single character                                          |
| %r          | String (uses repr() method)                               |
| %s          | String (uses str() method)                                |

Beyond specifying data types, the % operator also supports more complex format control:

```
%[key][alignment][width].[precision]type
```

| Name       | Description                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------- |
| Key        | Used for dictionary assignment; not needed if a tuple is passed after the % symbol                |
| Alignment  | Four types: +, -, 0, ' '; + shows sign, - left-aligns, space adds a space on the left, 0 pads with 0 |
| Width      | Specifies the length of the formatted string, padded with 0 or spaces if necessary                |
| Precision  | Number of digits after the decimal point                                                          |
| Type       | Data type (refer to placeholder types)                                                            |

For example, `print('%053f' % '12.34')` outputs `0012.340`.

# Python 2.6: format Function

With Python 2.6, a new string formatting method was introduced: the str.format() function. Compared to the % operator, the format function uses {} and : instead of %, offering more power. It supports various mapping methods such as positional, keyword, object attribute, and index mapping. Parameters can be used out of order, omitted, or reused multiple times. Here are some examples:

```python
'{1} {0}'.format('abc', 123)  # Positional mapping out of order, outputs '123 abc'

'{} {}'.format('abc', 123)  # No parameter names needed, outputs 'abc 123'

'{1} {0} {1}'.format('abc', 123)  # Parameters can be reused, outputs '123 abc 123'

'{name} {age}'.format(name='tom', age=27)  # Keyword mapping, outputs 'tom 27'

'{person.name} {person.age}'.format(person=person)  # Object attribute mapping, outputs 'tom 27'

'{0[1]} {0[0]}'.format(lst)  # Index mapping
```

As seen, the format function is more convenient than the % operator, requiring less memorization of placeholder meanings and improving code readability. For complex format control, the format function offers more powerful options:

```
[[fill character]alignment][sign][#][width][,][.precision][type]
```

For example:

```
'{:S^+#016,.2f}'.format(1234)  # Outputs 'SSS+1,234.00SSSS'
```

Let's break down the format control parameters using the example above:

| Type       | Description                                                                                     | Example Explanation                             |
| :--------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Fill       | Defaults to space if not specified                                                              | S indicates filling with S                      |
| Alignment  | ^ for center, < for left, > for right                                                           | ^ centers, filling with the fill character      |
| Sign       | + shows sign (positive shows +, negative shows -), space adds a space for alignment             | + shows space before positive numbers           |
| #          | Shows 0b, 0o, 0x for binary, octal, hexadecimal respectively                                    | # shows base symbol; not shown for decimal      |
| Width      | Specifies output string width                                                                   | 16 sets string width to 16, padded if necessary |
| ,          | Uses comma as a thousand separator                                                              | , uses thousand separator                       |
| Precision  | Number of digits after the decimal point                                                        | .2 sets precision to 2 digits                   |
| Type       | s for string, c for character, b/o/d for binary/octal/decimal, x/X for lowercase/uppercase hex, e/E for scientific notation, f for float | f indicates floating-point number               |

The format function enriches format control options over %, making output easier.

# Python 3.6: f-string

Many who have used ES6 are familiar with template strings, which allow embedding variables directly into strings for formatting. Python 3.6 introduced a similar feature: Formatted String Literals, or f-strings.

An f-string starts with f'' and is similar to u'' and b''. The string content is formatted like the format method, but variables can be directly embedded, enhancing readability. For example:

```python
amount = 1234
f'Please transfer {amount:,.2f} to me'  # 'Please transfer 1,234.00 to me'
```

Additionally, f-strings offer better performance than % and format. Let's conduct a simple test, executing the following statement 10,000 times using the % operator, format, and f-string:

```python
'My name is %s and I'm %s years old.' % (name, age)
'My name is {} and I'm {} years old.'.format(name, age)
f'My name is {name} and I'm {age} years old.'
```

The results are as follows:

![](/images/20180611_02.png)

# Conclusion

If your project uses Python 3.6 or later, f-string formatting is the preferred method. It maintains powerful functionality while being more semantically understandable, with significant performance improvements. If your project hasn't upgraded to 3.6 or uses 2.7, it's recommended to use format. While it doesn't offer performance advantages, it is more semantically understandable and powerful than the % operator.