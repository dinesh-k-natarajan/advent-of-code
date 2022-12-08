import time
import pytest

def parse_input( filename ):
    with open(filename,'r') as input_file:
        return [[int(tree) for tree in line] for line in input_file.read().splitlines()]

def compute_1( trees ):
    grid_dims = [len(trees),len(trees[0])]
    ext_visible = []
    int_visible = []
    # trees on grid boundary are visible from outside
    for i in range(grid_dims[0]):
        if i in [0, grid_dims[0]-1]:
            ext_visible += trees[i]
        else:
            ext_visible += [trees[i][0], trees[i][grid_dims[1]-1]]
    # internal trees that are shorter than others are visible from the outside
    for i in range(1,grid_dims[0]-1):
        for j in range(1,grid_dims[1]-1):
            tree = trees[i][j]
            # is the tree shorter than all other trees from itself to the edge?
            top = all(t < tree for t in [row[j] for row in trees[:i]])
            bottom = all(t < tree for t in [row[j] for row in trees[i+1:]])
            left = all(t < tree for t in trees[i][:j])
            right = all(t < tree for t in trees[i][j+1:])
            # is it visible from any of the 4 directions?
            if top | bottom | left | right:
                int_visible.append(tree)
    return len(ext_visible+int_visible)

def get_unblocked_trees(tree,view):
    # find number of unblocked trees from the tree in a specific view
    if all(t<tree for t in view): # if no trees are >= tree
        unblocked_trees = len(view)
    else:
        # from the tree, you can see upto the first tallest tree
        taller_trees = [view.index(t) for t in view if t>=tree]
        unblocked_trees = taller_trees[0]+1 # start index from 1
    return unblocked_trees

def compute_2( trees ):
    grid_dims = [len(trees),len(trees[0])]
    scenic_scores = []
    # ignoring trees on boundary (since their score in atleast one direction = 0)
    for i in range(1,grid_dims[0]-1):
        for j in range(1,grid_dims[1]-1):
            tree = trees[i][j]
            top = [row[j] for row in trees[:i]][::-1] # order reverseed, from tree POV
            bottom = [row[j] for row in trees[i+1:]]
            left = trees[i][:j][::-1] # order reversed, from tree POV
            right = trees[i][j+1:]
            score = 1
            for view in [top,bottom,left,right]:
                score *= get_unblocked_trees(tree,view)
            scenic_scores.append(score)
    return max(scenic_scores)

@pytest.mark.parametrize( 'test_input,expected', [ ('8.example', 21) ] )
def test_part1( test_input, expected ):
    assert compute_1( parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('8.example', 8) ] )
def test_part2( test_input, expected ):
    assert compute_2( parse_input(test_input) ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', compute_1( parse_input('8.in') ))
    print('Part 2 Solution = ', compute_2( parse_input('8.in') ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()