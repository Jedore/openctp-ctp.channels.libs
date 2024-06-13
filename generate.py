# Generate html files for channels.
import os
import time
from hashlib import md5


def traverse_dll(root_dir: str):
    for dir_path, dir_names, file_names in os.walk(root_dir):
        contents = []
        for name in dir_names:
            line = f'\n<a href="{name}/">{name}</a>'
            contents.append(line)

        for name in file_names:
            if name == 'index.html':
                continue

            md5()

            line = f'\n<a href="{name}">{name}</a>'
            contents.append(line)

        gen_html(os.path.join(dir_path, 'index.html'), dir_path.replace('\\', '/'), contents)

        for name in dir_names:
            traverse_dll(os.path.join(dir_path, name))


def gen_html(filename: str, title: str, contents: list):
    headers = [
        '<html><head><title>openctp-ctp multi channels libs</title></head><body>',
        f'<h1>Index of {title}</h1>',
        '<h4>Author: <a href="https://github.com/Jedore" target="_black">Jedore</a></h4>',
        '<hr><pre>',
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
