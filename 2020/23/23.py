import pytest

def get_labels( string ):
    """
    This function returns a list of labels of each cup.
    """
    return [ int(label) for label in string ]

def roll_by_one( cups ):
    """
    This functions rolls the cups by one unit.
    The new current cup is the next cup in the clockwise direction.
    """
    return cups[1:] + cups[:1]

def naive_simulation( cups, runs=100 ):
    """
    For Part 1:
    -----------
    For a given list of cups, the game is simulated for 100 rounds.

    The rules of the game are:
        -   The first cup is the current cup, and the next 3 cups are picked up.
        -   The picked cups are placed to the right of the target cup which is
            found by subtracting current cup by 1.
        -   If the target cup has been picked up, then the previous cup becomes 
            the target. If target reaches 0, then the max cup label is assigned 
            as target and checked against the picked cups.
        -   After placing the picked cups to their destination, the cups are rolled
            clockwise by one. The next round is continued with the new current cup.

    The game is simulated for 100 rounds. The final cups are rolled until 1 is the
    first cup. This function returns the remaining cups as a string.
    """
    for _ in range( runs ):
        current_cup = cups[0]
        picked_cups = cups[1:4]
        target_cup  = current_cup - 1 if current_cup > 1 else 9
        while target_cup in picked_cups:
            target_cup -= 1
            if target_cup == 0:
                target_cup = 9
        destination = cups.index( target_cup )
        cups = [ current_cup ] + cups[4:destination+1] + picked_cups + cups[destination+1:] 
        cups = roll_by_one( cups )
    while cups[0] != 1:
        cups = roll_by_one( cups )
    return ''.join( str(cup) for cup in cups[1:] )


def simulate_game( cups, runs=10000000, part2=True ):
    """
    Reimplementation of the game to adapt to Part 2 using a dictionary which stores
    the neighbors of each cup ( equivalent to a Linked List, TODO )
    
    Dictionary of neighbors:
    ------------------------
    - Reasons for use: 
        * List indices start from 0 (poor readability due to cup labels starting from 0)
        * Linked Lists are kinda complicated, needs OOP (TODO)
    - The neighbors of each cup can be found using: neighbor = neighbor_of[ cup ]
      Since the cups are cyclical, the neighbors are initialized using the roll_by_one
      function.

    For Part 2:
    -----------
    - Apart from the given cups, additional cups upto 1 Million are to be added.
    - The runs have increased to 10 Million
    - At the end, the two cups immediately next to the cup 1 are to be found.
    - The solution is the product of those two cups.
    """
    if part2:
        cups += list( range(10,1000001) )
    neighbors         = roll_by_one( cups )
    neighbor_of       = dict( zip( cups, neighbors ) )
    """
    Starting from the first cup as the current cup ( hence, previous cup is initialized
    to the last cup )
    """
    previous_cup      = cups[-1]
    for _ in range( runs ):
        current_cup   = neighbor_of[ previous_cup ]
        picked_cups   = []
        picked_cup    = current_cup
        """
        The three neighboring cups after the current cup are picked, hence picked_cup 
        is initialized to the current cup.
        """
        for _ in range( 3 ):
            picked_cup = neighbor_of[ picked_cup ]
            picked_cups.append( picked_cup )
        """
        Compute the target cup similar to implementation in naive_simulation
        """
        target_cup  = current_cup - 1 if current_cup > 1 else max(cups)
        while target_cup in picked_cups:
            target_cup -= 1
            if target_cup == 0:
                target_cup = max(cups)
        """
        In contrast to naive_simulation, the destination index is unnecessary. The 
        target cup is directly used to modify the neighbors after placing the picked ups 
        to the right of the current cup.
        
        i.e., the following shuffling of cups is made:
        Before: [ .... , current_cup, picked_cups, ..... , target_cup, neighbor_of[target_cup], .....  ]
        After:  [ .... , current_cup, ..... , target_cup, picked_cups, neighbor_of[target_cup], .....  ]
        """
        neighbor_of[ current_cup ] = neighbor_of[ picked_cups[-1] ]
        neighbor_of[ target_cup ], neighbor_of[ picked_cups[-1] ] = picked_cups[0], neighbor_of[ target_cup ]
        previous_cup = current_cup
    if not part2:
        """
        For Part 1:
        -----------
        The results are in the form of a string with the chain of neighboring cups starting from
        the neighboring cup of 1 ( caution: 1 should not be a part of the result! ).
        """
        final_cups = []
        next_cup   = 1
        for _ in range( len(cups)-1 ):
            next_cup = neighbor_of[ next_cup ]
            final_cups.append( next_cup )
        return ''.join( str(cup) for cup in final_cups )
    else:
        """
        For Part 2:
        -----------
        The two neighboring cups that come after 1 are found. The result is the product of those two cups.
        """
        my_cups = [1]
        [ my_cups.append( neighbor_of[ my_cups[-1] ] ) for _ in range(2) ]
        return my_cups[1] * my_cups[2]

@pytest.mark.parametrize( 'test_input, expected', [ ( '389125467', '67384529' ) ] )
def test_part1( test_input, expected ):
    assert naive_simulation( get_labels( test_input ) ) == expected
    assert simulate_game( get_labels( test_input ), runs=100, part2=False ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ( '389125467', 149245887792 ) ] )
def test_part2( test_input, expected ):
    assert simulate_game( get_labels( test_input ), runs=10000000, part2=True ) == expected

def main():
    print('Part 1 Solution = ', naive_simulation( get_labels( '469217538' ) ) )
    print('Part 2 Solution = ', simulate_game( get_labels( '469217538' ), runs=10000000, part2=True ) )

if __name__ == '__main__':
    exit( main() )
