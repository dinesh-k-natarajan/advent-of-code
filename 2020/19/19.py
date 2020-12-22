import pytest
import re
from collections import defaultdict
from lark import Lark, LarkError

def get_inputs( filename ):
    """
    The input file contains rules and messages separated by a blank line.
    """
    with open( filename, 'r') as input_file:
        raw_data = input_file.read().split('\n\n')
    rules = raw_data[0].splitlines()
    messages = raw_data[1].splitlines()
    return rules, messages

def count_valid( rules, messages, part2=False):
    """
    Task:
    This function counts the number of messages that completely match a specific rule
    
    Parsing using Lark:
    -------------------
    Setup:
    Using the Lark parser from the lark package, a given message can be checked against
    the known grammar. To comply with the syntax of the Lark parser, the rule numbers are
    prefixed with a string, here: 'rule_'. The grammar is built as a string with each rule
    in a new line.

    Parsing:
    The parser is initialized with the grammar and the starting rule of the grammar.
    Using the parse() method, a message is parsed into a tree structure based on the grammar.
    In the case LarkError is raised, the message is deemed invalid. 

    *** References: lark-parser python documentation - https://github.com/lark-parser/lark ,
                    user: dionyziz ***

    For Part 2:
    -----------
    The rules 8 and 11 are replaced manually in Part 2. No other changes to Part 1.
    """
    grammar = []
    for rule in rules:
        if part2 and rule == '8: 42':
            rule = '8: 42 | 42 8'
        if part2 and rule == '11: 42 31':
            rule = '11: 42 31 | 42 11 31'
        rule = re.sub( r"(\d+)", r"rule_\1", rule )
        grammar.append( rule )
    grammar = '\n'.join( grammar )
    lark_parser = Lark( grammar, start='rule_0' )
    valid = 0
    for message in messages:
        try:
            parse_tree = lark_parser.parse( message )
            valid += 1
        except LarkError:
            pass
    return valid

@pytest.mark.parametrize( 'test_input, expected', [ ('19.example1',2), ('19.example2',3) ] )
def test_part1( test_input, expected ):
    assert count_valid( *get_inputs( test_input ) )

@pytest.mark.parametrize( 'test_input, expected', [ ('19.example2',12) ] )
def test_part2( test_input, expected ):
    assert count_valid( *get_inputs( test_input ), part2=True )

def main():
    print('Part 1 Solution = ', count_valid( *get_inputs('19.in') ) )
    print('Part 2 Solution = ', count_valid( *get_inputs('19.in'), part2=True ) )

if __name__ == '__main__':
    exit( main() )
