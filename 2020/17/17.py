import pytest
from copy import deepcopy

def get_inputs( filename ):
    """
    Each input file has a grid of initial states. 
    This function returns a list of lists of each entry of each row of the grid
    """
    with open( filename, 'r' ) as input_file:
        return [ [entry for entry in row] for row in input_file.read().splitlines() ]

def print_states( title,grid ):
    """
    For debugging.
    This function prints the states in the format of the input file. 
    """
    print(title)
    for row in grid:
        print(''.join(row))

def simulate_cycles( grid, n_cycles=6, part2=False ):
    """
    Simulate the cycles on the given 2D slice of the initial states based on the given rules. 
    The sphere of influence of a cube includes cubes inside a radius of 3 in each dimension.
    Update the active cubes for n_cycles and count the number of active cubes at the end.
    
    NOTE: Part 1: 3-dimensional grid (assume a 3D slice at dim4=0)
          Part 2: 4-dimensional grid
        
        *** Improved solution partly inspired by user: jonathanpaulson *** 
    """
    active = set()
    """
    Step 1:
    Create a set of tuples which indicate the coordinates of the initially active cubes
    """
    for n_row, row in enumerate(grid):
        for n_col, cube in enumerate(row):
            if cube == '#':
                active.add( (n_row, n_col, 0, 0) )
    """
    Step 2:
    Repeat the following steps for n_cycles:
        2.1. Obtain the neighbors of the currently active cubes
    """
    for _ in range( n_cycles ):
        neighbors   = set()
        new_active  = set()
        for ( dim1, dim2, dim3, dim4 ) in active:
            for d1 in [-1,0,1]:
                for d2 in [-1,0,1]:
                    for d3 in [-1,0,1]:
                        for d4 in [-1,0,1]:
                            if part2 or dim4+d4==0: # for part1: active cubes are only from 3D slice where dim4=0
                                neighbors.add( (dim1+d1, dim2+d2, dim3+d3, dim4+d4) )
        """
        2.2. For the found neighbors of the active cubes, check if the neighbors are also active.
             For each cube in neighbors, count the number of active cubes surrounding it. 
        2.3. For each cube in neighbors that is also active, follow the given rules and 
             update its status based on the count of active_neighbors. 
             
             Rules:
                - If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. 
                  Otherwise, the cube becomes inactive.
                - If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. 
                  Otherwise, the cube remains inactive.
            
            Instead of removing inactive cubes from the set of previously active cubes, a new active cubes set is used.
        """
        for ( dim1, dim2, dim3, dim4 ) in neighbors:
            active_neighbors = 0
            for d1 in [-1,0,1]:
                for d2 in [-1,0,1]:
                    for d3 in [-1,0,1]:
                        for d4 in [-1,0,1]:
                            if d1==0 and d2==0 and d3==0 and d4==0: 
                                continue
                            if ( dim1+d1, dim2+d2, dim3+d3, dim4+d4 ) in active:
                                active_neighbors += 1
            if ( dim1, dim2, dim3, dim4 ) in active and active_neighbors in [2,3]:
                new_active.add( (dim1,dim2,dim3,dim4) )
            elif ( dim1, dim2, dim3, dim4 ) not in active and active_neighbors == 3:
                new_active.add( (dim1,dim2,dim3,dim4) )
        active = new_active
    return len(new_active)

@pytest.mark.parametrize( 'test_input, expected', [ ('17.example', 112) ] )
def test_part1( test_input, expected ):
        assert simulate_cycles( get_inputs(test_input), n_cycles=6 ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('17.example', 848) ] )
def test_part1( test_input, expected ):
        assert simulate_cycles( get_inputs(test_input), n_cycles=6, part2=True ) == expected

def main():
    print('Part 1 Solution = ', simulate_cycles( get_inputs( '17.in'), n_cycles=6 ) ) 
    print('Part 2 Solution = ', simulate_cycles( get_inputs( '17.in'), n_cycles=6, part2=True ) ) 

if __name__ == '__main__':
    exit(main())
