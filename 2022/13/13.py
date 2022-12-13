import time
import pytest
from itertools import zip_longest
from functools import cmp_to_key

def parse_input(filename):
    with open(filename,'r') as input_file:
        return [pair.splitlines() for pair in input_file.read().split('\n\n')]

# Convert 1 => True, -1 => False, None => None
get_bool = lambda i: i>0 if i is not None else None

def check_order(list1, list2):
    """ 
    Given two lists, checks if list1 is smaller than list2 based on given rules.
    If True => 1, False => -1, equal => None.
    NOTE: Uncomment prints to compare with example ans in the puzzle description
    """
    # print(f'Checking {list1} vs {list2}..')
    for x,y in zip_longest(list1, list2):
        # print(f'Comparing {x} vs {y}')
        if x is None and y is not None:
            # print('Left ran out of items')
            return 1
        elif x is not None and y is None:
            # print('Right ran out of items')
            return -1
        elif isinstance(x,int) and isinstance(y,int):
            # print('int vs int')
            if x < y:
                # print('Left is smaller')
                return 1
            elif x > y:
                # print('Right is smaller')
                return -1
            else:
                # print('Tie')
                continue
        elif isinstance(x,int) and isinstance(y,list):
            # print('int vs list')
            is_ordered = check_order([x], y)
        elif isinstance(x,list) and isinstance(y,int):
            # print('list vs int')
            is_ordered = check_order(x, [y])
        elif isinstance(x,list) and isinstance(y,list):
            # print('list vs list')
            is_ordered = check_order(x,y)
        if is_ordered is not None:
            return is_ordered

def compute_1(pairs):
    """
    Compute the sum of indices (starts from 1) of pairs which are in the right order
    """
    flags = [None for _ in pairs]
    for idx, pair in enumerate(pairs):
        list1 = eval(pair[0])
        list2 = eval(pair[1])
        # print(f'Starting comparison of {list1} vs {list2}') 
        flags[idx] = check_order(list1.copy(), list2.copy())
        # print(f'Pair {idx+1} in right order?: {get_bool(flags[idx])}')
        # print(60*'-')
    return sum([idx+1 for idx,flag in enumerate(flags) if get_bool(flag)])

def compute_2(pairs):
    """ 
    Treating the pairs as a list of signals, append [[2]] and [[6]] to signals.
    Sort the signals in ascending order, compute product of indices of new signals.
    """
    signals = [eval(list) for pair in pairs for list in pair]
    signals.append([[2]])
    signals.append([[6]])
    """ 
    list.sort() method takes an argument key which can be used to rank the items.
    itertools.cmp_to_key accepts a function as argument to compare and rank two items.
    """
    signals.sort(key=cmp_to_key(check_order), reverse=True)
    return (signals.index([[2]])+1)*(signals.index([[6]])+1)

@pytest.mark.parametrize('test_input,expected', [('13.example',13)])
def test_part1(test_input,expected):
    assert compute_1(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('13.example',140)])
def test_part2(test_input,expected):
    assert compute_2(parse_input(test_input)) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_1(parse_input('13.in'))}")
    print(f"Part 2 Solution = {compute_2(parse_input('13.in'))}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()