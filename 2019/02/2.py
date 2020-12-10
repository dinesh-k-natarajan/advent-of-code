import pytest

def get_inputs():
    with open( '2.in','r' ) as input_file:
        inputs = input_file.read().split(',')
        inputs = [ int(item) for item in inputs]
    return inputs

def intcode_program( initial ):
    final = initial.copy()
    for i in range( 0, len(initial), 4 ):
        if final[i] == 99:
            break
        elif final[i] == 1:
            final[ initial[i+3] ] = final[ initial[i+1] ] + final[ initial[i+2] ] 
        elif final[i] == 2:
            final[ initial[i+3] ] = final[ initial[i+1] ] * final[ initial[i+2] ]
        else:
            raise ValueError('Unknown opcode. Something went wrong!')
    return final

def inverse_intcode( initial, value_0 ):
    for value_1 in range( 100 ):
        for value_2 in range( 100 ):
            modified_initial = initial.copy()
            modified_initial[1] = value_1
            modified_initial[2] = value_2
            final = intcode_program( modified_initial )
            if final[0] == value_0:
                return value_1, value_2

@pytest.mark.parametrize('test_inputs,expected',
                            [ ([1,0,0,0,99],[2,0,0,0,99]),
                              ([2,3,0,3,99],[2,3,0,6,99]),
                              ([2,4,4,5,99,0],[2,4,4,5,99,9801]),
                              ([1,1,1,4,99,5,6,0,99],[30,1,1,4,2,5,6,0,99]) ] ) 
def test_part1( test_inputs, expected ):
    assert intcode_program( test_inputs ) == expected

@pytest.mark.parametrize( 'inputs, part1_values, part1_solution', 
                            [ (get_inputs(), (12,2), 3166704) ] )
def test_part2( inputs, part1_values, part1_solution ):
    assert inverse_intcode( inputs, part1_solution ) == part1_values

def main():
    inputs = get_inputs()
    # Part 1
    inputs_part1 = inputs.copy()
    inputs_part1[1] = 12
    inputs_part1[2] = 2
    outputs_part1   = intcode_program( inputs_part1 )
    print('Part 1 Solution = ', outputs_part1[0])
    # Part 2
    inputs_part2 = inputs.copy()
    value_0 = 19690720
    value_1, value_2 = inverse_intcode( inputs_part2, value_0 )
    print('Part 2 Solution = ', 100 * value_1 + value_2 )

if __name__ == '__main__':
    exit( main() )
