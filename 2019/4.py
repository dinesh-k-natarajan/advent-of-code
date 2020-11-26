import pytest

def count_valid( inputs, part2=False):
    num_valid = 0
    for number in range( inputs[0], inputs[1]+1 ):
        digits = [ int( char ) for char in str( number ) ]
        counts = [ 0 ]*len( digits )
        for idx, entry in enumerate( digits ):
            counts[idx]  = digits.count( entry ) - 1
        running_product = set( [ counts[i]*counts[i+1] for i in range( len(counts)-1 ) ] )
        if not part2:
            flag_adjacent = max( running_product ) > 0
        else:
            flag_adjacent = 1 in running_product
        ascending_digits = digits.copy()
        ascending_digits.sort()
        flag_decreasing  = ( digits == ascending_digits )
        num_valid += int( flag_adjacent and flag_decreasing )
    return num_valid

@pytest.mark.parametrize( 'test_input, expected', 
                            [ ( [111111, 111111], 1 ),
                              ( [223450, 223450], 0 ),
                              ( [123789, 123789], 0 ) ] )
def test_part1( test_input, expected ):
    assert count_valid( test_input ) == expected

@pytest.mark.parametrize( 'test_input, expected', 
                            [ ( [112233, 112233], 1 ),
                              ( [123444, 123444], 0 ),
                              ( [111122, 111122], 1 ) ] )
def test_part2( test_input, expected ):
    assert count_valid( test_input, part2=True ) == expected

def main():
    inputs = [ 146810, 612564 ]
    # Part 1
    print('Part 1 Solution = ', count_valid( inputs ) )
    # Part 2
    print('Part 2 Solution = ', count_valid( inputs, part2=True ) )

if __name__ == '__main__':
    exit( main() )
