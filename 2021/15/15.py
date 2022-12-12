import time
import pytest
import math

def parse_input(filename):
    with open(filename,'r') as input_file:
        return [[int(entry) for entry in line] for line in input_file.read().splitlines()]

# Movements in a 2D grid represented by a list of lists
DIRECTIONS = {'U':[-1,0], 'D':[1,0], 'L':[0,-1], 'R':[0,1]}

def compute_shortest_path(risks):
    start = (0,0)
    end = (len(risks)-1, len(risks[0])-1)
    costs = {(r,c):math.inf for r in range(end[0]+1) for c in range(end[1]+1)}
    costs[start] = 0
    queue = [start]
    visited = set()
    visited.add(start)
    while queue:
        x0, y0 = queue.pop(0)
        for dx, dy in DIRECTIONS.values():
            x1, y1 = x0 + dx, y0 + dy
            if x1 in range(end[0]+1) and y1 in range(end[1]+1):
                new_cost = costs[(x0,y0)] + risks[x1][y1]
                if new_cost < costs[(x1,y1)]:
                    costs[(x1,y1)] = new_cost
                    queue.append((x1,y1))
                    visited.add((x1,y1))
    print(f'Visited {len(set(visited))} out of {len(risks)*len(risks[0])} grid points')
    return costs[end]

def expand_tiles(risks):
    expanded_risks = [[-1 for _ in range(5*len(risks[0]))] for _ in range(5*len(risks))]
    for n_row in range(len(expanded_risks)):
        for n_col in range(len(expanded_risks[0])):
            new_entry = risks[n_row % len(risks)][n_col % len(risks[0])] + (n_row // len(risks)) + (n_col // len(risks[0])) - 1
            new_entry = (new_entry % 9) + 1
            expanded_risks[n_row][n_col] = new_entry
    return expanded_risks

def compute_2(risks):
    risks = expand_tiles(risks)
    return compute_shortest_path(risks)

@pytest.mark.parametrize('test_input,expected', [('15.example',40)])
def test_part1(test_input,expected):
    assert compute_shortest_path(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('15.example',315)])
def test_part2(test_input,expected):
    expanded_risks = expand_tiles(parse_input(test_input))
    risks_string = '\n'.join([''.join([str(item) for item in row]) for row in expanded_risks])
    assert risks_string == open('15.ex_expanded').read()
    assert compute_2(parse_input(test_input)) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_shortest_path(parse_input('15.in'))}")
    print(f"Part 2 Solution = {compute_2(parse_input('15.in'))}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()