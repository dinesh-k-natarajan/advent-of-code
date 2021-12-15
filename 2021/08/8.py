import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [ [digit.split(' ') for digit in line.split(' | ')] for line in lines ]         

def count_1478( entries ):
    segments_1478 = [ 2, 4, 3, 7 ]
    count = 0
    for entry in entries:
        count += len( [ digit for digit in entry[1] if len(digit) in segments_1478 ] )
    return count

def decode_values( entry ):
    segments_1478 = [ 2, 4, 3, 7 ]
    lengths = { 2:'1', 3:'7', 4:'4', 5:{'2','3','5'}, 6:{'0','6','9'}, 7:'8' }  
    signal_patterns, encoded_outputs = entry
    decoded_values = signal_patterns.copy()
    legend = dict()
    decoded_outputs = []
    for i, encoded_pattern in enumerate( signal_patterns ):
        if len(encoded_pattern) in segments_1478:
            decoded_values[i] = lengths[ len(encoded_pattern) ]
            legend[ decoded_values[i] ] = set( encoded_pattern )
        else: decoded_values[i] = lengths[ len(encoded_pattern) ]  
    for i, encoded_pattern in enumerate( signal_patterns ):
        while not isinstance( decoded_values[i], str ):
            if decoded_values[i].issubset( lengths[5] ):
                flag_3 = legend['7'].issubset( set(encoded_pattern) )
                flag_5 = len( set(encoded_pattern).intersection( legend['4'] ) ) == 3
                if flag_3: decoded_values[i] = '3'
                elif not flag_3 and flag_5: decoded_values[i] = '5'
                elif not flag_3 and not flag_5: decoded_values[i] = '2'
                legend[ decoded_values[i] ] = set( encoded_pattern )
            elif decoded_values[i].issubset( lengths[6] ):
                flag_9 = legend['4'].issubset( set(encoded_pattern) )
                flag_0 = legend['7'].issubset( set(encoded_pattern) )
                if flag_9: decoded_values[i] = '9'
                elif not flag_9 and flag_0: decoded_values[i] = '0'
                elif not flag_9 and not flag_0: decoded_values[i] = '6'
                legend[ decoded_values[i] ] = set( encoded_pattern )
    for encoded_output in encoded_outputs:
        decoded_outputs += [ key for key, value in legend.items() if set(encoded_output) == value ]
    return int( ''.join(decoded_outputs) )

def compute_sum( entries ):
    sum_outputs = 0
    for entry in entries:
        sum_outputs += decode_values( entry )
    return sum_outputs

@pytest.mark.parametrize( 'test_input,expected', [ ('8.example', 26 ) ] )
def test_part1( test_input, expected ):
    assert count_1478( get_input( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('8.example', 61229 ) ] )
def test_part2( test_input, expected ):
    assert compute_sum( get_input( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', count_1478( get_input('8.in') ) )
    print('Part 2 Solution = ', compute_sum( get_input('8.in') ) )

if __name__ == '__main__':
    main()
