import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [[line.split(' ')[0], int(line.split(' ')[1])] for line in lines] 

def compute_position( commands ):
    x = 0
    depth = 0
    for command in commands:
        direction, distance = command
        if direction == 'forward': 
            x += distance
        elif direction == 'down': 
            depth += distance
        elif direction == 'up': 
            depth -= distance
    return x * depth

def compute_corrected_position( commands ):
    x = 0
    depth = 0
    aim = 0
    for command in commands:
        direction, distance = command
        if direction == 'forward': 
            x += distance
            depth += aim * distance
        elif direction == 'down': 
            aim += distance
        elif direction == 'up': 
            aim -= distance
    return x * depth

@pytest.mark.parametrize( 'test_input,expected', [ ('2.example', 150) ] )
def test_part1( test_input, expected ):
    assert compute_position( get_input( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('2.example', 900) ] )
def test_part2( test_input, expected ):
    assert compute_corrected_position( get_input( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', compute_position( get_input('2.in') ))
    print('Part 2 Solution = ', compute_corrected_position( get_input('2.in') ))

if __name__ == '__main__':
    main()
