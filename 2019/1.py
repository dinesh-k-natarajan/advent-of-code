import pytest

def fuel_equation( mass ):
    return ( mass // 3 ) - 2

def compute_fuel( masses, part2=False ):
    total_fuel = 0
    for mass in masses.splitlines():
        fuel = fuel_equation( int(mass) )
        if part2:
            fuel_for_fuel = fuel_equation( fuel )
            while fuel_for_fuel > 0:
                fuel += fuel_for_fuel
                fuel_for_fuel = fuel_equation( fuel_for_fuel )
        total_fuel += fuel
    return total_fuel

@pytest.mark.parametrize('test_input,expected',[ ('12',2),
                                                  ('14',2),
                                                  ('1969',654),
                                                  ('100756',33583) ] )
def test_part1( test_input, expected ):
    assert compute_fuel( test_input ) == expected

@pytest.mark.parametrize('test_input,expected',[ ('14',2),
                                                  ('1969',966),
                                                  ('100756',50346) ] )
def test_part2(test_input, expected ): 
    assert compute_fuel( test_input, part2=True  ) == expected

def main():
    with open('1.in','r') as input_file:
        masses = input_file.read()
    print('Part 1 Solution = ', compute_fuel( masses ))
    print('Part 2 Solution = ', compute_fuel( masses, part2=True ))

if __name__ == '__main__':
    exit( main() )
