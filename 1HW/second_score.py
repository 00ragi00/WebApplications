n = int(input())
A = list(map(int, input().split()))
print(sorted(set(A))[-2])