---
date: "2018-03-03T19:30:00+00:00"
title: "60行Python代码，实现多线程PDF转Word"
categories:
  - Python
---

工作中经常会遇到需要提取PDF文件中文字的情况，一个PDF还好，复制粘贴一下也花不了太多时间，如果需要把大量PDF转为Word，怎么办呢？

![](/upload/cant-do-it.jpg)

今天教大家用60行代码实现，多线程批量PDF转Word。没兴趣看具体过程可以直接拉到最后，有代码。

## 分解任务

把PDF转为Word，分几步？两步，第一步读取PDF文件，第二步写入Word文件。

![](/upload/two-steps.jpg)

是的，就是这么简单，借助Python第三方包，可以轻松实现上面两个过程，我们要用到pdfminer3k和python-docx这两个包。

## 读取PDF

```python
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


resource_manager = PDFResourceManager()
return_str = StringIO()
lap_params = LAParams()

device = TextConverter(resource_manager, return_str, laparams=lap_params)
process_pdf(resource_manager, device, file) // file是使用open方法打开的PDF文件句柄
device.close()

// 此处content就是转换为文字的PDF内容
content = return_str.getvalue()
```

content变量存储的就是我们从PDF文件中读取出的文字内容，可以看到，使用pdfminer3k可以轻松完成这个任务。接下来我们需要把文字内容写入成一个word文件。

## 写入Word

```python
from docx import Document


doc = Document()
for line in content.split('\n'):
    paragraph = doc.add_paragraph()
    paragraph.add_run(remove_control_characters(line))
doc.save(file_path)
content是我们前面读取出的文字内容，由于是讲整个PDF读成一个字符串，所以需要使用split方法将每一行分隔开，然后按行写入word，否则所有的文字会在同一行。同时这段代码使用了一个remove_control_characters函数，这个函数是需要自己实现的，目的是移除控制字符（换行符、制表符、转义符等），因为python-docx是不支持控制字符写入的。
def remove_control_characters(content):
    mpa = dict.fromkeys(range(32))
    return content.translate(mpa)
```

控制字符就是ASCII码在32以下的，所以我们使用str的translate方法，把32以下的字符移除就可以。

## 用是能用，但是太慢了！

![](/upload/too-slow.jpg)

如果我们用上面代码去转换100个PDF文件，就会发现速度慢到难以接受，每个PDF都需要花很长时间才能转换好，怎么办？别急，接下来我们引入多线程，同时转换多个PDF，可以有效加快转换速度。

```python
import os
from concurrent.futures import ProcessPoolExecutor


with ProcessPoolExecutor(max_workers=int(config['max_worker'])) as executor:
    for file in os.listdir(config['pdf_folder']):
        extension_name = os.path.splitext(file)[1]
        if extension_name != '.pdf':
            continue
        file_name = os.path.splitext(file)[0]
        pdf_file = config['pdf_folder'] + '/' + file
        word_file = config['word_folder'] + '/' + file_name + '.docx'
        print('正在处理: ', file)
        result = executor.submit(pdf_to_word, pdf_file, word_file)
        tasks.append(result)
while True:
    exit_flag = True
    for task in tasks:
        if not task.done():
            exit_flag = False
    if exit_flag:
        print('完成')
        exit(0)
```

代码中config是包含存储PDF文件夹地址和word文件夹地址的字典，使用Python标准库中的concurrent包，实现多进程，pdf_to_word方法是对上面读取PDF和写入word逻辑的封装。后面的while循环是查询任务是否进行完成。

## 效果

到这里，我们已经实现了多线程批量转换PDF为word文档。拿谋篇著名文章来试验一下，效果如图（左侧是转换后的word，右侧是PDF）：

![](/upload/pdf-and-word.jpg)

## 不想写代码？

本文介绍的所有代码，已经打包成了一个独立可运行的项目，存放在github，如果不想自己写代码，可以直接clone或下载github项目运行。项目地址如下（记得点star）：

[https://github.com/simpleapples/pdf2word](https://github.com/simpleapples/pdf2word)
