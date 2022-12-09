import time
import pytest

def parse_input( filename ):
    with open(filename,'r') as input_file:
        actions = [line.split(' ') for line in input_file.read().splitlines()]
        return [[action[0], int(action[1])] for action in actions]

# Directions of movement (x=horizontal, y=vertical)
DIRECTION = {'U':(0,1),'D':(0,-1),'R':(1,0),'L':(-1,0)}
# whether x,y coordinate is positive(True) or negative (False)
QUADRANTS = {(True,True):'Q1',(False,True):'Q2',(False,False):'Q3',(True,False):'Q4'}
# Diagonal to move into a specific quadrant
DIAGONAL  = {'Q1':(1,1),'Q2':(-1,1),'Q3':(-1,-1),'Q4':(1,-1)}

def check_separation( H, T ):
    # T should be in contact with H either adjacently or diagonally
    if sum(item**2 for item in [h-t for h,t in zip(H,T)])<=2:
        # |difference| in [(0,0), (0,1), (1,0), (1,1)] => in contact
        return False
    else:
        return True

def move_tail( H, T ):
    # Assumed that H,T are separated and T must be moved
    diff = tuple(h-t for h,t in zip(H,T))
    # if H,T are in the same row or column
    if diff[0]*diff[1] == 0:
        # since actions are applied step-by-step, max(diff) is usually 2
        # find unit vector from diff to move T in that direction 
        move = tuple(item//2 for item in diff)
        T = tuple(t+m for t,m in zip(T,move))
    # if H,T aren't in the same row or column
    else:
        # find which quadrant the diff lies in
        quad = QUADRANTS[tuple(item>0 for item in diff)]
        # move T diagonally to that quadrant
        T = tuple(t+d for t,d in zip(T, DIAGONAL[quad]))
    return T 

def count_visited_positions( actions, n_knots=2 ):
    origin=(0,0)
    # all knots start at the origin
    knots = {rope:[origin] for rope in range(n_knots)}
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