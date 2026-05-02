def compute_average_scores(scores):
    n = len(scores[0])
    avgs = []

    for i in range(n):
        s = sum(scores[j][i] for j in range(len(scores)))
        avgs.append(s / len(scores))
        
    return tuple(avgs)

if __name__ == '__main__':
    n, x = map(int, input().split())
    if 0 < n <= 100 and 0 < x <= 100:

        ss = []

        for _ in range(x):
            ss.append(tuple(map(float, input().split())))

        res = compute_average_scores(ss)

        for avg in res:
            print(round(avg, 1))
    else: print('Ошибка! Проверьте ограничения!')