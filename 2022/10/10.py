import time
import pytest

def parse_input(filename):
    with open(filename,'r') as input_file:
        return [line.split(' ') for line in input_file.read().splitlines()]

def compute_signal_strengths(instructions):
    # find sum of signal strengths DURING (not after) the specified cycles
    X = [1]
    for instruction in instructions:
        if instruction[0]=='noop':
            # no operation, signal remains same
            X.append(X[-1])
        elif instruction[0]=='addx':
            # nothing happens in first cycle
            X.append(X[-1])
            # add value to previous signal in second cycle
            X.append(X[-1]+int(instruction[1]))
    cycles = [20,60,100,140,180,220]
    return sum(cycle*X[cycle-1] for cycle in cycles) #NOTE: X[cycle-1] -> DURING

def draw_pixel(CRT,sprite_pos,cycle):
    # This function draws a pixel with either # or . and increments cycle
    ## get row,col to draw on CRT
    row,col = cycle//40,cycle%40
    # vertical pos of sprite is purely determined by current cycle
    sprite_pos[0] = row
    if sprite_pos[1] in list(range(col-1,col+2)):
        # if current pixel overlaps with sprite ###, draw #
        CRT[row][col]='#'
    else:
        CRT[row][col]='.'
    return CRT,sprite_pos,cycle+1
    
def decode_CRT(instructions):
    # CRT is a 2D grid of 40 columns and 6 rows starting from top left
    CRT = [['0' for _ in range(40)] for _ in range(6)]
    # The sprite is ### with location [row,col] in CRT
    sprite_pos = [0,1]
    cycle = 0
    for instruction in instructions:
        if instruction[0]=='noop':
            # no operation w.r.t sprite, only draw pixels on CRT
            CRT,sprite_pos,cycle = draw_pixel(CRT,sprite_pos,cycle)
        elif instruction[0]=='addx':
            # draw pixels on CRT for 2 cycles
            for _ in range(2):
                CRT,sprite_pos,cycle = draw_pixel(CRT,sprite_pos,cycle)
            # at the end of 2nd cycle, update sprite_pos based on instruction
            sprite_pos[1] += int(instruction[1])
    return '\n'.join([''.join(row) for row in CRT])

@pytest.mark.parametrize('test_input,expected', [('10.example',13140)])
def test_part1(test_input,expected):
    assert compute_signal_strengths(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('10.example','10.ex_solution')])
def test_part2(test_input,expected):
    assert decode_CRT(parse_input(test_input)) == open(expected,'r').read()

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_signal_strengths(parse_input('10.in'))}")
    print(f"Part 2 Solution = \n{decode_CRT(parse_input('10.in'))}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()