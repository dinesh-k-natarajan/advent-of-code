import pytest
import re
from collections import defaultdict

def get_inputs( filename):
    """
    Given sentences in the file, split each sentence using delimiters into parent, children, amount of children
    Create dicts that describe the parents of any color, and the children and corresponding amount of any color
    parents_of  = Dict where keys are colors, values are set( parents of color)
        e.g.: { 'bright white': {'dark orange', 'light red'}, 
                'muted yellow': {'dark orange', 'light red'}, 
                'shiny gold': {'muted yellow', 'bright white'}, .... }
    children_of = Dict where keys are colors, values are lists of tuples ( amount, children of color)
        e.g.: { 'light red': [(1, 'bright white'), (2, 'muted yellow')], 
                'dark orange': [(3, 'bright white'), (4, 'muted yellow')], 
                'bright white': [(1, 'shiny gold')], .... }
    """
    with open( filename, 'r') as input_file:
        lines = input_file.read().splitlines()
    parents_of  = defaultdict(set)
    children_of = defaultdict(list)
    for line in lines:
        contents = [ item for item in re.split( 'contain | bags, | bag, | bags.| bag.', line) if item != '' ]
        bag      = contents[0]
        for inner_bag in contents[1:]:
            if inner_bag[:2] != 'no':
                inner_bag_count = int( inner_bag[:2] )
                inner_bag_color = inner_bag[2:]
                parents_of[inner_bag_color].add( bag )
                children_of[bag].append( (inner_bag_count, inner_bag_color))
    return [parents_of, children_of]

def bags_with_gold( parents_of, _ ):
    """
    Starting from leaf = 'gold', find recursively its parents upto the root and add them to a set
    Number of bags that could contain gold = length of the set
    """
    contains_gold = set()
    def find_roots( bag ):
        for outer_bag in parents_of[ bag ]:
            contains_gold.add( outer_bag )
            find_roots( outer_bag )
    find_roots('shiny gold')
    return len(contains_gold)

def contents_of_gold( _ , children_of ):
    """
    Starting from the root = 'gold', find recursively it's total amount of children
    """
    def count_contents( bag ):
        contents = 0
        for amount, inner_bag in children_of[ bag ]:
            contents += amount + amount * count_contents( inner_bag )
        return contents
    return count_contents( 'shiny gold' )

@pytest.mark.parametrize( 'test_input, expected', [ ('7.example1', 4) ] )
def test_part1( test_input, expected ):
    assert bags_with_gold( *get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('7.example1', 32), ('7.example2', 126) ] )
def test_part2( test_input, expected ):
    assert contents_of_gold( *get_inputs(test_input) ) == expected

def main():
    print('Part 1 Solution = ', bags_with_gold(   *get_inputs('7.in') ) )
    print('Part 2 Solution = ', contents_of_gold( *get_inputs('7.in') ) )

if __name__ == '__main__':
    exit( main())
