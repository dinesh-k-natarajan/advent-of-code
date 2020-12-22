import pytest
from collections import defaultdict
import re

def process_input( filename ):
    """ 
    The input file contains groups of lines describing each passport.
    Each passport contains a field and corresponding value.
    This function returns a list of all passports where each passport
    is a dictionary of { field:value }
    """
    with open(filename,'r') as input_file:
        raw_input = input_file.read().split('\n\n')
    list_of_dicts = []
    for entry in raw_input:
        pairs = re.split(' |\n', entry)
        entry_dict = defaultdict( lambda: None )
        for pair in pairs:
            if len(pair) > 0:
                [key, value] = pair.split(':')
                entry_dict[key] = value
        list_of_dicts.append( entry_dict )
    return list_of_dicts

def count_valid( data, part2=False ):
    """
    For Part 1:
    -----------
    The valid passports are those that contain the following required fields:
    byr, iyr, eyr, hgt, hcl, ecl, pid, cid. The field 'cid' is optional.
    
    For Part 2:
    -----------
    Along with the rules for the presence of required fields from Part 1, 
    additional rules are now considered for the values of those fields. 
    These rules are defined in the `valid_values` dictionary below.

    This function returns the number of valid passports defined by the correponding
    rules.
    """
    required_fields = {'byr','iyr','eyr','hgt','hcl','ecl','pid','cid'}
    allowed_missing = {'cid'}
    valid_values    = { 'byr':[4, 1920, 2002], 
                        'iyr':[4, 2010, 2020],
                        'eyr':[4, 2020, 2030],
                        'hgt':[['cm', 150, 193], ['in', 59, 76]], 
                        'hcl':['#',6, {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}],
                        'ecl':{'amb','blu', 'brn','gry','grn','hzl','oth'},
                        'pid': 9
                       }
    count = 0
    for num, entry in enumerate(data):
        if len(entry) > 0:
            entry_fields = set( entry.keys() )
            flag1 = required_fields & entry_fields == required_fields
            flag2 = required_fields - entry_fields == allowed_missing
            flag3 = True
            if part2:
                value_flags = dict()
                # Check years
                for year in ['byr','iyr','eyr']:
                    if entry[year] is not None:
                        value_flags[year] = (   len( entry[year] ) == valid_values[year][0] and 
                                                valid_values[year][1] <= int(entry[year]) <= valid_values[year][2]
                                            )
                # Check height
                if entry['hgt'] is not None:
                    hgt_flag = entry['hgt'][-2:] in { 'cm', 'in' }
                    if hgt_flag and entry['hgt'][-2:] == 'cm':
                        hgt_flag = hgt_flag and 150 <= int(entry['hgt'][:-2]) <= 193
                    elif hgt_flag and entry['hgt'][-2:] == 'in':
                        hgt_flag = hgt_flag and 59 <= int(entry['hgt'][:-2]) <= 76
                    value_flags['hgt'] = hgt_flag 
                # Check hair color
                if entry['hcl'] is not None:
                    value_flags['hcl'] = ( entry['hcl'][0] == '#' and
                                            len( entry['hcl'][1:] ) == 6 and
                                            set( entry['hcl'][1:] ).issubset( valid_values['hcl'][2] )
                                         )
                # Check eye color
                if entry['ecl'] is not None:
                    value_flags['ecl'] = entry['ecl'] in valid_values['ecl'] 
                # Check passport id
                if entry['pid'] is not None:
                    value_flags['pid'] = len( entry['pid'] ) == 9 
                # AND over value_flags
                flag3 = False not in value_flags.values()
            if (flag1 or flag2) and flag3:
                count += 1          
    return count

@pytest.mark.parametrize('test_input,expected',[ ('4.example1', 2) ] )
def test_part1( test_input, expected ):
    test_data = process_input( test_input )
    assert count_valid( test_data ) == expected

@pytest.mark.parametrize('test_input,expected',[ ('4.example2', 4) ] )
def test_part2( test_input, expected ):
    test_data = process_input( test_input )
    assert count_valid( test_data, part2=True ) == expected

def main():
    data = process_input( '4.in' )
    print('Part 1 Solution = ', count_valid(data) )
    print('Part 2 Solution = ', count_valid(data, part2=True) )

if __name__=='__main__':
    exit(main())
