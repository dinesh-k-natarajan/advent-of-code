import pytest
from copy import deepcopy

def get_inputs( filename ):
    """
    The input file is in the form of lines of instructions with a command
    and a value. For each line in the input file, an instructions list is
    created which contains a list [command, value]
    e.g.: instructions = [ ['acc','+50'], ['acc','-11'], .... ]
    """
    with open( filename, 'r') as input_file:
        lines = input_file.read().splitlines()
    instructions = []
    for line in lines:
        instructions.append( line.split(' ') )
    return instructions

def execute( instructions ):
    """
    Execute the given instructions and return the accumulator value before
    the beginning of an infinite loop. If an instruction was already visited
    or the end of the instructions is reached, the loop is terminated. 
    At the end of the run, the accumulator value altered by the 'acc' and a 
    boolean which describes whether an infinite loop was reached is returned.
    """
    accumulator  = 0
    visited      = set()
    location     = 0
    while location not in visited and location < len(instructions):
        visited.add( location )
        command, delta = instructions[location]
        if command == 'nop':
            location += 1
        elif command == 'acc':
            accumulator += int( delta )
            location += 1
        elif command == 'jmp':
            location += int( delta )
        else:
            raise ValueError('Instructions unclear, should be nop, acc or jmp')
    infinite_loop = location != len(instructions)
    return accumulator, infinite_loop

def get_accumulator( instructions, part2=False ):
    """
    For Part 1: Simply call the execute function and return the acc value.
    For Part 2: Make a deepcopy of the instructions, so that it can be modified.
    For every instruction, alter 'jmp' to 'nop' or viceversa and check if the 
    infinite loop is avoided from the execute function. Since only one command
    can be changed, the loop is terminated as soon as the infinite loop flag == 'False'    
            *** Part 2 Solution partly inspired by user: elvinyhlee *** 
    """
    if not part2:
        accumulator, _ = execute( instructions )
        return accumulator
    elif part2:
        for location, instruction in enumerate( instructions ):
            command, _ = instruction
            instructions_modified = deepcopy( instructions )
            if command != 'acc':
                if command == 'nop':
                    instructions_modified[location][0] = 'jmp'
                else:
                    instructions_modified[location][0] = 'nop'
                accumulator, infinite_loop = execute( instructions_modified )
                if not infinite_loop:
                    return accumulator

@pytest.mark.parametrize( 'test_input, expected', [ ('8.example', 5) ] )
def test_part1( test_input, expected ):
    assert get_accumulator( get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('8.example', 8) ] )
def test_part2( test_input, expected ):
    assert get_accumulator( get_inputs(test_input), part2=True ) == expected

def main():
    print('Part 1 Solution = ', get_accumulator( get_inputs('8.in') ) )
    print('Part 2 Solution = ', get_accumulator( get_inputs('8.in'), part2=True ) )

if __name__ == '__main__':
    exit( main())
