import time
import pytest

def parse_input( filename ):
    with open(filename,'r') as input_file:
        return input_file.read()

def find_marker( buffer, seq_len ):
    for idx in range(len(buffer)-seq_len+1):
        if len(set(buffer[idx:idx+seq_len])) == seq_len:
            return idx+seq_len
    return None

@pytest.mark.parametrize( 'test_input,expected', [  ('6.ex1', 7), 
                                                    ('6.ex2', 5),
                                                    ('6.ex3', 6),
                                                    ('6.ex4', 10),
                                                    ('6.ex5', 11), 
                                                ] )
def test_part1( test_input, expected ):
    assert find_marker( parse_input(test_input), seq_len=4 ) == expected

@pytest.mark.parametrize( 'test_input,expected', [  ('6.ex1', 19), 
                                                    ('6.ex2', 23),
                                                    ('6.ex3', 23),
                                                    ('6.ex4', 29),
                                                    ('6.ex5', 26), 
                                                ] )
def test_part2( test_input, expected ):
    assert find_marker( parse_input(test_input), seq_len=14 ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', find_marker( parse_input('6.in'), seq_len=4 ))
    print('Part 2 Solution = ', find_marker( parse_input('6.in'), seq_len=14 ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()