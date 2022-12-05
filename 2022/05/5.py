import time
import pytest
import re

def parse_input( filename ):
    with open(filename,'r') as input_file:
        part1, part2 = input_file.read().split('\n\n')
        # Find column indices of the stack using the stack number on the last row
        column_idx = [pos for pos,char in enumerate(part1.splitlines()[-1]) if char.isdigit()]
        # Extract the crates from the stack
        stacks = [[line[idx] for idx in column_idx]for line in part1.splitlines()[:-1]]
        # Transpose the stacks, such that each column(stack) is a list
        stacks = [[crate for crate in stack[::-1] if crate!=' '] for stack in list(map(list, zip(*stacks)))]
        # Extract the three integers per line of procedure
        procedure = [[int(item) for item in re.findall(r'[0-9]+', line)] for line in part2.splitlines()]
        return stacks, procedure

def find_top_crates_CM9000( stacks, procedure ):
    for num_crates, source, dest in procedure:
        # Pop out the last num_crates from source stack
        removed_crates = [stacks[source-1].pop() for _ in range(num_crates)]
        # Add crates one-by-one to destination stack
        stacks[dest-1].extend(removed_crates)
    return ''.join([stack.pop() for stack in stacks])

def find_top_crates_CM9001( stacks, procedure ):
    for num_crates, source, dest in procedure:
        # Pop out the last num_crates from source stack
        removed_crates = [stacks[source-1].pop() for _ in range(num_crates)]
        # Add multiple crates together to destination stack (order is reversed now)
        stacks[dest-1].extend(removed_crates[::-1])
    return ''.join([stack.pop() for stack in stacks])

@pytest.mark.parametrize( 'test_input,expected', [ ('5.example', 'CMZ') ] )
def test_part1( test_input, expected ):
    assert find_top_crates_CM9000( *parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('5.example', 'MCD') ] )
def test_part2( test_input, expected ):
    assert find_top_crates_CM9001( *parse_input(test_input) ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', find_top_crates_CM9000( *parse_input('5.in') ))
    print('Part 2 Solution = ', find_top_crates_CM9001( *parse_input('5.in') ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()