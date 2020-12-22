import pytest

def get_inputs( filename):
    """
    The input file contains the list of questions to which
    each group of passengers answered yes on the customs form.

    Each line in the group represents a single person.
    
    This function returns a list of lists where the entries
    of the inner list represents each person.
    """
    with open( filename, 'r') as input_file:
        groups = input_file.read().split('\n\n')
    inputs = []
    for group in groups:
        inputs.append( group.splitlines() )
    return inputs

def count_yes( answers, part2=False ):
    """
    For Part 1:
    -----------
    This function returns the count of questions to which atleast one
    person in the group answered yes.
    
    For Part 2:
    -----------
    This function returns the count of questions to which every
    person in the group answered yes.
    """
    count_any = 0
    count_all = 0
    for group in answers:
        yes_any    = set( [result for item in group for result in item] )
        count_any += len(yes_any)
        yes_all    = set(group[0]).intersection( *group[1:] ) 
        count_all += len(yes_all)
    if not part2:
        return count_any
    else:
        return count_all

@pytest.mark.parametrize( 'test_input, expected', [ ('6.example', 11) ] )
def test_part1( test_input, expected ):
    assert count_yes( get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('6.example', 6) ] )
def test_part2( test_input, expected ):
    assert count_yes( get_inputs(test_input), part2=True ) == expected

def main():
    inputs = get_inputs( '6.in')
    print('Part 1 Solution = ', count_yes(inputs))
    print('Part 2 Solution = ', count_yes(inputs, part2=True))

if __name__ == '__main__':
    exit( main())
