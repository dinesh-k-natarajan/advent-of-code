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
        return False
    else:
        return True

def move_tail( H, T ):
    # Assumed that H,T are separated and T must be moved
    diff = tuple(h-t for h,t in zip(H,T))
    # if H,T are in the same row or column
    if diff[0]*diff[1] == 0: 
        move = tuple(item//2 for item in diff)
        T = tuple(t+m for t,m in zip(T,move))
    # if h,t aren't in the same row or column
    else:
        quad = QUADRANTS[tuple(item>0 for item in diff)]
        T = tuple(t+d for t,d in zip(T, DIAGONAL[quad]))
    return T 

def compute_1( actions ):
    origin = (0,0)
    H_path = [origin]
    T_path = [origin]
    for action in actions:
        dir, dist = action
        H = H_path[-1]
        T = T_path[-1]
        for _ in range(dist):
            H = tuple(h+direc for h,direc in zip(H,DIRECTION[dir]))
            H_path.append(H)
            if check_separation(H,T):
                T = move_tail(H,T)
                T_path.append(T)
    return len(set(T_path))

def compute_2( actions ):
    origin=(0,0)
    # Head rope and 9 tail ropes
    ropes = {rope:[origin] for rope in range(10)}
    for action in actions:
        dir, dist = action
        H = ropes[0][-1]
        for _ in range(dist):
            H = tuple(h+direc for h,direc in zip(H,DIRECTION[dir]))
            ropes[0].append(H)
            # Check separation and move tail of each 2 ropes
            for i in range(1,10):
                if check_separation(ropes[i-1][-1],ropes[i][-1]):
                    T = move_tail(ropes[i-1][-1],ropes[i][-1])
                    ropes[i].append(T)
    return len(set(ropes[9]))

@pytest.mark.parametrize( 'test_input,expected', [ ('09.example', 13) ] )
def test_part1( test_input, expected ):
    assert compute_1( parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('09.example', 1), ('09.example2', 36) ] )
def test_part2( test_input, expected ):
    assert compute_2( parse_input(test_input) ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', compute_1( parse_input('09.in') ))
    print('Part 2 Solution = ', compute_2( parse_input('09.in') ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()