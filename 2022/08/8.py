import time
import pytest

def parse_input( filename ):
    with open(filename,'r') as input_file:
        return [[int(tree) for tree in line] for line in input_file.read().splitlines()]

def count_visible_trees( trees ):
    grid_dims = [len(trees),len(trees[0])]
    # trees on grid boundary are visible from outside
    n_boundary = 2*(grid_dims[0]+grid_dims[1]-2)
    # internal trees that are shorter than others are visible from the outside
    int_visible = []
    for i in range(1,grid_dims[0]-1):
        for j in range(1,grid_dims[1]-1):
            tree = trees[i][j]
            # is the tree shorter than all other trees from itself to the edge?
            top_flag    = all(t < tree for t in [row[j] for row in trees[:i]])
            bottom_flag = all(t < tree for t in [row[j] for row in trees[i+1:]])
            left_flag   = all(t < tree for t in trees[i][:j])
            right_flag  = all(t < tree for t in trees[i][j+1:])
            # is it visible from any of the 4 directions?
            if top_flag | bottom_flag | left_flag | right_flag:
                int_visible.append(tree)
    return n_boundary+len(int_visible)

def count_unblocked( tree, view ):
    # find number of unblocked trees from the tree in a specific view
    if all(t<tree for t in view): # if no trees are >= tree
        n_unblocked = len(view)
    else:
        # from the tree, you can see upto the first tallest tree
        taller_trees = [view.index(t) for t in view if t>=tree]
        n_unblocked = taller_trees[0]+1 # start index from 1
    return n_unblocked

def compute_max_score( trees ):
    grid_dims = [len(trees),len(trees[0])]
    scenic_scores = []
    # ignoring trees on boundary (since their score in atleast one direction = 0)
    for i in range(1,grid_dims[0]-1):
        for j in range(1,grid_dims[1]-1):
            tree = trees[i][j]
            # collect list of trees in each direction from tree, with the tree as origin
            top_trees    = [row[j] for row in trees[:i]][::-1] # reversed, from origin
            bottom_trees = [row[j] for row in trees[i+1:]]
            left_trees   = trees[i][:j][::-1] # reversed, from origin
            right_trees  = trees[i][j+1:]
            score = 1
            for view in [top_trees,bottom_trees,left_trees,right_trees]:
                score *= count_unblocked(tree,view)
            scenic_scores.append(score)
    return max(scenic_scores)

@pytest.mark.parametrize( 'test_input,expected', [ ('8.example', 21) ] )
def test_part1( test_input, expected ):
    assert count_visible_trees( parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('8.example', 8) ] )
def test_part2( test_input, expected ):
    assert compute_max_score( parse_input(test_input) ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', count_visible_trees( parse_input('8.in') ))
    print('Part 2 Solution = ', compute_max_score(   parse_input('8.in') ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()