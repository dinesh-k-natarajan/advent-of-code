import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [''.join(line.split(' ')) for line in input_file.read().splitlines()]

def decode_outcome(games):
    """
    Decide the outcomes of game w.r.t Player 2
    """
    possible_outcomes = {
        'W': ['RP', 'PS', 'SR'],
        'D': ['RR', 'PP', 'SS'],
        'L': ['RS', 'PR', 'SP']
    }
    return [[key for key, value in possible_outcomes.items() if game in value][0] for game in games]

SHAPES_TO_POINTS  = {'R':1, 'P':2, 'S':3}
RESULTS_TO_POINTS = {'W':6, 'D':3, 'L':0}

def count_score_part1( games ):
    """
    games is a list of lists with each list containing [opponent_shape, your_shape]
    ABC is opponent's RPS, XYZ is my RPS
    """
    translator = {'A':'R', 'B':'P', 'C':'S', 'X':'R', 'Y':'P', 'Z':'S'}
    translated_games = [''.join([translator[game[0]], translator[game[1]]]) for game in games]
    return sum([SHAPES_TO_POINTS[game[1]] for game in translated_games] 
            + [RESULTS_TO_POINTS[result] for result in decode_outcome(translated_games)])
    
def decode_choice( games ): 
    """
    Decode the choice of Player 2 based on Player 1 and desired outcome
    """
    possible_choices = {
        'R': ['SW', 'RD', 'PL'],
        'P': ['RW', 'PD', 'SL'],
        'S': ['PW', 'SD', 'RL'],
    }
    return [[key for key, value in possible_choices.items() if game in value][0] for game in games]

def count_score_part2( games ):
    """ 
    games is a list of lists with each list containing [opponent_shape, desired_result]
    xyz_to_results = {'X':'L', 'Y':'D', 'Z': 'W'}
    """
    translator = {'A':'R', 'B':'P', 'C':'S', 'X':'L', 'Y':'D', 'Z':'W'}
    translated_games = [''.join([translator[game[0]], translator[game[1]]]) for game in games]
    return sum([SHAPES_TO_POINTS[game] for game in decode_choice(translated_games)] 
            + [RESULTS_TO_POINTS[game[1]] for game in translated_games])

@pytest.mark.parametrize( 'test_input,expected', [ ('2.example', 15) ] )
def test_part1( test_input, expected ):
    assert count_score_part1( get_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('2.example', 12) ] )
def test_part2( test_input, expected ):
    assert count_score_part2( get_input(test_input) ) == expected

def main():
    print('Part 1 Solution = ', count_score_part1( get_input('2.in') ))
    print('Part 2 Solution = ', count_score_part2( get_input('2.in') ))

if __name__ == '__main__':
    main()