def get_inputs( filename ):
    """
    Each line in the input file is a math expression.
    This function returns a list containing each line.
    """
    with open( filename, 'r' ) as input_file:
        inputs = input_file.read().splitlines()
    return inputs

class NumType1:
    """
    A class of numbers that has '-' replaced by '*' such that
    '+' and '-' have equal precedence. 
    i.e., '+' -> '+', '*' -> '-'
    """
    def __init__( self, value ):
        self.value = value

    def __add__( self, num2 ):
        return NumType1( self.value + num2.value )

    def __sub__( self, num2 ):
        return NumType1( self.value * num2.value )

class NumType2:
    """
    A class of numbers that has '+' and '*' operators reversed 
    via remapping via '-', such that '+' has higher precedence than '*'. 
    i.e., '+' -> '*', '*' -> '-'
    """
    def __init__( self, value ):
        self.value = value

    def __mul__( self, num2 ):
        return NumType2( self.value + num2.value )

    def __sub__( self, num2 ):
        return NumType2( self.value * num2.value )

def modify_string( string, part2=False ):
    """
    The string representing the expression is modified such that
    the numbers are replaced by the newly defined number classes 
    that determine the operator precedence.
    *** Solution partly inspired by user: geohot (George Hotz) ***
    """
    modified_string = ''
    numbers_list = ['0','1','2','3','4','5','6','7','8','9']
    num_class = 'NumType1' if not part2 else 'NumType2'
    prev_was_num = False
    for char in string:
        if char in numbers_list and not prev_was_num:
            modified_string += num_class + '('
            prev_was_num = True
        elif char not in numbers_list and prev_was_num:
            modified_string += ')'
            prev_was_num = False
        modified_string += char
    if prev_was_num:
        modified_string += ')'
    return modified_string

def changed_precedence( expressions, part2=False ):
    """
    Task:
    For Part 1, each expression is to be evaluated with
    equal operator precedence for '+' and '*'. Parenthesis 
    are evaluated as usual, with the highest precedence.

    Method:
    A new class of numbers where '+' and '*' have equal 
    precedence is defined by leveraging the equal precedence
    between '+' and '-' in standard numbers.
    
    The numbers in the expression strings are replaced by the newly
    defined NumType1(  ) class. The strings can then be evaluated 
    using eval().

    This function returns the sum of results of each expression.
    
    For Part 2:
        - '+' has higher precedence than '*'
        - done by remapping '*' to '-' to achieve equal precedence
        - followed by remapping '+' to '*' to achieve reversed precedence
        - i.e., '+' -> '*' and '*' -> '-'
    """
    result = 0
    for expression in expressions:
        modified_expression = modify_string( expression, part2 )
        modified_expression = modified_expression.replace( '*', '-' )
        if part2:
            modified_expression = modified_expression.replace( '+', '*' )
        result += eval( modified_expression ).value 
    return result

def main():
    print('Part 1 Solution = ', changed_precedence( get_inputs('18.in') ) )
    print('Part 2 Solution = ', changed_precedence( get_inputs('18.in'), part2=True ) )

if __name__ == '__main__':
    exit( main() )
