n = int(input())
if 1 <= n <= 100:
    if n % 2 == 1: print('Weird')
    elif n % 2 == 0 and (2 <= n <= 5): print('Not Weird')
    elif n % 2 == 0 and (6 <= n <= 20): print('Weird')
    elif n % 2 == 0 and n > 20: print('Not Weird')
else: print('Ошибка! n должно быть целым числом от 1 до 100')

