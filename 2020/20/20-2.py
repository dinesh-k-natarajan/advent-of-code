import re
import numpy as np
from scipy import signal

def get_inputs( filename ):
    """
    The input file contains many tiles prefixed with a title line.
    This function returns a dictionary of (tile ID, np.array(tile) ).
    """
    with open( filename, 'r' ) as input_file:
        raw_data = input_file.read().split('\n\n')
    tiles = dict()
    for entry in raw_data:
        entry   = entry.splitlines()
        tile_id = int( re.findall( '\d+', entry[0] )[0] )
        tile    = [ re.sub( '\.', '0', line ) for line in entry[1:] ]
        tile    = [ re.sub( '#',  '1', line ) for line in tile ]
        tile    = [ [ int(item) for item in line ] for line in tile ]
        tiles[tile_id] = np.array( tile )
    return tiles

def get_orientations( tile_id, tile ):
    """
    For a given tile and tile ID, all possible orientations of the tile
    are found by flipping and rotating the tile. All orientations are 
    stored in a dictionary, which is memoized [1].
    
    Each tile is rotated 4 times ( degrees = 0, 90, 180, 270 )
    Then the tile is flipped and rotated 4 times (degrees = 0, 90, 180, 270 )
    These are the 8 unique possible orientations for a given tile. 
    #ididthemath
    
    This function returns the dict of different orientations of the tile.

    References:
    -----------
    1. https://www.python-course.eu/python3_memoization.php
    """
    global orientations_cache
    if tile_id in orientations_cache:
        return orientations_cache[ tile_id ]
    else:
        orientations = []
        for times in [0,1,2,3]:
            orientations.append( np.rot90( tile, times ) )
        flipped_tile = np.flipud( tile )
        for times in [0,1,2,3]:
            orientations.append( np.rot90( flipped_tile, times ) )
        orientations_cache[ tile_id ] = orientations
        return orientations

def other_tiles( tiles, tile_id ):
    """
    This function removes the given tile_id from the tiles dict and returns the remaining
    tiles as a dict.
    """
    return { ID: tiles[ ID ] for ID in tiles if ID not in tile_id }

def fit_jigsaw( x, y, grid_size, jigsaw_grid, tiles ):
    """
    This function recursively tries to find the solution to the jigsaw puzzle.
        *** Heavily inspired by reddit user: u/Fuzzy-Age6814 ***
    TODO: Cleanup and improve code readability.
    """
    if len( tiles ) == 0:
        return jigsaw_grid
    for tile_id, tile in tiles.items():
        orientations = get_orientations( tile_id, tile )
        jigsaw_grid[y][x]['tile_id'] = tile_id
        for orientation in orientations:
            fit_x, fit_y = True, True
            if x - 1 >= 0:
                # check if the tile's left edge matches the left tile's right edge
                left_neighbor = jigsaw_grid[y][x-1]['tile'][:,-1]
                if not np.array_equal( left_neighbor, orientation[:,0] ):
                    fit_x = False
            if y - 1 >= 0:
                # check if the tile's top edge matches the top tile's bottom edge
                top_neighbor = jigsaw_grid[y-1][x]['tile'][-1]
                if not np.array_equal( top_neighbor, orientation[0] ):
                    fit_y = False
            if fit_x and fit_y:
                jigsaw_grid[y][x]['tile'] = orientation
                new_x = ( x+1 ) % grid_size
                new_y = y + ( (x+1)//grid_size )
                solved_grid = fit_jigsaw( new_x, new_y, grid_size, jigsaw_grid, other_tiles(tiles, [tile_id]) )
                if solved_grid is not None:
                    return solved_grid
    """
    Apparently, for the final solution to be reached, this return statement should not be reached.
    Works for both the example and the input. 
    """
    return None

def find_corners( tiles ):
    """
    Since my solution in 20-1.py did not find the solved grid, the Part 1 here had to
    be reimplemented using a different approach, so that the entire grid is constructed
    in Part 1 already. 

    For Part 1:
    -----------
    The jigsaw puzzle is solved and the final grid is solved.
    This function returns the product of tile IDs of the four corners of the solved grid.
    
    Notation: 
    ---------
    Following the notation of images in Computer Vision: x - columns, y - rows
    """
    grid_size    = int( np.sqrt( len( tiles ) ) )
    jigsaw_grid  = [ [ dict() for x_dim in range(grid_size) ] for y_dim in range(grid_size) ]
    solved_grid  = fit_jigsaw( 0, 0, grid_size, jigsaw_grid, tiles )
    top_left     = solved_grid[0][0]['tile_id']
    top_right    = solved_grid[0][ grid_size-1 ]['tile_id']
    bottom_left  = solved_grid[ grid_size-1 ][0]['tile_id']
    bottom_right = solved_grid[ grid_size-1 ][ grid_size -1 ]['tile_id']
    return top_left * top_right * bottom_left * bottom_right, solved_grid

def assemble_tiles( solved_grid ):
    """
    This function returns all possible orientations of the assembled final image 
    built from the solved grid of tiles.
    """
    image_rows = []
    for tiles_row in solved_grid:
        image_row = None
        for tile in tiles_row:
            tile['tile'] = tile['tile'][1:-1, 1:-1]
            if image_row is None:
                image_row = tile['tile']
            else:
                image_row = np.concatenate( (image_row, tile['tile']), axis=1 )
        image_rows.append( image_row )
    image = None
    for row in image_rows:
        if image is None:
            image = row
        else:
            image = np.concatenate( (image, row), axis=0 )
    return get_orientations( 'final image', image )

def get_monster( filename ):
    """
    Loads the monster and returns the translated numpy array.
    """
    with open( filename, 'r' ) as monster_file:
        ascii_monster = monster_file.read().splitlines()
    monster = [ re.sub( '\s', '0', line ) for line in ascii_monster ]
    monster = [ re.sub( '#',  '1', line ) for line in monster ]
    monster = [ [ int(item) for item in line ] for line in monster ]
    return np.array( monster )

def find_monsters( solved_grid ):
    """
    For Part 2:
    -----------
    Each tile is now trimmed by removing its borders. The entire image is constructed 
    from the solved grid and its possible orientations are also obtained.
   
    Load the sea monster from '20.monster' and convert # to 1s and blank spaces to 0s.

    The convolution of the image with monster as kernel will help find the monster in
    the image. If the kernel exactly matches with a part of the image, the center pixel
    at that part of the image would have a convoluted value which is equal to the sum
    of the kernel. This pixel would also have the maximum value in the convolution as 
    it was the perfect match for the kernel.
    
    The number of monsters in the image is computed by finding the number of matching 
    pixels in the convolution. Having found the number of monsters, the water roughness
    of the sea is found by summing the 1s in the sea that are not the monster.
    """
    images  = assemble_tiles( solved_grid )
    monster = get_monster( '20.monster' )  
    for image in images:
        convolution = signal.convolve2d( image, monster )
        if np.max( convolution ) == np.sum( monster ):
            num_monster = np.sum( convolution == np.sum( monster ) ) 
    water_roughness = np.sum(image) - num_monster * np.sum(monster)
    return water_roughness

"""
Currently, using the code block below acts as a pesudo main() function.
TODO: Using global variables with my usual code structure of a main() function 
and if __name__ == '__main__' statement.

Lesson learnt:
--------------
Beware of using memoized functions. Fatal bug was introduced when the cache
dictionary was NOT reinitialized with a blank dict! The example and input had
some common tile IDs which combined with the cache from example lead to the bug.
"""
orientations_cache = dict() 
corners, solved_grid = find_corners(  get_inputs( '20.example' ) )
print('Test 1 Solution = ', corners )
print('Test 2 Solution = ', find_monsters( solved_grid ) )
orientations_cache = dict() 
corners, solved_grid = find_corners(  get_inputs( '20.in' ) )
print('Part 1 Solution = ', corners ) 
print('Part 2 Solution = ', find_monsters( solved_grid ) )
