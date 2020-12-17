import pytest
import re
from collections import defaultdict
from copy import deepcopy

def get_inputs( filename ):
    with open( filename, 'r' ) as input_file:
        raw_data = [ item.splitlines() for item in input_file.read().split('\n\n') ]
    # Dictionary of sets describing the rules to be satisfied by the entries in the tickets
    rules = defaultdict(set)
    for rule in raw_data[0]:
        field, range1, range2 = re.split( ': | or ', rule )
        range1 = [ int(item) for item in range1.split('-') ]
        range1[-1] += 1
        range2 = [ int(item) for item in range2.split('-') ]
        range2[-1] += 1
        rules[ field ] = set( range(*range1) ) | set ( range(*range2) )
    # List of entries in my ticket
    my_ticket = [ int(entry) for entry in raw_data[1][-1].split(',') ]
    # List of lists for the nearby tickets and their corresponding entries
    nearby_tickets = [ [int(entry) for entry in ticket.split(',')] for ticket in raw_data[2][1:] ]
    return [ rules, my_ticket, nearby_tickets ]

def check_invalid( rules, _ , nearby_tickets, part2=False ):
    """
    From the given rules, find the invalid entries in the nearby tickets. 
    The entries in the tickets should be in the set of possible entries given in the rules dictionary. 
    This function returns the sum of the invalid entries. 
    """
    invalid = []
    for ticket in nearby_tickets:
        entries_rules      = list( rules.values() ) 
        admissible_entries = entries_rules[0].union( *entries_rules[1:] ) 
        invalid.append( [ entry for entry in ticket if entry not in admissible_entries ] ) 
    if not part2:
        return sum( [ subitem for item in invalid for subitem in item ] )
    else:
        return invalid

def decode_fields( rules, my_ticket, nearby_tickets ):
    """
    Find invalid tickets and remove them. From the valid tickets and the rules,
    decode the order of the fields in the ticket. The order is consistent through
    all the tickets. 

    Once the order is found, find the values for the 6 fields that begin with 'departure'.
    This function returns the product of those values. 
    """
    """
    Step 1:
    Get invalid tickets and remove them
    """
    invalid = check_invalid( rules, None, nearby_tickets, part2=True )
    valid_tickets = deepcopy( nearby_tickets )
    for ticket_num, invalid_entry in enumerate(invalid):
        if invalid_entry != []:
            valid_tickets.remove( nearby_tickets[ticket_num] )
    """
    Step 2:
    Match the entries in valid tickets to the fields based on the field rules
    Create a dict with fields as keys with values as a list with all possible columns
    """
    possible_columns = defaultdict( list )
    for field in rules: 
        possible_columns[field] = list( range( len(my_ticket) ) )
    """
    Step 3:
    For each column, iterate through each rule and check if the entries satisfy the rule
    If the column and rule combination that leads to a violation, then remove the column
    from the possible_columns value for that rule. 
    This gives: for each field, the admissible columns based on the valid tickets 
    """ 
    for column in range( len(my_ticket) ):
        for rule_num, rule in enumerate( rules.values() ):
            if not all( [ ticket[column] in rule for ticket in valid_tickets ] ):
                possible_columns[ list( possible_columns.keys() )[rule_num] ].remove( column )
    """
    Step 4:
    Given the admissible columns for each field, if only one column is admissible it is
    assigned as the unique column for that field and removed from the list of admissible
    columns list of the other fields. Repeating this to all fields, finally results in
    the correct assignment of fields and columns in the dict `fields_order`
    """
    fields_order = defaultdict( list )
    while len(fields_order) < len(possible_columns):
        for field in possible_columns.keys():
            if len( possible_columns[ field ] ) == 1:
                unique_column = possible_columns[ field ][0]
                fields_order[field] = unique_column 
                for field_ in possible_columns.keys():
                    possible_columns[field_] = [ column for column in possible_columns[field_] 
                                                 if column != unique_column ] 
    """
    Step 5:
    Find the product of the values corresponding to the fields starting with 'departure'
    """
    product = 1
    for field in fields_order.keys():
        if field.startswith('departure'):
            product *= my_ticket[ fields_order[ field ] ]
    return product

@pytest.mark.parametrize('test_input,expected',[ ( '16.example1', 71) ] )
def test_part1( test_input, expected ):
    assert check_invalid( *get_inputs( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', check_invalid( *get_inputs( '16.in' ) ) )
    print('Part 2 Solution = ', decode_fields( *get_inputs( '16.in' ) ) )

if __name__ == '__main__':
    exit( main() )
