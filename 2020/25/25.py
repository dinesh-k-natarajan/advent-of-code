import pytest

def get_inputs( filename ):
    """
    The input file contains two numbers - door's public key and card's public key.
    """
    with open( filename ) as input_file:
        return [ int(number) for number in  input_file.read().splitlines() ]

def find_loop_size( public_key, subject=7 ):
    """
    To transform a subject number, start with the value 1. 
    
    Then, a number of times called the loop size, perform the following steps:
        - Set the value to itself multiplied by the subject number.
        - Set the value to the remainder after dividing the value by 20201227
    
    After the desired loop size, the subject number 7 is transformed into the 
    public key itself.
    """
    loops = 0
    value = 1
    while value != public_key:
        loops += 1
        value *= subject
        value = value % 20201227
    return loops

def find_encryption( public_key, loops ):
    """
    Starting from the given public_key, this function applies the transformation
    for loops times and returns the value
    """
    value = 1
    for _ in range(loops):
        value *= public_key
        value = value % 20201227
    return value        

def decode_encryption( card, door ):
    """
    This function returns the encryption key based on the card's and door's public keys.
    """
    card_loop_size = find_loop_size( card, subject=7 )
    door_loop_size = find_loop_size( door, subject=7 )
    key = find_encryption( door, card_loop_size )
    assert find_encryption( card, door_loop_size ) == key
    return key

@pytest.mark.parametrize( 'test_input, expected', [ ('25.example', 14897079 ) ] )
def test_part1( test_input, expected ):
    assert decode_encryption( *get_inputs( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', decode_encryption( *get_inputs( '25.in' ) ) )
    print('Part 2 Solution =  Mission Complete!' )

if __name__ == '__main__':
    main()
