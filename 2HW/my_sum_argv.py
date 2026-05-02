import sys

def my_sum(*args):
    return sum(args)

if __name__ == '__main__':
    nums = [float(x) for x in sys.argv[1:]]
    print(my_sum(*nums))
