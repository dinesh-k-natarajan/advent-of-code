import pytest
import re

def get_input( filename ):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [ [int(entry) for entry in re.findall(r'\d+', line)] for line in lines ]

def count_overlapping_points( lines ):
    hv_lines = [ line for line in lines if line[0]==line[2] or line[1]==line[3] ]
     
    return count

@pytest.mark.parametrize( 'test_input,expected', [ ('5.example', 5) ] )
def test_part1( test_input, expected ):
    assert count_overlapping_points( get_input( test_input ) ) == expected

#@pytest.mark.parametrize( 'test_input,expected', [ ('5.example', 230) ] )
#def test_part2( test_input, expected ):
#    assert count_overlapping_points( get_input( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', count_overlapping_points( get_input('5.in') ))
#    print('Part 2 Solution = ', count_overlapping_points( get_input('5.in') ))

if __name__ == '__main__':
    main()
