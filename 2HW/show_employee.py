def show_employee(name, salary=100000):
    return f"{name}: {salary} ₽"

if __name__ == '__main__':
    n = input()
    s = int(input())
    print(show_employee(n, s))
