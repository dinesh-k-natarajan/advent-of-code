import time
import pytest

my_range = lambda a,b: range(int(a), int(b)+1) 

def parse_input( filename ):
    with open(filename,'r') as input_file:
        return [[my_range(*limits.split('-')) for limits in pair.split(',')] for pair in input_file.read().splitlines()]

def count_fully_contained_pairs( pairs ):
    return len([elves for elves in pairs if (set(elves[0]).issubset(elves[1]) or set(elves[1]).issubset(elves[0]))])

def count_overlapped_pairs( pairs ):
    return len([elves for elves in pairs if set.intersection(set(elves[0]), set(elves[1]))])

@pytest.mark.parametrize( 'test_input,expected', [ ('4.example', 2) ] )
def test_part1( test_input, expected ):
    assert count_fully_contained_pairs( parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('4.example', 4) ] )
def test_part2( test_input, expected ):
    assert count_overlapped_pairs( parse_input(test_input) ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', count_fully_contained_pairs( parse_input('4.in') ))
    print('Part 2 Solution = ', count_overlapped_pairs( parse_input('4.in') ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()