import pytest
from collections import defaultdict

def get_inputs( filename ):
    """
    The input file has a row of seats in each line. 
    This function returns each row as a list.
    """
    with open( filename, 'r') as input_file:
        inputs = input_file.read().splitlines()
    return inputs

def adjust_layout( seats ):
    """
    . denotes floor, L denotes free seats, # denotes occupied seats.
    
    Based on the following rules, the seat layout is adjusted:
        
        1.  If a seat is empty (L) and there are no occupied seats 
            adjacent to it, the seat becomes occupied.
        2.  If a seat is occupied (#) and four or more seats adjacent 
            to it are also occupied, the seat becomes empty.
        3.  Otherwise, the seat's state does not change.

    This function returns the seats after one round of layout changes
    """
     
    return seats

def count_occupied( seats ):
    """
    The adjust_layout function is run until the seat layout converges. 
    This function returns the number of occupied seats in the converged
    layout.
    """
    return seats.count('#')

@pytest.mark.parametrize( 'test_input, expected', [ ('11.example', 37) ] )
def test_part1( test_input, expected ):
    assert count_occupied( get_inputs(test_input) ) == expected

def main():
    print('Test 1 Solution = ', count_occupied( get_inputs('11.example') ) )
    #print('Part 1 Solution = ', count_occupied( get_inputs('11.in') ) )

if __name__ == '__main__':
    exit( main())
