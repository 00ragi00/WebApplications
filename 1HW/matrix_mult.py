def multiply_matrices(n, A, B):
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

try:
    line = input().split()
    if line:
        n = int(line[0])

        A = []
        B = []

        for _ in range(n):
            row = list(map(int, input().split()))
            A.append(row)

        for _ in range(n):
            row = list(map(int, input().split()))
            B.append(row)

        result = multiply_matrices(n, A, B)

        for row in result:
            print(*row)
            
except (ValueError, IndexError):
    pass
