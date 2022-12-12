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
                 locations.append((n_row, n_col))
    return locations

def compute_shortest_path(heightmap, start, part2=False):
    # finds shortest path to all points in a heightmap from start
    if not part2:
        # elevation is a 2D grid with elevation('a')=0,..., elevation('z')=25
        elevation = [[ord(entry)-ord('a') for entry in row] for row in heightmap]
    elif part2:
        # for efficiently solving part2, start from 'E'. Hence invert the elevation to keep the movement rule unchanged
        elevation = [[ord('z')-ord(entry) for entry in row] for row in heightmap] 
    # cost is a dict mapping (x,y) to cost to reach (x,y) from start along shortest path
    # initialized with value = infinity implying unvisited spots
    cost = {(r,c):math.inf for r in range(len(heightmap)) for c in range(len(heightmap[0]))}
    # Visited is a history of points visited by the algorithm
    visited = set()
    # Queue is a list of points to be visited next by the algorithm
    queue = []
    # Update info about starting point
    cost[start] = 0
    visited.add(start)
    queue.append(start)
    # Iterate until queue is empty
    while queue: 
        x0, y0 = queue.pop(0)
        # from each point (x0,y0), find potential point(s) to visit based on rules
        for dx, dy in DIRECTIONS.values():
            x1, y1 = x0 + dx, y0 + dy
            # check if (x1,y1) is within the grid
            if x1 in range(0,len(heightmap)) and y1 in range(0,len(heightmap[0])): 
                # check if (x1,y1) is unvisited (to avoid going back)
                if (x1,y1) not in visited:
                    # checking movement rule: elevation change should be atmost 1
                    if elevation[x1][y1] - elevation[x0][y0] <= 1:
                        # (x1,y1) was visited. Update its shortest path from start 
                        cost[(x1,y1)] = cost[(x0,y0)] + 1
                        visited.add((x1,y1))
                        queue.append((x1,y1))
    # print(f'Visited {len(visited)} out of {len(heightmap)*len(heightmap[0])} grid points')
    return cost

def compute_1(heightmap):
    # In part 1, start is 'S' and end is 'E'
    start = locate_char(heightmap, 'S')[0]
    end   = locate_char(heightmap, 'E')[0]
    # Equivalent elevation: 'S' => 'a', 'E' => 'z'
    heightmap[start[0]][start[1]] = 'a'
    heightmap[end[0]][end[1]]     = 'z'
    # find shortest path from 'S' to all points in heightmap, then find # steps to 'E'
    steps = compute_shortest_path(heightmap, start)
    return steps[end]

def compute_2(heightmap):
    # In part 2, the starting points are all 'a's in the heightmap
    locations_a = locate_char(heightmap, 'a')
    location_S  = locate_char(heightmap, 'S')[0]
    end = locate_char(heightmap, 'E')[0]
    # Equivalent elevation: 'S' => 'a', 'E' => 'z'
    heightmap[location_S[0]][location_S[1]] = 'a'
    heightmap[end[0]][end[1]] = 'z'
    # find the shortest path from 'E' to all points in heightmap, then find # steps to nearest 'a' from 'E'
    steps = compute_shortest_path(heightmap, start=end, part2=True)
    # Thus, the algorithm is executed once starting from 'E', instead of multiple times starting from all 'a's
    # Improved speed from 2.02590 s to 0.02400 s => 84x speedup
    # credits: https://www.reddit.com/r/adventofcode/comments/zjovug/2022_day_12_part_2_big_o_whats_that/
    return min([steps[start] for start in locations_a])

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