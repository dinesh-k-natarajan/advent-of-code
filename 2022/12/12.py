import time
import pytest
import math

def parse_input(filename):
    with open(filename,'r') as input_file:
        return [[char for char in line] for line in input_file.read().splitlines()]

# Movement in 2D grid represented by a list of lists with origin at top-left
DIRECTIONS = {'U':[-1,0], 'D':[1,0], 'L':[0,-1], 'R':[0,1]}

def print_grid(grid):
    # for printing and debugging the grid of values
    grid = [[str(entry) for entry in row] for row in grid]
    print('\n'.join(['\t'.join(row) for row in grid]))

def locate_char(heightmap, char):
    locations = []
    for n_row, row in enumerate(heightmap):
        for n_col, entry in enumerate(row):
            if entry == char: 
                 locations.append([n_row, n_col])
    return locations

def compute_shortest_path(heightmap, start, end):
    # elevation is a 2D grid with elevation('a')=1,..., elevation('z')=26
    elevation = [[ord(entry)-ord('a')+1 for entry in row] for row in heightmap]
    # Steps is a 2D grid of shortest path between each point and the start
    # initialized with value = infinity implying unvisited spots
    steps = [[math.inf for _ in range(len(heightmap[0]))] for _ in range(len(heightmap))] 
    # Visited is a list of visited points based on the rules
    visited = []
    # Update starting point
    steps[start[0]][start[1]] = 0
    visited.append(start)
    while visited:
        x0, y0 = visited.pop(0)
        # from each point (x0,y0), find potential point(s) to visit based on rules
        for dx, dy in DIRECTIONS.values():
            x1, y1 = x0 + dx, y0 + dy
            # check if (x1,y1) is within the grid
            if x1 in range(0,len(heightmap)) and y1 in range(0,len(heightmap[0])): 
                # check if (x1,y1) is unvisited (to ensure shortest path, no revisits)
                if steps[x1][y1] == math.inf: 
                    # checking movement rule: elevation change should be atmost 1
                    if elevation[x1][y1] - elevation[x0][y0] <= 1:
                        # (x1,y1) was visited. Update its shortest path from start 
                        steps[x1][y1] = steps[x0][y0] + 1
                        # Add (x1,y1) to the list of visited points
                        visited.append([x1,y1])
    return steps[end[0]][end[1]]

def compute_1(heightmap):
    # In part 1, start is 'S' and end is 'E'
    start = locate_char(heightmap, 'S')[0]
    end   = locate_char(heightmap, 'E')[0]
    # Equivalent elevation: 'S' => 'a', 'E' => 'z'
    heightmap[start[0]][start[1]] = 'a'
    heightmap[end[0]][end[1]]     = 'z'
    # find shortest path from 'S' to 'E'
    return compute_shortest_path(heightmap, start, end)

def compute_2(heightmap):
    # In part 2, the starting points are all 'a's in the heightmap
    locations_a = locate_char(heightmap, 'a')
    location_S  = locate_char(heightmap, 'S')[0]
    end = locate_char(heightmap, 'E')[0]
    # Equivalent elevation: 'S' => 'a', 'E' => 'z'
    heightmap[location_S[0]][location_S[1]] = 'a'
    heightmap[end[0]][end[1]] = 'z'
    # find the shortest path from any 'a' in the heightmap to 'E'
    return min([compute_shortest_path(heightmap, start, end) for start in locations_a])

@pytest.mark.parametrize('test_input,expected', [('12.example',31)])
def test_part1(test_input,expected):
    assert compute_1(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('12.example',29)])
def test_part2(test_input,expected):
    assert compute_2(parse_input(test_input)) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_1(parse_input('12.in'))}")
    print(f"Part 2 Solution = {compute_2(parse_input('12.in'))}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()