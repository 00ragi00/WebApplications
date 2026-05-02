import sys
import os

def search(name, path='.'):
    for item in os.listdir(path):
        fp = os.path.join(path, item)
        if os.path.isfile(fp) and item == name:
            return fp
        elif os.path.isdir(fp):
            r = search(name, fp)
            if r:
                return r
    return None

if __name__ == '__main__':
    n = sys.argv[1]
    start_path = os.path.dirname(os.path.abspath(__file__))
    r = search(n, start_path)
    if r:
        with open(r, 'r') as f:
            for i, line in enumerate(f):
                if i >= 5:
                    break
                print(line, end='')
    else:
        print(f"Файл {n} не найден")
