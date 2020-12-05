import pytest 

def get_input( filename ):
    with open(filename,'r') as input_file:
        inputs = input_file.read().splitlines()
    return inputs

def locate_seat( boarding_pass ):
    def get_partition( low, high, b_pass, region ): 
        if b_pass != '':
            if b_pass[0] == region[0]:
                low  = low
                high = (high + low - 1)//2
                return get_partition( low, high, b_pass[1:], region )
            elif b_pass[0] == region[1]:
                low  = (high + low + 1)//2
                high = high
                return get_partition( low, high, b_pass[1:], region )
            else:
                raise ValueError('invalid region, should be F or B')
        else:
            assert low == high
            return low

    row = get_partition( 0, 127, boarding_pass[:-3], ['F','B'] )
    col = get_partition( 0, 7,   boarding_pass[-3:], ['L','R'] )
    return row * 8 + col

def decode_seats( boarding_passes ):
    seat_ids = []
    for boarding_pass in boarding_passes:
        seat_ids.append( locate_seat( boarding_pass ) )
    return seat_ids

def find_seat( boarding_passes ):
    taken_seats = decode_seats( boarding_passes )
    all_seats   = set( [ *range( max( taken_seats )+1 ) ] )
    free_seats  = all_seats - set(taken_seats)
    for seat in free_seats:
        if seat-1 not in free_seats and seat+1 not in free_seats:
            my_seat = seat
    return my_seat

@pytest.mark.parametrize('example, expected', [ (['FBFBBFFRLR'], 357) ] )
def test( example, expected ):
    assert max( decode_seats( example ) ) == expected

def main():
    boarding_passes = get_input( '5.in' )
    print('Part 1 Solution = ', max( decode_seats( boarding_passes ) ) )
    print('Part 2 Solution = ', find_seat( boarding_passes ) )

if __name__ == '__main__':
    exit( main() )
