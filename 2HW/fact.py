# Сравнение скорости:
# Итерационная функция (fact_it) работает быстрее рекурсивной (fact_rec),
# так как рекурсия создаёт накладные расходы на вызов функций и хранение стека.
# При n=100: fact_it = 8.821487426757812e-06, fact_rec = 2.1457672119140625e-05.
# При больших n рекурсия также может вызвать ошибку RecursionError из-за
# ограничения глубины стека Python.

def fact_rec(n):
    if n <= 1:
        return 1
    return n * fact_rec(n - 1)

def fact_it(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

if __name__ == '__main__':
    import time
    n = int(input())

    if 1 <= n <= 10**5:
        
        s = time.time()
        r1 = fact_rec(n)
        t1 = time.time() - s
        
        s = time.time()
        r2 = fact_it(n)
        t2 = time.time() - s
        
        print(f"rec: {r1}, time: {t1}")
        print(f"it: {r2}, time: {t2}")
    else:
        print('Ошибка! Проверьте ограничения!')
