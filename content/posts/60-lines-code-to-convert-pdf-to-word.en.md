---
date: "2018-03-03T19:30:00+00:00"
title: "Convert PDF to Word Using 60 Lines of Python Code with Multithreading"
categories:
  - Python
---

In the workplace, we often encounter situations where we need to extract text from PDF files. For a single PDF, copying and pasting doesn't take much time, but what if you need to convert a large number of PDFs to Word documents?

![](/images/cant-do-it.jpg)

Today, I'll teach you how to use 60 lines of code to achieve multithreaded batch PDF to Word conversion. If you're not interested in the detailed process, you can skip to the end for the code.

## Task Breakdown

How do you convert a PDF to Word? In two steps: first, read the PDF file, and second, write to a Word file.

![](/images/two-steps.jpg)

Yes, it's that simple. With the help of Python third-party packages, we can easily accomplish these two processes. We'll use the packages pdfminer3k and python-docx.

## Reading PDF

```python
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


resource_manager = PDFResourceManager()
return_str = StringIO()
lap_params = LAParams()

device = TextConverter(resource_manager, return_str, laparams=lap_params)
process_pdf(resource_manager, device, file) // file is the PDF file handle opened with the open method
device.close()

// Here, content is the text content converted from the PDF
content = return_str.getvalue()
```

The `content` variable stores the text content we read from the PDF file. As you can see, using pdfminer3k makes this task easy. Next, we need to write the text content into a Word file.

## Writing to Word

```python
from docx import Document


doc = Document()
for line in content.split('\n'):
    paragraph = doc.add_paragraph()
    paragraph.add_run(remove_control_characters(line))
doc.save(file_path)
```

`content` is the text content we read earlier. Since the entire PDF is read as a single string, we need to use the `split` method to separate each line and write them into the Word document line by line; otherwise, all the text will be on the same line. This code also uses a `remove_control_characters` function, which you need to implement yourself. Its purpose is to remove control characters (such as newline, tab, escape characters) because python-docx does not support writing control characters.

```python
def remove_control_characters(content):
    mpa = dict.fromkeys(range(32))
    return content.translate(mpa)
```

Control characters are those with ASCII codes below 32, so we use the `translate` method of `str` to remove characters below 32.

## It Works, But It's Too Slow!

![](/images/too-slow.jpg)

If we use the above code to convert 100 PDF files, we'll find the speed unbearably slow, with each PDF taking a long time to convert. What can we do? Don't worry, next we'll introduce multithreading to convert multiple PDFs simultaneously, which can effectively speed up the conversion process.

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
        print('Processing: ', file)
        result = executor.submit(pdf_to_word, pdf_file, word_file)
        tasks.append(result)
while True:
    exit_flag = True
    for task in tasks:
        if not task.done():
            exit_flag = False
    if exit_flag:
        print('Completed')
        exit(0)
```

In the code, `config` is a dictionary containing the addresses of the folders storing PDF and Word files. We use the `concurrent` package from the Python standard library to implement multiprocessing. The `pdf_to_word` method encapsulates the logic for reading PDFs and writing to Word. The while loop at the end checks whether the tasks have been completed.

## Results

By now, we have achieved multithreaded batch conversion of PDFs to Word documents. Let's test it with a famous article. The effect is shown in the image (left is the converted Word document, right is the PDF):

![](/images/pdf-and-word.jpg)

## Don't Want to Write Code?

All the code introduced in this article has been packaged into a standalone runnable project and stored on GitHub. If you don't want to write the code yourself, you can directly clone or download the GitHub project and run it. The project address is as follows (remember to star it):

[https://github.com/simpleapples/pdf2word](https://github.com/simpleapples/pdf2word)
