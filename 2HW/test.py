import pytest # type: ignore
import subprocess
import os
import shutil
import math

INTERPRETER = 'python'

def run_script(filename, args=None, input_data=None):
    cmd = [INTERPRETER, filename]
    if args:
        cmd.extend(args)

    proc = subprocess.run(
        cmd,
        input='\n'.join(input_data) if input_data else None,
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

from fact import fact_rec, fact_it
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_gen
from my_sum import my_sum
from email_validation import fun as email_fun, filter_mail
from fibonacci import fibonacci, cube
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from complex_numbers import Complex
from circle_square_mk import circle_square_mk


class TestFactorial:
    def test_fact_rec_zero(self):
        assert fact_rec(0) == 1

    def test_fact_rec_one(self):
        assert fact_rec(1) == 1

    def test_fact_rec_small(self):
        assert fact_rec(5) == 120

    def test_fact_rec_medium(self):
        assert fact_rec(10) == 3628800

    def test_fact_it_zero(self):
        assert fact_it(0) == 1

    def test_fact_it_one(self):
        assert fact_it(1) == 1

    def test_fact_it_small(self):
        assert fact_it(5) == 120

    def test_fact_it_medium(self):
        assert fact_it(10) == 3628800

    def test_fact_equality(self):
        assert fact_rec(7) == fact_it(7)

    def test_fact_large(self):
        assert fact_it(20) == 2432902008176640000


class TestShowEmployee:
    def test_with_salary(self):
        result = show_employee("Иванов", 50000)
        assert "Иванов" in result
        assert "50000" in result

    def test_default_salary(self):
        result = show_employee("Петров")
        assert "Петров" in result
        assert "100000" in result

    def test_high_salary(self):
        result = show_employee("Сидоров", 1000000)
        assert "Сидоров" in result
        assert "1000000" in result

    def test_zero_salary(self):
        result = show_employee("Козлов", 0)
        assert "Козлов" in result
        assert "0" in result


class TestSumAndSub:
    def test_positive_numbers(self):
        s, d = sum_and_sub(10, 5)
        assert s == 15
        assert d == 5

    def test_negative_numbers(self):
        s, d = sum_and_sub(-5, -3)
        assert s == -8
        assert d == -2

    def test_mixed_numbers(self):
        s, d = sum_and_sub(10, -5)
        assert s == 5
        assert d == 15

    def test_floats(self):
        s, d = sum_and_sub(3.5, 1.5)
        assert abs(s - 5.0) < 0.001
        assert abs(d - 2.0) < 0.001

    def test_zero(self):
        s, d = sum_and_sub(0, 0)
        assert s == 0
        assert d == 0


class TestProcessList:
    def test_process_list_basic(self):
        result = process_list([1, 2, 3, 4])
        assert result == [1, 4, 27, 16]

    def test_process_list_empty(self):
        result = process_list([])
        assert result == []

    def test_process_list_gen_basic(self):
        result = list(process_list_gen([1, 2, 3, 4]))
        assert result == [1, 4, 27, 16]

    def test_process_list_all_even(self):
        result = process_list([2, 4, 6])
        assert result == [4, 16, 36]

    def test_process_list_all_odd(self):
        result = process_list([1, 3, 5])
        assert result == [1, 27, 125]


class TestMySum:
    def test_sum_two_numbers(self):
        assert my_sum(1, 2) == 3

    def test_sum_multiple(self):
        assert my_sum(1, 2, 3, 4, 5) == 15

    def test_sum_floats(self):
        assert abs(my_sum(1.5, 2.5, 3.0) - 7.0) < 0.001

    def test_sum_negative(self):
        assert my_sum(-1, -2, -3) == -6

    def test_sum_single(self):
        assert my_sum(42) == 42

    def test_sum_zero(self):
        assert my_sum(0, 0, 0) == 0


class TestMySumArgv:
    def test_sum_argv_basic(self):
        result = run_script('my_sum_argv.py', args=['1', '2', '3'])
        assert '6' in result or '6.0' in result

    def test_sum_argv_floats(self):
        result = run_script('my_sum_argv.py', args=['1.5', '2.5'])
        assert '4' in result or '4.0' in result

    def test_sum_argv_single(self):
        result = run_script('my_sum_argv.py', args=['42'])
        assert '42' in result


class TestFilesSort:
    def setup_method(self):
        os.makedirs('test_dir', exist_ok=True)
        open('test_dir/z.txt', 'w').close()
        open('test_dir/a.py', 'w').close()
        open('test_dir/m.txt', 'w').close()

    '''def teardown_method(self):
        if os.path.exists('test_dir'):
            shutil.rmtree('test_dir')'''

    def test_files_sort(self):
        result = run_script('files_sort.py', args=['test_dir'])
        lines = result.split('\n')
        assert 'a.py' in lines[0]
        assert 'm.txt' in lines[1] or 'z.txt' in lines[1]


class TestFileSearch:
    def setup_method(self):
        os.makedirs('search_dir', exist_ok=True)
        with open('search_dir/target.txt', 'w') as f:
            f.write('line1\nline2\nline3\nline4\nline5\nline6\n')

    '''def teardown_method(self):
        if os.path.exists('search_dir'):
            shutil.rmtree('search_dir')'''

    def test_file_found(self):
        result = run_script('file_search.py', args=['target.txt'])
        assert 'line1' in result


class TestEmailValidation:
    def test_valid_email(self):
        assert email_fun('user@mail.com') == True

    def test_invalid_no_at(self):
        assert email_fun('usermail.com') == False

    def test_invalid_no_dot(self):
        assert email_fun('user@mailcom') == False

    def test_valid_with_numbers(self):
        assert email_fun('user123@mail.com') == True

    def test_valid_with_underscore(self):
        assert email_fun('user_name@mail.com') == True

    def test_filter_mail(self):
        emails = ['valid@test.com', 'invalid', 'another@test.ru']
        result = filter_mail(emails)
        assert len(result) == 2


class TestFibonacci:
    def test_fibonacci_basic(self):
        result = fibonacci(5)
        assert result == [0, 1, 1, 2, 3]

    def test_fibonacci_one(self):
        result = fibonacci(1)
        assert result == [0]

    def test_cube_basic(self):
        assert cube(2) == 8
        assert cube(3) == 27

    def test_fibonacci_cubed(self):
        result = list(map(cube, fibonacci(5)))
        assert result == [0, 1, 1, 8, 27]


class TestAverageScores:
    def test_average_basic(self):
        scores = [(5.0, 4.0), (4.0, 5.0), (4.5, 4.5)]
        result = compute_average_scores(scores)
        assert abs(result[0] - 4.5) < 0.1
        assert abs(result[1] - 4.5) < 0.1

    def test_average_single_student(self):
        scores = [(5.0, 4.0, 3.0)]
        result = compute_average_scores(scores)
        assert result == (5.0, 4.0, 3.0)


class TestPlaneAngle:
    def test_plane_angle_90(self):
        a = Point(0, 0, 0)
        b = Point(1, 0, 0)
        c = Point(1, 1, 0)
        d = Point(1, 1, 1)
        angle = plane_angle(a, b, c, d)
        assert abs(angle - 90) < 1

    def test_point_subtraction(self):
        p1 = Point(3, 5, 7)
        p2 = Point(1, 2, 3)
        result = p1 - p2
        assert result.x == 2
        assert result.y == 3
        assert result.z == 4

    def test_point_dot(self):
        p1 = Point(1, 0, 0)
        p2 = Point(0, 1, 0)
        assert p1.dot(p2) == 0


class TestComplexNumbers:
    def test_complex_add(self):
        c1 = Complex(2, 1)
        c2 = Complex(3, 4)
        result = c1 + c2
        assert result.real == 5
        assert result.imaginary == 5

    def test_complex_sub(self):
        c1 = Complex(5, 7)
        c2 = Complex(2, 3)
        result = c1 - c2
        assert result.real == 3
        assert result.imaginary == 4

    def test_complex_mul(self):
        c1 = Complex(2, 3)
        c2 = Complex(4, 5)
        result = c1 * c2
        assert result.real == -7
        assert result.imaginary == 22

    def test_complex_mod(self):
        c = Complex(3, 4)
        result = c.mod()
        assert abs(result.real - 5.0) < 0.01

    def test_complex_str_positive(self):
        c = Complex(3, 4)
        assert "+4.00i" in str(c)


class TestMonteCarlo:
    def test_circle_area_accuracy(self):
        r = 5.0
        n = 10000
        result = circle_square_mk(r, n)
        real = math.pi * r * r
        assert abs(result - real) < 5

    def test_circle_small_radius(self):
        r = 1.0
        n = 5000
        result = circle_square_mk(r, n)
        real = math.pi
        assert abs(result - real) < 1


class TestIntegration:
    def test_factorial_with_sum(self):
        f5 = fact_it(5)
        total = my_sum(f5, 10, 20)
        assert total == 150

    def test_fibonacci_with_process(self):
        fib = fibonacci(5)
        result = process_list(fib)
        assert len(result) == 5

    def test_complex_operations(self):
        c1 = Complex(1, 1)
        c2 = Complex(1, -1)
        mul = c1 * c2
        assert mul.real == 2
        assert mul.imaginary == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])