line1 = input().split()
n = int(line1[0])
m = int(line1[1])

i = []
for _ in range(m):
    l = input().split()
    name = l[0]
    weight = int(l[1])
    price = int(l[2])
    vpu = price / weight if weight > 0 else 0
    i.append({'name': name, 'w': weight, 'p': price, 'vpu': vpu})

i.sort(key=lambda x: x['vpu'], reverse=True)

l_i = []

for item in i:
    if n <= 0:
        break
    
    if item['w'] <= n:
        take_w = item['w']
        take_p = item['p']
        n -= take_w
        l_i.append((item['name'], take_w, take_p))
    else:
        take_w = n
        take_p = take_w * item['vpu']
        n = 0
        l_i.append((item['name'], take_w, take_p))

for name, w, p in l_i:
    print(f"{name} {w:.2f} {p:.2f}")
