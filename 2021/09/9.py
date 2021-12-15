import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        lines = input_file.read().splitlines()
        return [ [ int(num) for num in line ] for line in lines ]

def compute_risk( heightmap ):
    low_points = []
    valid_row = list( range( len( heightmap  ) ) )
    valid_col = list( range( len( heightmap[0] ) ) )
    for row in valid_row:
        for col in valid_col:
            neighbors = []
            neighbor_coords = [  [row-1,col],
                                 [row, col+1],
                                 [row+1, col],
                                 [row, col-1]
                               ]
            for coord in neighbor_coords:
                if coord[0] in valid_row and coord[1] in valid_col:
                    neighbors.append( heightmap[coord[0]][coord[1]] )
            if all( heightmap[row][col] < neighbor for neighbor in neighbors ):
                low_points.append( heightmap[row][col] )
    return sum( 1+point for point in low_points )

def compute_basins( heightmap ):
    
    return None

@pytest.mark.parametrize( 'test_input,expected', [ ('9.example', 15 ) ] )
def test_part1( test_input, expected ):
    assert compute_risk( get_input( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('9.example', 1134 ) ] )
def test_part2( test_input, expected ):
    assert compute_basins( get_input( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', compute_risk( get_input('9.in') ) )
    print('Part 2 Solution = ', compute_basins( get_input('9.in') ) )

if __name__ == '__main__':
    main()
