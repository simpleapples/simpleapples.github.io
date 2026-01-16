import os
import re

def replace_image_links(content: str) -> str:
    # 匹配 ![alt](/images/filename.ext)，允许 alt 内容非空
    pattern = re.compile(r'!\[.*?\]\(/images/([\w\-.]+\.(?:png|jpg|jpeg|gif))\)')

    def repl(match):
        filename = match.group(1)
        return f'{{ $image := .Resources.Get "images/{filename}" }}'

    return pattern.sub(repl, content)

def process_file(src_path, dst_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = replace_image_links(content)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Processed: {dst_path}")

def process_folder(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.md'):
            src_path = os.path.join(input_folder, filename)
            dst_path = os.path.join(output_folder, filename)
            process_file(src_path, dst_path)


# 替换成你的路径
input_folder = "/Users/zzy/Documents/workspace/blog/content/posts"
output_folder = "/Users/zzy/Documents/workspace/blog/content/posts"
process_folder(input_folder, output_folder)