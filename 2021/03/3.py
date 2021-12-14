import pytest
from statistics import multimode

def get_input( filename ):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [ [int(i) for i in line] for line in lines ]

def bin_to_dec( binary ):
    decimal = 0
    for i in range( len( binary ) ):
        decimal += 2**i * binary[-(i+1)]
    return decimal

def compute_power_consumption( report ):
    gamma_bin = []
    epsilon_bin = []
    for column_num in range( len(report[0]) ):
        column = [ line[column_num] for line in report ]
        gamma_bin.append( max( set(column), key=column.count ) )
        epsilon_bin.append( min( set(column), key=column.count ) )
    assert len(gamma_bin) == len(epsilon_bin) == len(report[0])
    return bin_to_dec( gamma_bin ) * bin_to_dec( epsilon_bin )

def O2_rating( report ):
    while len( report ) > 1:
        for column_num in range( len(report[0]) ):
            column = [ line[column_num] for line in report ]
            most_common = max( multimode( column ) )
            report = [ number for number in report if number[column_num]==most_common ]
    assert len(report) == 1
    return bin_to_dec( report[0] )

def CO2_rating( report ):
    while len( report ) > 1:
        for column_num in range( len(report[0]) ):
            column = [ line[column_num] for line in report ]
            least_column = min( set(column), key=column.count )
            report = [ number for number in report if number[column_num]==least_column ]
    assert len(report) == 1
    return bin_to_dec( report[0] )

def compute_rating( report ):
    return O2_rating( report ) * CO2_rating( report )

@pytest.mark.parametrize( 'test_input,expected', [ ('3.example', 198) ] )
def test_part1( test_input, expected ):
    assert compute_power_consumption( get_input( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('3.example', 230) ] )
def test_part2( test_input, expected ):
    assert compute_rating( get_input( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', compute_power_consumption( get_input('3.in') ))
    print('Part 2 Solution = ', compute_rating( get_input('3.in') ))

if __name__ == '__main__':
    main()
