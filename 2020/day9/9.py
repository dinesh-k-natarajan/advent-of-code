import pytest
from itertools import combinations

def get_inputs( filename ):
    """
    The input file has a number in each line. 
    This function returns the numbers as a list.
    """
    with open( filename, 'r') as input_file:
        inputs = [ int(item) for item in input_file.read().splitlines() ]
    return inputs

def find_invalid( data, preamble ):
    """
    From the given list of numbers, each number after the index 'preamble' should 
    be a sum of any two of the previous 'preamble' numbers. This function returns
    the first invalid number that fails this property. 
    """
    for loc in range( preamble, len(data) ):
        current_num = data[ loc ] 
        subset = data[ loc-preamble : loc ]
        pairs  = combinations( subset, 2 )
        flag   = any([ current_num == sum(pair) for pair in pairs ])
        if not flag:
            return current_num

def find_limits( data, preamble ):
    """
    After finding the invalid number from find_invalid function, the goal is to
    find a contiguous range of arbitrary length > 2 in the data that adds upto 
    the invalid number. This function returns the sum( min, max )
    """
    invalid     = find_invalid( data, preamble )
    invalid_loc = data.index( invalid )
    subset      = data[ :invalid_loc ]
    len_range   = 2
    found_range = False
    while not found_range:
        ranges = [ [ *subset[ idx:idx+len_range ]] for idx in range(len(subset)-len_range+1) ]
        for range_ in ranges:
            if sum( range_ ) == invalid:
                limits = range_
                found_range = True
                break
        len_range += 1
    return min( limits ) + max( limits ) 

@pytest.mark.parametrize( 'test_input, expected', [ ('9.example', 127) ] )
def test_part1( test_input, expected ):
    assert find_invalid( get_inputs(test_input), preamble=5 ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('9.example', 62) ] )
def test_part2( test_input, expected ):
    assert find_limits( get_inputs(test_input), preamble=5 ) == expected

def main():
    print('Part 1 Solution = ', find_invalid( get_inputs('9.in'), preamble=25 ) )
    print('Part 2 Solution = ', find_limits(  get_inputs('9.in'), preamble=25 ) )

if __name__ == '__main__':
    exit( main())
