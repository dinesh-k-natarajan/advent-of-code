import pytest
from collections import defaultdict

def get_inputs( filename ):
    """
    Each line contains the ingredients and allergens of a food item.
    This function returns the foods as a list of dicts containing the 
    keys: ingredients and allergens. 
    """
    with open( filename, 'r' ) as input_file:
        lines = input_file.read().splitlines()
    foods = []
    for line in lines:
        ingredients, allergens = line.split(' (contains ')
        ingredients = ingredients.split(' ')
        allergens   = allergens.strip(')').split(', ')
        food = defaultdict( list )
        food['ingredients'] = ingredients
        food['allergens']   = allergens
        foods.append( food )
    return foods 

def non_allergens( foods, part2=False ):
    """
    Part 1 Task:
    Figure out which ingredients do not contain any allergens and count
    the number of their occurence in all the foods.
    """
    allergic = defaultdict( set )
    all_ingredients = set()
    for food in foods:
        ingredients = food['ingredients']
        allergens   = food['allergens']
        all_ingredients |= set( ingredients )
        for allergen in allergens:
            if allergen not in allergic:
                allergic[ allergen ] = set(ingredients)
            else:
                allergic[ allergen ] &= set(ingredients)
    inerts = all_ingredients - set( item for sets in allergic.values() for item in sets ) 
    count = 0
    for food in foods:
        ingredients = food['ingredients']
        count += sum( inert in inerts for inert in ingredients )
    if not part2:
        return count
    else:
        return allergic

def dangerous_ingredients( foods ):
    """
    Part 2 Task:
    This function returns the list of dangerous ingredients (unique to each allergen)
    in alphabetical order of the allergen
    """
    possibly_allergic = non_allergens( foods, part2=True )
    dangerous = defaultdict( str )
    while len( dangerous.keys() ) < len( possibly_allergic.keys() ):
        for allergen, ingredients in possibly_allergic.items():
            if len(ingredients) == 1:
                unique_ingredient = list(ingredients)[0]
                dangerous[ allergen ] = unique_ingredient
                for other_allergen in possibly_allergic:
                    if other_allergen != allergen and unique_ingredient in possibly_allergic[ other_allergen ]:
                        possibly_allergic[ other_allergen ].remove( unique_ingredient )
    return ','.join( [ dangerous[key] for key in sorted( dangerous.keys() ) ] )

@pytest.mark.parametrize( 'test_input, expected', [ ('21.example', 5) ] )
def test_part1( test_input, expected ):
    assert non_allergens( get_inputs( test_input ) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('21.example', 'mxmxvkd,sqjhc,fvjkl') ] )
def test_part2( test_input, expected ):
    assert dangerous_ingredients( get_inputs( test_input ) ) == expected

def main():
    print('Part 1 Solution = ', non_allergens( get_inputs( '21.in' ) ) )
    print('Part 2 Solution = ', dangerous_ingredients( get_inputs( '21.in' ) ) )

if __name__ == '__main__':
    exit( main() )
