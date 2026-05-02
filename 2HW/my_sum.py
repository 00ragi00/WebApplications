def my_sum(*args):
    return sum(args)

if __name__ == '__main__':
    nums = [float(x) for x in input().split()]
    print(my_sum(*nums))
