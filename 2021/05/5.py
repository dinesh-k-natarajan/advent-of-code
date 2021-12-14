import pytest
import re
from collections import defaultdict

def get_input( filename ):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [ [int(entry) for entry in re.findall(r'\d+', line)] for line in lines ]

sign = lambda x: -1 if x < 0 else ( 1 if x > 0 else 0 )

def count_overlapping_points( lines, part_2=False ):
    considered_lines = [ line for line in lines if line[0]==line[2] or line[1]==line[3] ]
    if part_2:
        considered_lines = lines
    points = defaultdict( lambda: 0)
    for line in considered_lines:
        x1, y1, x2, y2 = line
        len_x = abs( x2 - x1 )
        len_y = abs( y2 - y1 )
        dir_x = sign( x2 - x1 )
        dir_y = sign( y2 - y1 )
        for d in range( max(len_x,len_y)+1 ):
            x = x1 + dir_x * d
            y = y1 + dir_y * d
            points[ x,y ] += 1
    return sum( 1 for value in points.values() if value > 1 )

@pytest.mark.parametrize( 'test_input,expected', [ ('5.example', 5) ] )
def test_part1( test_input, expected ):
    assert count_overlapping_points( get_input( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('5.example', 12) ] )
def test_part2( test_input, expected ):
    assert count_overlapping_points( get_input( test_input ), part_2=True ) == expected

def main():
    print('Part 1 Solution = ', count_overlapping_points( get_input('5.in') ))
    print('Part 2 Solution = ', count_overlapping_points( get_input('5.in'), part_2=True ))

if __name__ == '__main__':
    main()
