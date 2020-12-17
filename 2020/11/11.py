import pytest
from copy import deepcopy
from itertools import product

def get_inputs( filename ):
    """
    The input file has a row of seats in each line. 
    This function returns each row as a list.
    """
    with open( filename, 'r') as input_file:
        return [ [seat for seat in row] for row in input_file.read().splitlines() ]
    
def print_seats(name,seats):
    """
    For debugging. 
    This function prints name of the layout, the layout in input format, 
    and the number of occupied seats in the layout. 
    """
    print(name)
    for row in seats:
        print(''.join(row))
    print('occupied seats:', sum( [ row.count('#') for row in seats ] ) ) 

def adjust_layout( seats, part2=False ):
    """
    . denotes floor, L denotes free seats, # denotes occupied seats.
    
    Based on the following rules, the seat layout is adjusted:
        
        1.  If a seat is empty (L) and there are no occupied seats 
            adjacent to it, the seat becomes occupied.
        2.  If a seat is occupied (#) and four or more seats adjacent 
            to it are also occupied, the seat becomes empty.
        3.  Otherwise, the seat's state does not change.

    This function returns the seats after one round of layout changes
    
    Changes in rules for Part 2:
        1. The adjacent seats have to a seat (L or #) and not a floor. 
        2. The tolerance for adjacent occupied seats has increased from 4 to 5. 
    """
    new_layout = deepcopy( seats )
    adj_rows = [-1,0,1] 
    adj_cols = [-1,0,1]
    tolerance = 4 if not part2 else 5
    for n_row, row in enumerate( new_layout ):
        for n_col, seat in enumerate( row ):
            if not part2:
                adj_seats = [ [seat for seat in seats[n_row+r][n_col+c]] for (r,c) in product(adj_rows,adj_cols) 
                            if 0<=n_row+r<len(seats) and 0<=n_col+c<len(seats[0]) and (n_row+r,n_col+c) != (n_row,n_col) ]
                adj_seats = [ seat for redundant_list in adj_seats for seat in redundant_list ]
            elif part2:
                adj_seats = []
                for r in adj_rows:
                    for c in adj_cols:
                        if (r,c) == (0,0): continue
                        radius = 1
                        while 0 <= n_row + radius*r < len(seats) and 0 <= n_col + radius*c < len(seats[0]):
                            adj = seats[n_row+radius*r][n_col+radius*c]
                            if adj != '.':
                                adj_seats.append( adj )
                                break
                            radius += 1
            n_occupied = adj_seats.count('#')
            if seats[n_row][n_col] == 'L' and n_occupied == 0:
                new_layout[n_row][n_col] = '#'
            elif seats[n_row][n_col] == '#' and n_occupied >= tolerance:
                new_layout[n_row][n_col] = 'L'
    assert new_layout is not seats
    return new_layout

def count_occupied( seats, part2=False ):
    """
    The adjust_layout function is run until the seat layout converges. 
    This function returns the number of occupied seats in the converged
    layout.
    """
    old_layout = deepcopy( seats )
    converged = False
    while not converged:
        new_layout = adjust_layout( old_layout, part2 )
        assert new_layout is not old_layout
        if new_layout == old_layout:
            converged = True
        old_layout = deepcopy( new_layout )
    return sum( [ row.count('#') for row in new_layout ] )

@pytest.mark.parametrize( 'test_input, expected', [ ('11.example', 37) ] )
def test_part1( test_input, expected ):
    assert count_occupied( get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('11.example', 26) ] )
def test_part2( test_input, expected ):
    assert count_occupied( get_inputs(test_input), part2=True ) == expected

def main():
    print('Part 1 Solution = ', count_occupied( get_inputs('11.in') ) )
    print('Part 2 Solution = ', count_occupied( get_inputs('11.in'), part2=True) )

if __name__ == '__main__':
    exit( main())
