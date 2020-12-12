import pytest

def get_inputs( filename ):
    """
    The input file has intructions in each line 
    This function returns the instructions as a list of lists.
    """
    with open( filename, 'r') as input_file:
        inputs = [ [ item[:1], int(item[1:]) ] for item in input_file.read().splitlines() ]
    return inputs

def compute_distance( instructions ):
    """

    """

    return distance

@pytest.mark.parametrize( 'test_input, expected', [ ('12.example', 25) ] )
def test_part1( test_input, expected ):
    assert compute_distance( get_inputs(test_input) ) == expected

def main():
    print('Test 1 Solution = ', compute_distance( get_inputs('12.example') ) )
    #print('Part 1 Solution = ', compute_distance( get_inputs('12.in') ) )

if __name__ == '__main__':
    exit( main())
