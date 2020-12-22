import pytest
import re

def split_policies( policies ):
    """
    This function splits each line of policies using regular expressions
    and the specific delimiters. 
    """
    delimiters = '-| |: '
    return [ re.split(delimiters, item) for item in policies] 

def count_valid( policies ):
    """
    This function counts the number of valid passwords based on the policies.

    e.g.: In the policy, '1-3 a: abcde', if the password 'abcde' contains
    'a' atleast '1' time(s) and atmost '3' times, then it is valid.
    """
    policies = split_policies( policies )
    valid = 0
    for policy in policies:
        limits = set( range( int(policy[0]), int(policy[1])+1 ) )
        count  = policy[3].count( policy[2] )
        if count in limits:
            valid += 1
    return valid

def recount_valid( policies ):
    """
    This function recounts the number of valid passwords based on the policies
    and the new rule introduced in Part 2.
    
    Rule change: The numbers '1-3' represent the positions of the password 
    of which exactly one (XOR logic) must contain the character 'a'

    Test cases:
        1-3 a: abcde is valid: position 1 contains a and position 3 does not.
        1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
        2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
    """
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
