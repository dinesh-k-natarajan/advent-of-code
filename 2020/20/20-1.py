import pytest
import re
import math
import numpy as np

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

def get_edge( tile, edge ):
    """
    This function returns the specific edge of the given tile.
    """
    if edge == 'top':
        return tile[0,:]
    elif edge == 'bottom':
        return tile[-1,:]
    elif edge == 'left':
        return tile[:,0]
    elif edge == 'right':
        return tile[:,-1]
    else:
        raise ValueError("The arg 'edge' should be top, bottom, left or right!")

def is_match( tile, other_tile, edge ):
    """
    Returns a boolean if the given edge of tile matches the corresponding neighboring 
    edge of other tile.
    """
    if edge == 'top':
        return ( get_edge( tile, edge ) == get_edge( other_tile, 'bottom') ).all()
    elif edge == 'bottom':
        return ( get_edge( tile, edge ) == get_edge( other_tile, 'top'   ) ).all()
    elif edge == 'left':
        return ( get_edge( tile, edge ) == get_edge( other_tile, 'right' ) ).all()
    elif edge == 'right':
        return ( get_edge( tile, edge ) == get_edge( other_tile, 'left'  ) ).all()
    else:
        raise ValueError("The arg 'edge' should be top, bottom, left or right!")

def match_edges( tiles ):
    """
    This function iterates over each tile and tries to find matching edges with all
    possible orientations of the other tiles.

    The number of matching edges are stored in a dictionary with keys as the tile ID.
    This function returns the matching_edges dictionary.
    """
    matching_edges = { tile_id: 0 for tile_id in tiles }
    for current_tile_id, current_tile in tiles.items():
        for other_tile_id, other_tile in tiles.items():
            if current_tile_id != other_tile_id:
                orientations = get_orientations( other_tile_id, other_tile )
                for orientation in orientations:    
                    for edge in ['top','bottom','left','right']:
                        if is_match( current_tile, orientation, edge ):
                            matching_edges[current_tile_id] += 1
    return matching_edges

def find_corners( tiles ):
    """
    The counts of matching edges for each tile with another tile is computed.
    The edges that have exactly 2 matching edges with another tile are the corner
    tiles. The tile_ids of those corners are found and their product is the solution
    to Part 1.
    """
    matching_edges = match_edges( tiles )
    product = 1
    for tile_id in matching_edges:
        if matching_edges[ tile_id ] == 2:
            product *= tile_id
    return product

# pseudo main() function
orientations_cache = dict() 
print('Test 1 Solution = ', find_corners( get_inputs( '20.example' ) ) )
orientations_cache = dict() 
print('Part 1 Solution = ', find_corners( get_inputs( '20.in' ) ) )
