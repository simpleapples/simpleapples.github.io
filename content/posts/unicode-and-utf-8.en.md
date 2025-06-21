---
date: "2018-12-07T15:22:00+00:00"
title: "Unicode and UTF-8"
categories:
  - Tech
---

![](/images/20181207_01.jpg)

The concepts of Unicode and UTF-8 are fundamental and important, yet they are often overlooked.

<!-- more -->

### Character Set

In computer systems, all data is stored in binary, and all operations are represented in binary. Human languages and symbols also need to be converted into binary form to be stored in computers, which necessitates a mapping table from human language to binary encoding. This mapping table is called a character set.

### ASCII

The earliest character set was called the American Standard Code for Information Interchange, abbreviated as ASCII, established by the American National Standard Institute. In the ASCII character set, the letter `A` corresponds to the character code `65`, which converts to binary as `0100 0001`. Since binary representation is relatively long, hexadecimal `41` is often used.

### GB2312, GBK

The ASCII character set specifies a total of 128 characters but does not cover characters beyond Western letters. When computers need to display and store Chinese characters, a character set for encoding Chinese is required. GB 2312 was created to solve Chinese encoding, published by the National Standard Committee. Considering that Western letters are often needed in the Chinese context, GB 2312 is also backward compatible with ASCII, meaning Western letters use the same codes as in ASCII. However, GB 2312 only covers over 6,000 Chinese characters, leaving many unaccounted for, leading to the development of GBK and GB 18030, both of which are extensions of GB 2312.

### Unicode

As seen, for Simplified Chinese alone, at least three character sets have emerged, and for Traditional Chinese, there are character sets like BIG5. Almost every language requires its own character set, each with its own encoding rules, often incompatible with one another. The same character may have different codes in different character sets, necessitating the use of the same character encoding on both sides to avoid garbled text during cross-language communication. To address the limitations of traditional character encoding, Unicode was created. Unicode, short for Universal Multiple-Octet Coded Character Set (UCS), includes all the world's characters and symbols in one character set, with unified encoding to eliminate the problem of garbled text from different encodings.

### Character Encoding UTF-8

Unicode unifies the encoding of all characters and is a Character Set. A character set only assigns a unique number to each character but does not specify how to store it. A character numbered `65` requires only one byte, but a character numbered `40657` requires two bytes, and characters further back may need three or even four bytes.

At this point, the rules for storing Unicode characters become crucial. We could stipulate that a character uses four bytes, or 32 bits, which would cover all characters currently included in Unicode. This encoding method is called UTF-32 (UTF stands for UCS Transformation Format). Although the UTF-32 rule is simple, its drawback is evident. Suppose we use UTF-32 and ASCII to encode a document containing only Western letters; the former would require four times the space of the latter (ASCII requires only one byte per character).

In storage and network transmission, the more space-efficient variable-length encoding method UTF-8 is commonly used. UTF-8 represents Unicode characters using 1 to 4 bytes.

The encoding rules for UTF-8 are as follows (the numbers after U+ represent Unicode character codes):

```
U+ 0000 ~ U+ 007F: 0XXXXXXX
U+ 0080 ~ U+ 07FF: 110XXXXX 10XXXXXX
U+ 0800 ~ U+ FFFF: 1110XXXX 10XXXXXX 10XXXXXX
U+10000 ~ U+1FFFF: 11110XXX 10XXXXXX 10XXXXXX 10XXXXXX
```

As seen, UTF-8 achieves variable length through the number of leading marker bits. Single-byte characters occupy only one byte, achieving backward compatibility with ASCII. Like UTF-32, it includes all characters in Unicode, while effectively reducing space usage during storage and transmission.