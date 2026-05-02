cube = lambda x: x**3

def fibonacci(n):
    fs = []
    a, b = 0, 1
    for _ in range(n):
        fs.append(a)
        a, b = b, a + b
    return fs

if __name__ == '__main__':
    n = int(input())
    if 1 <= n <= 15:
        print(list(map(cube, fibonacci(n))))
    else: print('Ошибка! Проверьте ограничения!')
