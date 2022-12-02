import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [[int(item) for item in group.split()] for group in input_file.read().split('\n\n')]

def count_max_calories( calories ):
    return max([sum(sublist) for sublist in calories])

def count_top3_calories( calories ):
    return sum(sorted([sum(sublist) for sublist in calories], reverse=True)[:3])
    
@pytest.mark.parametrize( 'test_input,expected', [ ('1.example', 24000) ] )
def test_part1( test_input, expected ):
    assert count_max_calories( get_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('1.example', 45000) ] )
def test_part2( test_input, expected ):
    assert count_top3_calories( get_input(test_input) ) == expected

def main():
    print('Part 1 Solution = ', count_max_calories( get_input('1.in') ))
    print('Part 2 Solution = ', count_top3_calories( get_input('1.in') ))

if __name__ == '__main__':
    main()
