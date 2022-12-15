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

def get_intervals_at_y(pairs, y:int):
    """ 
    This function finds intervals where beacons cannot be found for a given
    y coordinate. It returns a list of non-overlapping intervals.

    The manhattan distance inequality: d(s,point) <= |sx-bx| + |sy-by| creates a zone
    around the sensor in which no other beacon can be found. It is diamond-shaped.
    """
    intervals = []
    # Create a list of non-beacon intervals for each sensor
    for pair in pairs:
        sensor, beacon = pair
        manhattan_dist = compute_manhattan(sensor, beacon) 
        md_y = abs(y - sensor[1])
        # add intervals within the diamond-zone of a sensor
        if md_y < manhattan_dist: 
            md_x = manhattan_dist - md_y
            intervals.append([sensor[0] - md_x, sensor[0] + md_x])
    # Combine overlapping intervals
    # Reference: https://www.geeksforgeeks.org/merging-intervals/
    intervals.sort()
    merged_intervals = []
    merged_intervals.append(intervals[0])
    for interval in intervals[1:]:
        if merged_intervals[-1][0] <= interval[0] <= merged_intervals[-1][1]: 
            merged_intervals[-1][1] = max(merged_intervals[-1][1], interval[1])
        else:
            merged_intervals.append(interval)
    return merged_intervals

def solve_1(pairs, y:int=None):
    not_beacon_intervals = get_intervals_at_y(pairs, y)
    # Part 1: find number of positions which cannot be a beacon at given y
    # The faster solution is to find the sum of interval lengths without a beacon
    return sum(interval[1]-interval[0] for interval in not_beacon_intervals)

def solve_2(pairs, atmost:int=None):
    for y in range(0, atmost+1):
        potential_beacons = []
        # get intervals where beacons are not possible
        not_beacon_intervals = get_intervals_at_y(pairs, y)
        # if only one interval is found, check for potential beacons
        if len(not_beacon_intervals) == 1:
            interval = not_beacon_intervals.pop()
            flag_left  = (0 <= interval[0])
            flag_right = (interval[1] <= atmost)
            if not flag_left and not flag_right:
                # interval covers [0,atmost] fully => no beacon at this y
                continue # skips everything below to next for loop iteration
            elif flag_left and not flag_right:
                potential_beacons += [(x,y) for x in range(0, interval[0])]
            elif not flag_left and flag_right: 
                potential_beacons += [(x,y) for x in range(interval[1]+1, atmost+1)]
            elif flag_left and flag_right:
                potential_beacons += [(x,y) for x in range(0, interval[0])]
                potential_beacons += [(x,y) for x in range(interval[1]+1, atmost+1)]
        # if more than one interval is found, check for potential beacons
        else:
            # search for each pair of intervals
            for interval1, interval2 in zip(not_beacon_intervals, not_beacon_intervals[1:]):
                # print('\tConsidering two intervals: ', interval1, interval2)
                potential_beacons += [(x,y) for x in range(interval1[1]+1,interval2[0])]
        # Terminating condition: there is only one distress beacon in the puzzle
        if len(potential_beacons) > 0:
            assert len(potential_beacons) == 1
            break
    # Return the tuning frequency of distress beacon
    distress_beacon = potential_beacons.pop()
    print(f'Found distress beacon at coordinates: {distress_beacon}')
    return distress_beacon[0]*4000000 + distress_beacon[1]

@pytest.mark.parametrize('test_input,expected', [('15.example',26)])
def test_part1(test_input,expected):
    assert solve_1(parse_input(test_input), y=10) == expected

@pytest.mark.parametrize('test_input,expected', [('15.example',56000011)])
def test_part2(test_input,expected):
    assert solve_2(parse_input(test_input), atmost=20) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {solve_1(parse_input('15.in'), y=2000000)}")
    print(f"Part 2 Solution = {solve_2(parse_input('15.in'), atmost=4000000)}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()