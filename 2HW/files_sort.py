import sys
import os

if __name__ == '__main__':
    p = sys.argv[1]
    fs = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    fs.sort(key=lambda x: (x.split('.')[-1], x))
    for f in fs:
        print(f)
