import time
import pytest

def parse_input( filename ):
    with open(filename,'r') as input_file:
        actions = [line.split(' ') for line in input_file.read().splitlines()]
        return [[action[0], int(action[1])] for action in actions]

# Directions of movement (x=horizontal, y=vertical)
DIRECTION = {'U':(0,1),'D':(0,-1),'R':(1,0),'L':(-1,0)}
# Binarize function to map True -> 1, False -> -1
binarize = lambda boolean: 1 if boolean else -1

def check_separation( H, T ):
    # T should be in contact with H either adjacently or diagonally
    # ||difference||² <=2 -> in contact, >2 -> separated
    return sum(item**2 for item in [h-t for h,t in zip(H,T)]) > 2

def move_tail( H, T ):
    # Assumed that H,T are separated and T must be moved
    diff = tuple(h-t for h,t in zip(H,T))
    # if H,T are in the same row or column
    if 0 in diff:
        # since actions are applied step-by-step, max(diff) is usually 2
        # find unit vector from diff to move T in that direction 
        unit_vector = tuple(item//2 for item in diff)
    # if H,T aren't in the same row or column
    else:
        # move T by unit diagonal to the quadrant in which diff lies
        # Unit diagonals = Q1:(1,1),Q2:(-1,1),Q3:(-1,-1),Q4:(1,-1)
        unit_vector = tuple(binarize(item>0) for item in diff)
    return tuple(t+u for t,u in zip(T,unit_vector))

def count_visited_positions( actions, n_knots=2 ):
    # all knots start at the origin
    knots = {knot:[(0,0)] for knot in range(n_knots)}
    for action in actions:
        dir, dist = action
        # First knot is the Head
        H = knots[0][-1]
        # Move the head step-by-step based on action
        for _ in range(dist):
            H = tuple(h+direc for h,direc in zip(H,DIRECTION[dir]))
            knots[0].append(H)
            # Looping over all non-head knots
            for i in range(1,n_knots):
                # Check separation of previous and next knots
                if check_separation(knots[i-1][-1],knots[i][-1]):
                    # If separated, move tail knot based on previous knot
                    T = move_tail(knots[i-1][-1],knots[i][-1])
                    knots[i].append(T)
    return len(set(knots[n_knots-1]))

@pytest.mark.parametrize( 'test_input,expected', [ ('09.example', 13) ] )
def test_part1( test_input, expected ):
    assert count_visited_positions( parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('09.example', 1), ('09.example2', 36) ] )
def test_part2( test_input, expected ):
    assert count_visited_positions( parse_input(test_input), n_knots=10 ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', count_visited_positions( parse_input('09.in') ))
    print('Part 2 Solution = ', count_visited_positions( parse_input('09.in'), n_knots=10 ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()