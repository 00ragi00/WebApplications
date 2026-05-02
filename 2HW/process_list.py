# Сравнение скорости:
# List comprehension (process_list) и генератор (process_list_gen) работают
# примерно одинаково по скорости при полном переборе элементов.
# Однако генератор эффективнее по памяти: он не создаёт весь список сразу,
# а вычисляет элементы по одному. При len(arr)=1000 разница во времени
# минимальна, list: 8.440017700195312e-05, Gen: 9.274482727050781e-05,
# но генератор предпочтительнее при больших объёмах данных.

def process_list(arr):
    return [x**2 if x % 2 == 0 else x**3 for x in arr]

def process_list_gen(arr):
    for x in arr:
        if x % 2 == 0:
            yield x**2
        else:
            yield x**3

if __name__ == '__main__':
    import time
    #arr = list(range(1000))
    arr = list(map(int, input().split()))
    if 1 <= len(arr) <= 10**3:
    
        s = time.time()
        r1 = process_list(arr)
        t1 = time.time() - s
        
        s = time.time()
        r2 = list(process_list_gen(arr))
        t2 = time.time() - s
        
        print(f"List: {t1}, Gen: {t2}")
    else: print('Ошибка! Проверьте ограничения!')