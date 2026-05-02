import subprocess
import pytest # type: ignore

# Для Windows
INTERPRETER = 'python'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, filename],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50'])
    ],
    'division': [
        (['3', '5'], ['0', '0.6']),
        (['10', '2'], ['5', '5.0']),
        (['4', '3'], ['1', '1.3333333333333333']),
        (['0', '5'], ['0', '0.0']),
        (['-7', '2'], ['-4', '-3.5']),
        (['1234567890', '12345'], ['100005', '100005.49939246659'])
    ],
    'loops': [
        (['1'], ['0']),
        (['3'], ['0', '1', '4']),
        (['5'], ['0', '1', '4', '9', '16']),
        (['10'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81']),
        (['20'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81', '100', '121', '144', '169', '196', '225', '256', '289', '324', '361'])
    ],
    'print_function': [
        (['1'], '1'),
        (['2'], '12'),
        (['3'], '123'),
        (['5'], '12345'),
        (['10'], '12345678910'),
        (['20'], '1234567891011121314151617181920')
    ],
    'second_score': [ 
        (['5', '2 3 6 6 5'], '5'),
        (['4', '57 57 -57 57'], '-57'),
        (['5', '1 -1 -2 -1 2'], '1'),
        (['6', '10 9 8 7 6 5'], '9'),
        (['3', '-10 -10 -20'], '-20'),
        (['5', '100 10 100 10 99'], '99')
    ],
    'nested_list': [
        (
            ['5', 'Harry', '37.21', 'Berry', '37.21', 'Tina', '37.2', 'Akriti', '41', 'Harsh', '39'],
            ['Berry', 'Harry']
        ),
        (
            ['3', 'Ann', '10.0', 'Bob', '20.0', 'Cara', '30.0'],
            ['Bob']
        ),
        (
            ['4', 'Alex', '50', 'Ben', '40', 'Cody', '60', 'Drew', '45'],
            ['Drew']
        ),
        (
            ['5', 'Liam', '10', 'Noah', '20', 'Olivia', '20', 'Emma', '30', 'Ava', '40'],
            ['Noah', 'Olivia']
        ),
        (
            ['4', 'mike', '0', 'john', '-10', 'anna', '0', 'zoe', '10'],
            ['anna', 'mike']
        )
    ],
    'lists': [
        (
            ['12',
            'insert 0 5',
            'insert 1 10',
            'insert 0 6',
            'print',
            'remove 6',
            'append 9',
            'append 1',
            'sort',
            'print',
            'pop',
            'reverse',
            'print'],
            ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]']
        ),
        (
            ['4',
            'append 1',
            'append 2',
            'insert 1 3',
            'print'],
            ['[1, 3, 2]']
        ),
        (
            ['7',
            'append 3',
            'append 1',
            'append 2',
            'sort',
            'print',
            'reverse',
            'print'],
            ['[1, 2, 3]', '[3, 2, 1]']
        ),
        (
            ['5',
            'append 5',
            'append 5',
            'append 6',
            'remove 5',
            'print'],
            ['[5, 6]']
        )
    ],
    'swap_case': [
        (['Www.MosPolytech.ru'], 'wWW.mOSpOLYTECH.RU'),
        (['Pythonist 2'], 'pYTHONIST 2'),
        (['hello world'], 'HELLO WORLD'),
        (['PYTHON'], 'python'),
        (['HaCkErRaNk'], 'hAcKeRrAnK'),
        (['123!@#'], '123!@#')
    ],
    'split_and_join': [
        (['this is a string'], 'this-is-a-string'),
        (['Hello World'], 'Hello-World'),
        (['Python'], 'Python'),
        (['   '], ''),
        (['a    b c'], 'a-b-c'),
        (['  trim me  '], 'trim-me')
    ],
    'anagram': [
        (['listen', 'silent'], 'YES'),
        (['hello', 'world'], 'NO'),
        (['abc', 'ab'], 'NO'),
        (['test', 'test'], 'YES'),
        (['Abc', 'abc'], 'NO'),
        (['123', '321'], 'YES')
    ],
    'metro': [
        (['3', '5 15', '12 20', '0 10', '10'], '2'),
        (['2', '10 20', '30 40', '5'], '0'),
        (['3', '1 100', '20 50', '30 35', '32'], '3'),
        (['1', '10 20', '10'], '1'),
        (['1', '10 20', '20'], '1'),
        (['1', '10 20', '15'], '1'),
        (['2', '1 5', '6 10', '5'], '1'),
        (['2', '1 5', '6 10', '6'], '1')
    ],
    'minion_game': [
        (['BANANA'], 'Стюарт 12'),
        (['AAAA'], 'Кевин 10'),
        (['BBBB'], 'Стюарт 10'),
        (['BA'], 'Стюарт 2'),
        (['A'], 'Кевин 1'),
        (['B'], 'Стюарт 1'),
        (['AEIOU'], 'Кевин 15'),
        (['BCDFG'], 'Стюарт 15')
    ],
    'is_leap': [
        (['2000'], 'True'),
        (['2400'], 'True'),
        (['1900'], 'False'),
        (['2100'], 'False'),
        (['2024'], 'True'),
        (['2012'], 'True'),
        (['2023'], 'False'),
        (['2025'], 'False'),
        (['100000'], 'True')
    ],
    'happiness': [
        (['3 2', '1 5 3', '3 1', '5 7'], '1'),
        (['3 2', '1 2 2', '1 2', '3 4'], '3'),
        (['3 2', '3 4 3', '1 2', '3 4'], '-3'),
        (['3 2', '10 20 30', '1 2', '3 4'], '0'),
        (['5 1', '1 1 2 2 3', '1', '2'], '0'),
        (['2 1', '100 200', '1', '2'], '0')
    ],
    'pirate_ship': [
        (
            ['10 3', 'A 5 10', 'B 10 10', 'C 2 1'],
            ['A 5.00 10.00', 'B 5.00 5.00']
        ),
        (
            ['100 2', 'Gold 10 1000', 'Silver 20 500'],
            ['Gold 10.00 1000.00', 'Silver 20.00 500.00']
        ),
        (
            ['1 2', 'Iron 10 10', 'Gold 2 200'],
            ['Gold 1.00 100.00']
        ),
        (
            ['12 2', 'A 10 10', 'B 5 5'],
            ['A 10.00 10.00', 'B 2.00 2.00']
        )
    ],
    'matrix_mult': [
        (
            ['2', '1 2', '3 4', '1 0', '0 1'],
            ['1 2', '3 4']
        ),
        (
            ['2', '1 2', '3 4', '2 0', '1 2'],
            ['4 4', '10 8']
        ),
        (
            ['3', 
            '1 2 3', '4 5 6', '7 8 9', 
            '1 0 0', '0 1 0', '0 0 1'],
            ['1 2 3', '4 5 6', '7 8 9']
        ),
        (
            ['2', '1 2', '3 4', '0 0', '0 0'],
            ['0 0', '0 0']
        )
    ]



}

def test_hello_world():
    assert run_script('hello_world.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    expected_output = '\n'.join(expected)
    assert run_script('nested_list.py', input_data) == expected_output

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    expected_output = '\n'.join(expected)
    assert run_script('lists.py', input_data) == expected_output

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join'])
def test_split_and_join(input_data, expected):
    assert run_script('split_and_join.py', input_data) == expected

def test_max_word_from_file():
    assert run_script('max_word.py') == 'сосредоточенности'

def test_price_sum_from_file():
    output = run_script('price_sum.py')
    expected = '6842.84 5891.06 6810.90'
    assert output == expected

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    expected_output = '\n'.join(expected)
    assert run_script('pirate_ship.py', input_data) == expected_output

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    expected_output = '\n'.join(expected)
    assert run_script('matrix_mult.py', input_data) == expected_output
