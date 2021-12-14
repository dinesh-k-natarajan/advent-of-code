import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [ int(i) for i in input_file.read().split(',') ]

def compute_fuel( positions ):
    fuel_per_target = dict()
    for target in range( max(positions)+1 ):
        fuel_per_submarine = [ abs(target-position) for position in positions ]
        fuel_per_target[target] = sum( fuel_per_submarine )
    return min( fuel_per_target.values() )

def recompute_fuel( positions ):
    """
    Move from 16 to 5: 66 fuel : 11 = 1+2+3+4+5+6+7+8+9+10+11 = 66
    Move from 1 to 5: 10 fuel  : 4 = 1+2+3+4= 10
    """
    fuel_per_target = dict()
    for target in range( max(positions)+1 ):
        fuel_per_submarine = [ sum( range(1,abs(target-position)+1) ) for position in positions ]
        fuel_per_target[target] = sum( fuel_per_submarine )
    return min( fuel_per_target.values() )

@pytest.mark.parametrize( 'test_input,expected', [ ('7.example', 37 ) ] )
def test_part1( test_input, expected ):
    assert compute_fuel( get_input( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('7.example', 168 ) ] )
def test_part2( test_input, expected ):
    assert recompute_fuel( get_input( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', compute_fuel( get_input('7.in') ) )
    print('Part 2 Solution = ', recompute_fuel( get_input('7.in') ) )

if __name__ == '__main__':
    main()
