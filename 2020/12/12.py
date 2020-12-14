import pytest

def get_inputs( filename ):
    """
    The input file has intructions in each line with a command and a value. 
    This function returns the instructions as a list of lists.
    """
    with open( filename, 'r') as input_file:
        inputs = [ [ item[:1], int(item[1:]) ] for 
                     item in input_file.read().splitlines() ]
    return inputs

def navigate_ship( instructions ):
    """
    From the starting point of the ship (0,0), the ship has to be navigated 
    based on the command and delta mentioned in each instruction.

    The positions are modelled as complex numbers. The direction conventions
    can be understood by referring to move_along dictionary in the code below. 
    Initially, the ship faces east. 
    
    Navigation:
      - If the command is 'F', the ship moves by delta in the same direction. 
      - If the command is ['N','E','W','S'], the ship moves by delta according 
        to the corresponding direction described in move_along.
      - If the command is 'L', the facing direction is rotated counterclockwise.
        i.e., For N to be rotated to W, facing is multiplied by complex(0,1) raised
        to the power of (angle/90) -> 90 = once, 180 = twice, 270 = thrice.
      - If the command is 'R', the facing direction is rotated clockwise.
        i.e., For N to be rotated to E, facing is multiplied by complex(0,-1) raised
        to the power of (angle/90) -> 90 = once, 180 = twice, 270 = thrice.

    Task:
    This function returns the manhattan distance of the position from starting
    point which was (0,0) -> distance = abs(real) + abs(imag)
    """
    position    = complex(0,0)
    move_along  = {'N': complex( 0, 1), 'S': complex( 0,-1),
                   'E': complex( 1, 0), 'W': complex(-1, 0) }
    facing      = move_along['E']
    for command, delta in instructions:
        if command == 'F':
            position += delta * facing
        elif command in ['N','E','W','S']:
            position += delta * move_along[ command ]
        elif command == 'L':
            facing *= complex(0, 1) ** (delta//90)
        else:
            assert command == 'R'
            facing *= complex(0,-1) ** (delta//90)            
    return int(abs(position.real)+abs(position.imag))

def navigate_waypoint( instructions ):
    """
    From the starting point of the ship (0,0) and the ship's waypoint at (10,1), 
    the ship has to be navigated based on the command and delta mentioned 
    in each instruction. The waypoint is a reference point relative to the
    ship, and it moves with the ship.

    The positions are modelled as complex numbers. The direction conventions
    can be understood by referring to move_along dictionary in the code below.  
    
    Navigation:
      - If the command is 'F', the ship moves by delta times the waypoint. 
      - If the command is ['N','E','W','S'], the waypoint moves by delta according 
        to the corresponding direction described in move_along.
      - If the command is 'L', the waypoint is rotated counterclockwise.
        i.e., For N to be rotated to W, waypoint is multiplied by complex(0,1) raised
        to the power of (angle/90) -> 90 = once, 180 = twice, 270 = thrice.
      - If the command is 'R', the waypoint is rotated clockwise.
        i.e., For N to be rotated to E, waypoint is multiplied by complex(0,-1) raised
        to the power of (angle/90) -> 90 = once, 180 = twice, 270 = thrice.

    Task:
    This function returns the manhattan distance of the position from starting
    point which was (0,0) -> distance = abs(real) + abs(imag)
    """
    position    = complex(0,0)
    move_along  = {'N': complex( 0, 1), 'S': complex( 0,-1),
                   'E': complex( 1, 0), 'W': complex(-1, 0) }
    waypoint    = complex(10,1)
    for command, delta in instructions:
        if command == 'F':
            position += delta * waypoint
        elif command in ['N','E','W','S']:
            waypoint += delta * move_along[ command ]
        elif command == 'L':
            waypoint *= complex(0, 1) ** (delta//90)
        else:
            assert command == 'R'
            waypoint *= complex(0,-1) ** (delta//90)            
    return int(abs(position.real)+abs(position.imag))

@pytest.mark.parametrize( 'test_input, expected', [ ('12.example', 25) ] )
def test_part1( test_input, expected ):
    assert navigate_ship( get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('12.example', 286) ] )
def test_part2( test_input, expected ):
    assert navigate_waypoint( get_inputs(test_input) ) == expected

def main():
    print('Part 1 Solution = ', navigate_ship(     get_inputs('12.in') ) )
    print('Part 2 Solution = ', navigate_waypoint( get_inputs('12.in') ) )

if __name__ == '__main__':
    exit( main())
