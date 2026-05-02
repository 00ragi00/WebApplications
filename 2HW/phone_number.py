def wrapper(f):
    def fun(l):
        formatted = []
        for p in l:
            digits = ''.join(filter(str.isdigit, p))
            if len(digits) == 11:
                digits = digits[1:]
            formatted.append(f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}")
        return f(formatted)
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
