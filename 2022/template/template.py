import time
import pytest

def parse_input(filename):
    with open(filename,'r') as input_file:
        return [line for line in input_file.read().splitlines()]

def compute_1(inputs):
    print(inputs)
    return None

def compute_2(inputs):
    return None

@pytest.mark.parametrize('test_input,expected', [('1.example',None)])
def test_part1(test_input,expected):
    assert compute_1(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('1.example',None)])
def test_part2(test_input,expected):
    assert compute_2(parse_input(test_input)) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_1(parse_input('1.in'))}")
    print(f"Part 2 Solution = {compute_2(parse_input('1.in'))}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()