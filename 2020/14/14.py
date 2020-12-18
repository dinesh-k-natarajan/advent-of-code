import pytest
import re
from collections import defaultdict
from itertools import product
from copy import deepcopy

def get_inputs( filename ):
    """
    The input file contains groups of: a mask and values to be written to memory.
    This function returns a program that consists of groups of instructions. 
    Each group is a dictionary with two lists: mask and values.
    Each mask list contains tuples of (position, mask value)
    Each values list contains tuples of (memory address, value)
    """
    with open( filename, 'r' ) as input_file:
        raw_data = [ line for line in input_file.read().splitlines() ]
    mask_begins = [ raw_data.index(line) for line in raw_data if line.startswith('mask') ] 
    mask_begins.append( len(raw_data) )
    groups = [ raw_data[ mask_begins[i]:mask_begins[i+1] ] for i in range(len(mask_begins)-1) ]
    program = []
    for n_group, group in enumerate(groups):
        parsed_group = defaultdict(list)
        for n_entry, entry in enumerate(group):
            if entry.startswith('mask'):
                _ , mask = re.split(' = ', entry)
                parsed_group['mask'] = [ ( i,ch ) for (i,ch) in enumerate(mask) ] 
            elif entry.startswith('mem'):
                address, value = re.findall(r'\d+', entry)
                parsed_group['value'].append( (int(address), int(value)) )
        program.append( parsed_group )
    return program 

def apply_mask( value, mask, part2=False ):
    """
    The value is an integer.
    The mask is in the form of a list of tuples ( bit address, mask value )
    for e.g.: (4, 1) -> 1 is overwritten at bit corresponding to 2^4
    
    For Part 1:
        - if mask entry = X, then corresponding value is unchanged
        - if mask entry = 0 or 1, corresponding value is overwritten

    For Part 2:
        - if mask entry = 0, value is unchanged
        - if mask entry = 1, value is overwritten with 1
        - if mask entry = X, value is floating, i.e., 0 or 1 are both possible
    Based on the possible combinations of floating values, all possible masked 
    addresses are found and returned. 
    """
    bin_string = '{:036b}'.format(value).replace(' ','0')
    bin_masked = [ ch for ch in bin_string ]
    for bit, mask_value in mask:
        if mask_value == 'X' and not part2: continue
        if mask_value == '0' and part2: continue
        bin_masked[bit] = mask_value
    if not part2:
        bin_masked = ''.join( bin_masked )
        return int( bin_masked, 2 )
    elif part2:
        addresses = []
        floating_loc = [ loc for (loc,ch) in enumerate(bin_masked) if ch == 'X' ]
        floating_combos = [ list(item) for item in product( ['0','1'], repeat=len(floating_loc) ) ]
        for combo in floating_combos:
            address = deepcopy( bin_masked ) 
            for i, loc in enumerate(floating_loc):
                address[loc] = combo[i]
            addresses.append( ''.join( address ) )
        return [ int(item,2) for item in addresses ]

def decoder_v1( program ):
    """
    The memory is initialized based on the parsed program.
    Each value is stored in its address after application of the mask.
    This function returns the sum of stored values in the memory at the end of initialization. 
    """
    memory = defaultdict(int)
    for group in program:
        mask = group['mask']
        for value in group['value']:
            raw_value = value[1]
            masked_value = apply_mask( raw_value, mask )
            memory[ value[0] ] = masked_value
    return sum( list( memory.values() ) )

def decoder_v2( program ):
    """
    The difference to decoder_v1 is that the mask is applied to the memory address and not the value.
    The mask also applies X to the memory value which indicates a floating value.
    A floating value can take all combinations of possible values (0,1).
    This generates multiple addresses after application of mask.
    """
    memory = defaultdict(int)
    for group in program:
        mask = group['mask']
        for value in group['value']:
            raw_address = value[0]
            masked_addresses = apply_mask( raw_address, mask, part2=True )
            for address in masked_addresses:
                memory[ address ] = value[1]
    return sum( list( memory.values() ) )

@pytest.mark.parametrize( 'test_input, expected', [ ('14.example1', 165 ) ] )
def test_part1( test_input, expected ):
    assert decoder_v1( get_inputs( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ( '14.example2', 208 ) ] )
def test_part2( test_input, expected ):
    assert decoder_v2( get_inputs( test_input ) ) == expected
def main():
    print('Part 1 Solution = ', decoder_v1( get_inputs('14.in') ) )
    print('Part 2 Solution = ', decoder_v2( get_inputs('14.in') ) )

if __name__ == '__main__':
    exit( main() )
