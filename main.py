import os
from reader import Reader


def conver_dir(target):
    for fp in os.listdir(target):
        print(fp)
        if not fp.endswith('.txt'):
            continue
        with open(os.path.join(target, fp), 'r', encoding='utf8') as f:
            text = f.read()
        r = Reader(text)
        r.load()
        r.format()
        text = r.to_txt()
        newpath = os.path.join(target, 'revised')
        newpath = os.path.join(newpath, fp)
        with open(newpath, 'w', encoding='utf8') as f:
            f.write(text)


if __name__ == '__main__':
    conver_dir('.')