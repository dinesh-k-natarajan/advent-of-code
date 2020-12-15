import pytest
from collections import defaultdict

def compute_number( starting_numbers, final=2020 ):
    """
    Given the starting numbers, the next number spoken should follow the rules below:

      - If the previous number was spoken for the first time,
        then the new number is 0. 
      - If the previous number was already spoken before,
        then the new number is difference of the previous two turns it was spoken

    The numbers spoken in each turn is kept track in the list `numbers`.
    The turns in which each unique number was spoken is kept track in the dict of lists `turns`

    Task:
    This function returns the last number spoken at the end of the `final` turn
    """
    numbers = starting_numbers.copy()
    turns   = defaultdict( list, { key:[value+1] for value,key in enumerate( numbers ) } )
    for turn in range( len(numbers)+1, final+1 ):
        prev_num = numbers[-1]
        if len( turns[ prev_num ] ) == 1: 
            next_num = 0
        else:
            assert len( turns[prev_num] ) > 1
            next_num =  turns[prev_num][-1] - turns[prev_num][-2]
        turns[ next_num ].append( turn )
        numbers.append( next_num )
    return numbers[-1]

@pytest.mark.parametrize('test_input,expected',[ ([0,3,6], 436),
                                                 ([1,3,2],   1),
                                                 ([2,1,3],  10),
                                                 ([1,2,3],  27),
                                                 ([2,3,1],  78),
                                                 ([3,2,1], 438),
                                                 ([3,1,2],1836) ] )
def test_part1( test_input, expected ):
    assert compute_number( test_input ) == expected

def main():
    print('Part 1 Solution = ', compute_number( [0,13,1,16,6,17], final=2020) )
    print('Part 2 Solution = ', compute_number( [0,13,1,16,6,17], final=30000000 ) )

if __name__ == '__main__':
    exit( main() )
