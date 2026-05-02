s = input().strip().upper()
l = len(s)

s_s = 0
k_s = 0
v = "AEIOU" 

for i in range(l):
    if s[i] in v:
        k_s += l - i
    else:
        s_s += l - i

if s_s > k_s:
    print(f"Стюарт {s_s}") 
elif k_s > s_s:
    print(f"Кевин {k_s}")
else:
    print("Ничья")
