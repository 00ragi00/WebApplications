from datetime import datetime
import functools
import os

def function_logger(fp):
    os.makedirs(os.path.dirname(fp), exist_ok=True) if os.path.dirname(fp) else None
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            s = datetime.now()
            r = func(*args, **kwargs)
            e = datetime.now()

            with open(fp, 'a', encoding='utf-8') as f:
                f.write(f"Function: {func.__name__}\n")
                f.write(f"Start:    {s}\n")
                if args:
                    f.write(f"Args:     {args}\n")
                if kwargs:
                    f.write(f"Kwargs:   {kwargs}\n")
                f.write(f"Result:   {r if r is not None else '-'}\n")
                f.write(f"End:      {e}\n")
                f.write(f"Duration: {e - s}\n")
                f.write("-" * 40 + "\n")

            return r
        return wrapper
    return decorator

if __name__ == '__main__':
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'function_log.txt')

    @function_logger(log_path)
    def greet(name):
        return f'Hello, {name}!'

    @function_logger(log_path)
    def add(a, b):
        return a + b

    print(greet('John'))
    print(add(3, 5))
    print(f"Лог записан в: {log_path}")
