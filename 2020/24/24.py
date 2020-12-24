import pytest 
import re

def get_inputs( filename ):
    """
    Each line in the input file contains directions to a tile
    starting from the origin.
    This function returns a list of lists with directions to each tile.
    """
    with open( filename, 'r' ) as input_file:
        raw_data = input_file.read().splitlines()
    directions = 'e|se|sw|w|nw|ne'
    tiles = []
    for line in raw_data:
        tile = re.findall( directions, line )
        tiles.append( tile )
    return tiles

def get_coordinates( x,y,direction ):
    """
    Given (x,y) coordinates and direction, this function returns the 
    coordinates of the next tile
    
    The strange coordinate system used to represent hexagonal grids here
    is called the 'Axial Coordinate System'. 
    
    Reference: https://www.redblobgames.com/grids/hexagons/
    """
    coordinate_transform = { 
                            'e' : ( x+1, y   ), 
                            'se': ( x  , y+1 ), 
                            'sw': ( x-1, y+1 ), 
                            'w' : ( x-1, y   ), 
                            'nw': ( x  , y-1 ), 
                            'ne': ( x+1, y-1 ), 
                            }
    return coordinate_transform[ direction ]

def flip_tiles( tiles ):
    """
    Initially all tiles are white. Every time, a tile is visited based on the
    directions, it is flipped (to black, or to white again).
    
    The directions are represented in (x,y) coordinates starting from reference
    tile at (0,0). 

    Based on the given directions to each tile starting from the reference tile,
    the coordinates of the tile is found and added to the set of black tiles. If
    the tile is already a black tile, it is flipped and thus removed from the set.
    
    This function returns the set of black tiles.
    """
    black_tiles = set()
    for directions_to_tile in tiles:
        x,y = (0,0)
        for direction in directions_to_tile:
            x,y = get_coordinates( x,y, direction )
        found_tile = (x,y)
        if found_tile not in black_tiles:
            black_tiles.add( found_tile )
        else:
            black_tiles.remove( found_tile )
    return black_tiles

def get_adjacent( coords ):
    """
    Given coordinates of a specific tile, this function returns the coordinates
    of the six adjacent tiles as a set.
    """
    x,y = coords
    adjacent = set()
    for direction in ['e','se','sw','w','nw','ne']:
        adjacent.add( get_coordinates( x,y,direction) )
    return adjacent

def simulate_flipping( tiles, days=100 ):
    """
    The black tiles from the initial configuration are first obtained using
    Part 1.

    For Part 2:
    -----------
    The tiles are to be flipped for 100 days based on the following rules:
        
        - Any black tile with 0 or more than 2 black tiles immediately adjacent 
          to it is flipped to white.
        - Any white tile with exactly 2 black tiles immediately adjacent
          to it is flipped to black.
    
    First, all the new tiles to be flipped are located and the found tiles are 
    flipped simultaneously. This is repeated for given number of days.

    This function returns the black_tiles at the final day.
    
    Notes on the tricky concept that cost me time:
    ----------------------------------------------
        Update all_tiles daily:
        -----------------------
        Given a black tile, its adjacent tiles are to be found. Every adjacent tile 
        and its black tile belongs to the set of all_tiles.
    
        Failed attempt:
        ---------------
        Using only the all_tiles found from the initial configuration (flip_tables)
        resulted in very low counts of black_titles. Since the set of black_tiles is
        expected to grow as days progress, the set of all_tiles has to updated daily.

    """
    black_tiles = flip_tiles( tiles )
    for _ in range( 100 ):
        all_tiles  = set()
        all_tiles |= black_tiles
        all_tiles |= set( [ adjacent for black in black_tiles for adjacent in get_adjacent(black) ] ) 
        new_black  = set()
        for tile in all_tiles:
            adj_and_black = len( get_adjacent(tile) & black_tiles ) 
            if tile in black_tiles and adj_and_black in [1,2]:
                new_black.add( tile )
            elif tile not in black_tiles and adj_and_black == 2:
                new_black.add( tile )
        black_tiles = new_black
    return black_tiles

def count_tiles( tiles, part2=False ):
    """
    This function returns the number of black tiles
    """
    if not part2:
        return len( flip_tiles( tiles ) )
    else:
        return len( simulate_flipping( tiles ) )

@pytest.mark.parametrize( 'test_input, expected', [ ( '24.example', 10 ) ] )
def test_part1( test_input, expected ):
    assert count_tiles( get_inputs( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ( '24.example', 2208 ) ] )
def test_part2( test_input, expected ):
    assert count_tiles( get_inputs( test_input ), part2=True ) == expected

def main():
    print('Part 1 Solution = ', count_tiles( get_inputs( '24.in' ) ) )
    print('Part 2 Solution = ', count_tiles( get_inputs( '24.in' ), part2=True ) )

if __name__ == '__main__':
    main()
