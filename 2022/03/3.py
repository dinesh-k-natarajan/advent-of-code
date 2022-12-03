import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [line for line in input_file.read().splitlines()]

HIERARCHY = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def compute_item_priorities( inputs ):
    rucksacks = [[set(line[:len(line)//2]), set(line[len(line)//2:])] for line in inputs]
    shared_items = [list(compartments[0].intersection(compartments[1])) for compartments in rucksacks]
    priorities = [[(HIERARCHY.index(item)+1) for item in rucksack] for rucksack in shared_items]
    return sum([priority for rucksack in priorities for priority in rucksack])

def compute_badge_priorities( inputs ): 
    groups_of_3 = [inputs[i*3:(i+1)*3] for i in range((len(inputs)+3-1)//3)]
    shared_items = [list((set(group[0]).intersection(set(group[1]))).intersection(set(group[2]))) for group in groups_of_3]
    priorities = [[(HIERARCHY.index(item)+1) for item in rucksack] for rucksack in shared_items]
    return sum([priority for rucksack in priorities for priority in rucksack])

@pytest.mark.parametrize( 'test_input,expected', [ ('3.example', 157) ] )
def test_part1( test_input, expected ):
    assert compute_item_priorities( get_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('3.example', 70) ] )
def test_part2( test_input, expected ):
    assert compute_badge_priorities( get_input(test_input) ) == expected

def main():
    print('Part 1 Solution = ', compute_item_priorities( get_input('3.in') ))
    print('Part 2 Solution = ', compute_badge_priorities( get_input('3.in') ))

if __name__ == '__main__':
    main()
