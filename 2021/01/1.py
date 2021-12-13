import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [ int(i) for i in input_file.read().splitlines() ]

def count_depth_increase( depths ):
    increases = [ j-i for i,j in zip(depths[:-1],depths[1:]) ]
    return sum( i>0 for i in increases )

def count_windowed_increase( depths ):
    three_measurement_sum = [ i+j+k for i,j,k in zip(depths[:-2], depths[1:-1], depths[2:]) ]
    return count_depth_increase( three_measurement_sum )

@pytest.mark.parametrize( 'test_input,expected', [ ([199,200,208,210,200,207,240,269,260,263], 7) ] )
def test_part1( test_input, expected ):
    assert count_depth_increase( test_input ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ([199,200,208,210,200,207,240,269,260,263], 5) ] )
def test_part2( test_input, expected ):
    assert count_windowed_increase( test_input ) == expected

def main():
    print('Part 1 Solution = ', count_depth_increase( get_input('1.in') ))
    print('Part 2 Solution = ', count_windowed_increase( get_input('1.in') ))

if __name__ == '__main__':
    main()
