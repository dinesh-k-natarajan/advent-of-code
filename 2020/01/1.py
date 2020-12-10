import pytest

def product_of_2( numbers ):
    numbers = [ int( item ) for item in numbers ]
    for i in range( len(numbers) ):
        for j in range( i+1, len(numbers) ):
            if numbers[i] + numbers[j] == 2020:
                return numbers[i] * numbers[j] 

def product_of_3( numbers ):
    numbers = [ int( item ) for item in numbers ]
    for i in range( len(numbers) ):
        for j in range( i+1, len(numbers) ):
            for k in range( j+1, len(numbers) ):
                if numbers[i] + numbers[j] + numbers[k] == 2020:
                   return numbers[i] * numbers[j] * numbers[k]

@pytest.mark.parametrize('test_input,expected',[ (['1721','979','366','299','675','1456'], 514579) ] )
def test_part1( test_input, expected ):
    assert product_of_2( test_input ) == expected

@pytest.mark.parametrize('test_input,expected',[ (['1721','979','366','299','675','1456'], 241861950) ] )
def test_part2( test_input, expected ):
    assert product_of_3( test_input ) == expected

def main():
    with open('1.in','r') as input_file:
        expenses = input_file.read().splitlines()
    print('Part 1 Solution = ', product_of_2( expenses ))
    print('Part 2 Solution = ', product_of_3( expenses ))

if __name__ == '__main__':
    exit( main() )
