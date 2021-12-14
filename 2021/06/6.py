import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [ int(i) for i in input_file.read().split(',') ]

def count_lanternfish( ages, days ):
    for day in range(1,days+1):
        ages = [ age-1 for age in ages]
        num_reproducing_fish = len( [ age for age in ages if age < 0 ] )
        ages = [ 6 if age < 0 else age for age in ages ] + [8]*num_reproducing_fish
    return len( ages )

def count_lanternfish_efficient( ages, days ):
    fish_per_age = [ ages.count(age) for age in range(9) ]
    for day in range(days):
        num_reproducing_fish = fish_per_age.pop(0)
        fish_per_age[6] += num_reproducing_fish
        fish_per_age.append( num_reproducing_fish )
    return sum( fish_per_age ) 

@pytest.mark.parametrize( 'test_input,expected', [ ('6.example', 5934) ] )
def test_part1( test_input, expected ):
    assert count_lanternfish( get_input( test_input ), days=80 ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('6.example', 26984457539) ] )
def test_part2( test_input, expected ):
    assert count_lanternfish_efficient( get_input( test_input ), days=256 ) == expected

def main():
    print('Part 1 Solution = ', count_lanternfish( get_input('6.in'), days=80 ))
    print('Part 2 Solution = ', count_lanternfish_efficient( get_input('6.in'), days=256 ))

if __name__ == '__main__':
    main()
