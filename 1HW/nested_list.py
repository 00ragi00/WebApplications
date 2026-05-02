N = int(input())
if 2 <= N <= 5:
    L = []
    for i in range (N):
        first = str(input())
        second = float(input())
        S = [first, second]
        L.append(S)
    L = sorted(L, key=lambda x: (x[1], x[0]))
    G = sorted(set(grades[1] for grades in L))
    for students in L:
        if students[1] == G[1]:
            print(students[0])




