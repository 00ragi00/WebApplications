import string

with open('example.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    for i in string.punctuation:
        t = t.replace(i, '')
    w = t.split()
    max_len = 0
    for n in w:
        if len(n) > max_len:
            max_len = len(n)
    for n in w:
        if len(n) == max_len:
            print(n)
    
