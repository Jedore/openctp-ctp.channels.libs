# Generate html files for channels.
import os
import shutil
import time
from hashlib import md5

from natsort import natsorted


def traverse_dll(root_dir: str):
    for dir_path, dir_names, file_names in os.walk(root_dir):
        # 排序
        dir_names = natsorted(dir_names)
        file_names = natsorted(file_names)

        contents = []
        for name in dir_names:
            line = f'\n<a href="{name}/">{name}</a>'
            contents.append(line)

        for name in file_names:
            if name == 'index.html' or name == 'favicon.png':
                continue

            # 删除 lib 文件
            if '.lib' in name:
                os.remove(os.path.join(dir_path, name))
                continue

            # 添加 lib 前缀
            if '.so' in name and 'lib' not in name:
                shutil.move(os.path.join(dir_path, name), os.path.join(dir_path, 'lib' + name))
                name = 'lib' + name

            with open(os.path.join(dir_path, name), 'rb') as f:
                md5_string = md5(f.read()).hexdigest()

            line = f'\n<a class="lib" href="{name}">{name}</a> {" " * (52 - len(name))}{md5_string}'
            contents.append(line)

        gen_html(os.path.join(dir_path, 'index.html'), dir_path.replace('\\', '/'), contents)


def gen_html(filename: str, title: str, contents: list):
    headers = [
        '<html><head>\n',
        '<title>openctp-ctp multi channels libs</title>\n',
        f'<link rel="icon" href="/favicon.png">\n',
        '</head>\n',
        '<body>\n',
        f'<h1>Index of {title}</h1>\n',
        '<h4>Author: <a href="https://github.com/Jedore" target="_black">Jedore</a></h4>\n',
        '<hr><pre>\n',
        '<a href="/">/</a>\n',
        '<a href="../">../</a>',
    ]
    tails = [
        '\n</pre><hr></body></html>'
    ]
    with open(filename, 'w', encoding='utf8') as fp:
        fp.writelines(headers + contents + tails)


if __name__ == '__main__':
    start = time.time()
    traverse_dll('channels')
    print('Duration:', int(time.time() - start), 'seconds')
