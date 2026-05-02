import random
import math

# Оценка погрешности в зависимости от n:
# n=100:    погрешность ~1-3
# n=1000:   погрешность ~0.3-1
# n=10000:  погрешность ~0.1-0.3
# n=100000: погрешность ~0.03-0.1
# Погрешность уменьшается пропорционально 1/sqrt(n).
# Для получения точности до 2 знаков после запятой нужно n >= 100000.

def circle_square_mk(r, n):
    inside = 0
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        if x**2 + y**2 <= r**2:
            inside += 1
    return (inside / n) * (2 * r) * (2 * r)

if __name__ == '__main__':
    r = float(input())
    n = int(input())
    res = circle_square_mk(r, n)
    real = math.pi * r * r
    print(f"Метод МК: {res:.4f}")
    print(f"Формула: {real:.4f}")
    print(f"Погрешность: {abs(res - real):.4f}")
