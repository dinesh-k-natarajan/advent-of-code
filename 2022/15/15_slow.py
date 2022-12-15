""" 
This script contains the initial code used to submit part 1's solution.
It only works for one y coordinate and took 45 seconds to solve the input puzzle.
This approach using sets was abandoned for part 2 as it needs to loop over 4000000 y's
and would have taken atleast 8 HOURS to solve part 2.
"""
import time
import pytest
import re

def parse_input(filename:str):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [[(int(coords[0]), int(coords[1])) for coords in re.findall(r'x=([+-]?\d+), y=([+-]?\d+)', line)] for line in lines]

def compute_manhattan(sensor:tuple, beacon:tuple):
    """ 
    In R², the manhattan distance between two points is  the sum of the 
    absolute values of the differences in both coordinates.
    """
    return abs(sensor[0]-beacon[0]) + abs(sensor[1]-beacon[1])

def compute_slope(point1:tuple, point2:tuple):
    # Slope, m = (change in y) / (change in x)
    return (point2[1]-point1[1]) // (point2[0]-point1[0])

def get_empty_positions(sensor:tuple, beacon:tuple, y:int):
    """
    WIth sensor as origin, at all points within the manhattan distance between sensor
    and beacon, no other beacons will be found. This function returns a set of such empty positions at the specified y coordinate.

    The manhattan distance forms a diamond with origin as sensor.
    """
    empty_pos = []
    distance = compute_manhattan(sensor, beacon)
    # find tips of the diamond 
    diamond_top    = tuple(s-dist for s,dist in zip(sensor,(0,distance)))
    diamond_bottom = tuple(s+dist for s,dist in zip(sensor,(0,distance)))
    diamond_left   = tuple(s-dist for s,dist in zip(sensor,(distance,0)))
    diamond_right  = tuple(s+dist for s,dist in zip(sensor,(distance,0)))
    # print(f'S:{sensor}, MD:{distance}, DT:{diamond_top}, DB:{diamond_bottom}, DL:{diamond_left}, DR:{diamond_right}')
    # find slopes of the four sides of diamond
    slope_LT = compute_slope(diamond_left, diamond_top)
    slope_LB = compute_slope(diamond_left, diamond_bottom)
    # print(f'slope_LT = {slope_LT}')
    # print(f'slope_LB = {slope_LB}')
    # starting from diamond_top, find all points within the diamond
    if diamond_top[1] <= y < sensor[1]:
        # find x coordinate on line LT using diamond_top
        # x - x1 = (y - y1)/m
        x_left = diamond_top[0] + ((y - diamond_top[1])//slope_LT)
        x_right = x_left + 2*(diamond_top[0] - x_left)
        # print(f'At y={y}, x goes from {x_left} to {x_right}')
        empty_at_y = [(x,y) for x in range(x_left, x_right+1)]
        # print(f'y={y} => {empty_at_y}')
        empty_pos += empty_at_y
    elif sensor[1] <= y < diamond_bottom[1]:
        # find x coordinate on line BL using diamond_left
        # x - x1 = (y - y1)/m
        x_left = diamond_left[0] + ((y - diamond_left[1])//slope_LB)
        x_right = x_left + 2*(diamond_top[0] - x_left)
        # print(f'At y={y}, x goes from {x_left} to {x_right}')
        empty_at_y = [(x,y) for x in range(x_left, x_right+1)]
        # print(f'y={y} => {empty_at_y}')
        empty_pos += empty_at_y
    return set(empty_pos)

def compute_1(pairs, y:int):
    sensors = set()
    beacons = set()
    not_beacons = set()
    for pair in pairs: 
        sensor, beacon = pair
        sensors.add(sensor)
        beacons.add(beacon)
        not_beacons = not_beacons.union(get_empty_positions(sensor,beacon,y))
    # find count of not_beacons at given y coordinate
    return sum(1 for point in not_beacons if point not in beacons.union(sensors))

@pytest.mark.parametrize('test_input,expected', [('15.example',26)])
def test_part1(test_input,expected):
    assert compute_1(parse_input(test_input), y=10) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_1(parse_input('15.in'), y=2000000)}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()