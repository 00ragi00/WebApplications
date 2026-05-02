n = int(input())
p = []
k = 0

for i in range(n):
    t = list(map(int, input().split()))
    p.append(t)

T = int(input())

for i in p:
    start = i[0]
    end = i[1]
    if start <= T <= end:
        k += 1

print(k)
