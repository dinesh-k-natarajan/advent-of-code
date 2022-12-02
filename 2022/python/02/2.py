import pytest

def get_input( filename ):
    with open(filename,'r') as input_file:
        return [line.split(' ') for line in input_file.read().splitlines()]

def compute_RPS_results( games ): 
    """ 
    list of games with each game containing [opponent_shape, your_shape]
    """
    results = []
    for game in games:
        if game[1] == game[0]: results.append('D')
        elif game[1]=='R':
            if game[0]=='S': results.append('W') # Rock beats scissors
            elif game[0]=='P': results.append('L') # Rock loses to paper
        elif game[1]=='P':
            if game[0]=='R': results.append('W') # Paper beats rock
            elif game[0]=='S': results.append('L') # Paper loses to scissors
        elif game[1]=='S':
            if game[0]=='P': results.append('W') # Scissors beats paper
            elif game[0]=='R': results.append('L') # Scissors loses to rock
    return results

def count_score_part1( games ):
    """
    games is a list of lists with each list containing [opponent_shape, your_shape]
    Strategy guide:
    Points for shapes: {'R':1, 'P':2, 'S':3}
    Points for results: {'W':6, 'D':3, 'L':0}
    """
    shapes_to_RPS = {'A':'R', 'B':'P', 'C':'S', 'X':'R', 'Y':'P', 'Z':'S'}
    translated_games = [[shapes_to_RPS[game[0]], shapes_to_RPS[game[1]]] for game in games]
    results = compute_RPS_results(translated_games)
    shapes_to_points = {'R':1, 'P':2, 'S':3}
    results_to_points = {'W':6, 'D':3, 'L':0}
    points_from_shapes = [shapes_to_points[game[1]] for game in translated_games]
    points_from_results = [results_to_points[result] for result in results]
    return sum([p1+p2 for p1,p2 in zip(points_from_shapes, points_from_results)])

def decode_games( games ):
    """
    games is a list of lists with each list containing [opponent_shape, desired_result]
    xyz_to_results = {'X':'L', 'Y':'D', 'Z': 'W'}
    Compute your shapes according to desired results.
    """
    shapes_to_RPS = {'A':'R', 'B':'P', 'C':'S'}
    xyz_to_results = {'X':'L', 'Y':'D', 'Z': 'W'}
    translated_games = [[shapes_to_RPS[game[0]],xyz_to_results[game[1]]] for game in games]
    results = [xyz_to_results[game[1]] for game in games]
    decoded_games = []
    for game in translated_games:
        if  game[1] == 'D': decoded_game = [game[0], game[0]] # copycat
        elif game[1] == 'W':
            if game[0] == 'R': decoded_game = [game[0], 'P'] # P beats R
            elif game[0] == 'P': decoded_game = [game[0], 'S'] # S beats P
            elif game[0] == 'S': decoded_game = [game[0], 'R'] # R beats S
        elif game[1] == 'L':
            if game[0] == 'R': decoded_game = [game[0], 'S'] # S loses to R
            elif game[0] == 'P': decoded_game = [game[0], 'R'] # R loses to P
            elif game[0] == 'S': decoded_game = [game[0], 'P'] # P loses to S
        decoded_games.append(decoded_game)
    return results, decoded_games

def count_score_part2( games ):
    """ 
    games is a list of lists with each list containing [opponent_shape, desired_result]
    xyz_to_results = {'X':'L', 'Y':'D', 'Z': 'W'}
    Strategy guide remains the same:
    Strategy guide:
    Points for shapes: {'R':1, 'P':2, 'S':3}
    Points for results: {'W':6, 'D':3, 'L':0}
    """
    results, decoded_games = decode_games( games )
    shapes_to_points = {'R':1, 'P':2, 'S':3}
    results_to_points = {'W':6, 'D':3, 'L':0}
    points_from_shapes = [shapes_to_points[game[1]] for game in decoded_games]
    points_from_results = [results_to_points[result] for result in results]
    return sum([p1+p2 for p1,p2 in zip(points_from_shapes, points_from_results)])

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