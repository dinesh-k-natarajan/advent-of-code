import time
import pytest
import re
from collections import defaultdict
from itertools import product

def parse_input(filename):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [[(int(coords[0]),int(coords[1])) for coords in re.findall(r'(\d+),(\d+)', line)] for line in lines]

# function that returns the sign of the number, 1 if 0 or positive, -1 if negative
get_sign = lambda num: 1 if num>=0 else -1

def diff_range(start, end):
    """ Given two points, this function: 
        (1) finds difference between the two points in x,y coordinates
        (2) finds signs of the differences
        (3) returns the ranges of the difference in x,y coordinates
    Examples: 
    if dx,dy = (0,-3): returns range(0,-4,-1) = [0,-1,-2,-3]
    if dx,dy = (0, 3): returns range(0, 4, 1) = [0, 1, 2, 3] """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    sign_x = get_sign(dx)
    sign_y = get_sign(dy)
    return range(0, dx+sign_x, sign_x), range(0, dy+sign_y, sign_y)


""" Subclassing of collections.defaultdict to allow default values based on the key
Usage: d = DefaultDict(lambda key: key + 5)
Reference: https://stackoverflow.com/a/65902222 """
class DefaultDict(defaultdict):
    def __missing__(self, key):
        return self.default_factory(key)

# Source of sand inflow is given
SAND_SOURCE = (500,0)

def draw_cave(rock_paths, part2=False):
    """ Cave is a 2D grid: origin (0,0) is top-left, x: right, y: down.
    Cave is represented as a dict of coordinates and their associated material types. 
       
    Material types: 
        rock         : # 
        air          : . (default)
        sand source  : +
        sand at rest : o

    For part 2: 
    if y_max is the highest y coordinate of the cave, there is a floor at y = y_max + 2.
    It stretches in x-direction from -∞ to +∞.  """
    if part2:
        floor = 2 + max(coords[1] for path in rock_paths for coords in path)
        cave = DefaultDict(lambda key: '#' if key[1]==floor else '.')
    else: 
        cave = defaultdict(lambda: '.')
    cave[SAND_SOURCE] = '+'
    for rock_path in rock_paths:
        for start, end in zip(rock_path, rock_path[1:]):
            for i,j in product( *diff_range(start,end)):
                cave[(start[0]+i, start[1]+j)] = '#'
    return cave

def find_bounds(cave):
    top = min(coords[1] for coords in cave.keys())
    bottom = max(coords[1] for coords in cave.keys())
    left = min(coords[0] for coords in cave.keys())
    right = max(coords[0] for coords in cave.keys())
    return top, bottom, left, right

def in_bounds(coords, bounds):
    top, bottom, left, right = bounds
    return (left <= coords[0] <= right) and (top <= coords[1] <= bottom)

# Movement dictionary
MOVEMENTS = {'D':(0,1), 'DL':(-1,1), 'DR':(1,1)}

def find_equilibrium(cave, part2=False):
    """ This function simulates the sand filling and returns the units of sand required 
    before equilibrium is reached. Equilibrium implies that sand flows out of bounds 
    of the cave into the abyss.

    Movement hierarchy of sand: try next move if location is blocked
        (1) down one
        (2) down one, left
        (3) down one, right
        (4) comes to rest
    
    For part 2: The equilibrium condition is different. Stop if a unit of sand comes 
    to rest at the SAND_SOURCE. 
    
    NOTE: Print statements are the documentation. """
    bounds = find_bounds(cave)
    n_sand = 0
    if_equilibrium = False
    while not if_equilibrium:
        current_pos = SAND_SOURCE
        sand_state = '*'
        # print(f'Dropping sand #{n_sand}')
        while sand_state != 'o':
            # print(f'Current position: {current_pos}')
            if not part2: 
                if if_equilibrium:= not in_bounds(current_pos, bounds):
                    # print(f'Sand #{n_sand} went out of bounds at {current_pos}')
                    break
            next_pos = tuple(i+j for i,j in zip(current_pos, MOVEMENTS['D']))
            # print(f'\tChecking coordinate {next_pos}')
            if cave[next_pos] == '.':
                # print(f'\t\tCoordinate {next_pos} is free. Moving down...')
                current_pos = next_pos
                continue
            elif cave[next_pos] in ['#', 'o']:
                # print(f'\t\t{next_pos} is blocked by {cave[next_pos]}. Moving DL.')
                new_pos = tuple(i+j for i,j in zip(current_pos, MOVEMENTS['DL']))
                if cave[new_pos] not in ['#', 'o']:
                    # print(f'\t\t{new_pos} is not blocked by {cave[new_pos]}. Updating current_pos as {new_pos}.')
                    # Before continuing to next while iteration, update current_pos
                    current_pos = new_pos
                    continue
                else:
                    # print(f'\t\t{new_pos} is blocked by {cave[new_pos]}! Moving DR.')
                    new_pos = tuple(i+j for i,j in zip(current_pos, MOVEMENTS['DR']))
                    if cave[new_pos] not in ['#', 'o']:
                        # print(f'\t\t{new_pos} is not blocked by {cave[new_pos]}. Updating current_pos as {new_pos}.')
                        # Before continuing to next while iteration, update current_pos
                        current_pos = new_pos
                        continue
                    else: 
                        # print(f'\tAll options exhausted. Sand #{n_sand} comes to rest at {current_pos}')
                        # print(50*'o')
                        sand_state = 'o'
                        cave[current_pos] = sand_state
                        n_sand += 1
                        if part2: 
                            if if_equilibrium := current_pos == SAND_SOURCE:
                                break
    return n_sand

def compute_1(rock_paths):
    cave = draw_cave(rock_paths)
    return find_equilibrium(cave)

def compute_2(rock_paths):
    cave = draw_cave(rock_paths, part2=True)
    return find_equilibrium(cave, part2=True)

@pytest.mark.parametrize('test_input,expected', [('14.example',24)])
def test_part1(test_input,expected):
    assert compute_1(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('14.example',93)])
def test_part2(test_input,expected):
    assert compute_2(parse_input(test_input)) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_1(parse_input('14.in'))}")
    print(f"Part 2 Solution = {compute_2(parse_input('14.in'))}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()