import pytest
import re

def split_policies( policies ):
    delimiters = '-| |: '
    return [ re.split(delimiters, item) for item in policies] 

def count_valid( policies ):
    policies = split_policies( policies )
    valid = 0
    for policy in policies:
        limits = set( range( int(policy[0]), int(policy[1])+1 ) )
        count  = policy[3].count( policy[2] )
        if count in limits:
            valid += 1
    return valid

def recount_valid( policies ):
    policies = split_policies( policies )
    valid = 0
    for policy in policies:
        positions = [ int(item)-1 for item in policy[:2] ]
        flag1 = policy[3][positions[0]] == policy[2] 
        flag2 = policy[3][positions[1]] == policy[2]
        if flag1 ^ flag2:
            valid += 1
    return valid

@pytest.mark.parametrize('test_input,expected',[ (['1-3 a: abcde',
                                                   '1-3 b: cdefg',
                                                   '2-9 c: ccccccccc'
                                                   ], 2) ] )
def test_part1( test_input, expected ):
    assert count_valid( test_input ) == expected

@pytest.mark.parametrize('test_input,expected',[ (['1-3 a: abcde',
                                                    '1-3 b: cdefg',
                                                    '2-9 c: ccccccccc'
                                                   ], 1) ] )
def test_part2( test_input, expected ):
    assert recount_valid( test_input ) == expected

def main():
    with open('2.in','r') as input_file:
        policies = input_file.read().splitlines()
    print('Part 1 Solution = ',   count_valid( policies ))
    print('Part 2 Solution = ', recount_valid( policies ))

if __name__ == '__main__':
    exit( main() )
