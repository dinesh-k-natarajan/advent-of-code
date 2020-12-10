import pytest

def get_input( file_name ):
    with open( file_name, 'r') as file:
        return file.read().splitlines()

def count_trees( grid, delta_col=3, delta_row=1 ):
    height = len(grid)
    width  = len(grid[0])
    count = 0
    row, col = 0, 0
    while row < height:
        count += grid[row][col] == '#'
        row += delta_row
        col = (col+delta_col) % width
    return count

def get_product( grid, slopes):
    product = 1
    for slope in slopes:
        product *= count_trees( grid, *slope)
    return product

@pytest.mark.parametrize('test_input,expected',[ ('3.example', 7) ] )
def test_part1( test_input, expected ):
    test_grid = get_input( test_input )
    assert count_trees( test_grid ) == expected

@pytest.mark.parametrize('test_input,slopes, expected',[ ('3.example',
                                                         [[1,1],[3,1],[5,1],[7,1],[1,2]], 336) ] )
def test_part2( test_input, slopes, expected ):
    test_grid = get_input( test_input )
    assert  get_product( test_grid, slopes ) == expected

def main():
   grid = get_input( '3.in' )
   print('Part 1 Solution = ', count_trees(grid))
   slopes = [[1,1],[3,1],[5,1],[7,1],[1,2]]
   print('Part 2 Solution = ', get_product(grid, slopes))

if __name__ == '__main__':
    exit( main() )
