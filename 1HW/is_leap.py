y = int(input())
l = False

if y % 4 == 0:
    l = True
    if y % 100 == 0:
        l = False
        if y % 400 == 0:
            l = True

print(l)
