import pytest
from copy import deepcopy

def get_inputs( filename ):
    """
    The input file contains the starting decks of each player. 
    This function returns a list of lists of their decks.
    """
    with open( filename, 'r' ) as input_file:
        raw_data = input_file.read().split('\n\n')
    decks = []
    for num, raw_deck in enumerate(raw_data):
        deck = [int(card) for card in raw_deck.splitlines()[1:] ]
        decks.append( deck )
    return decks

def calc_score( winning_deck ):
    """
    This function returns the score of the winning player
    """
    score = 0
    for point, card in enumerate( winning_deck[::-1] ):
        score += (point+1) * card
    return score

def play_round( decks ):
    """
    Plays a single round of the combat game.
    This function returns the decks after one round.
    """
    cards = [ deck.pop(0) for deck in decks ]
    if cards[0] > cards[1]:
        decks[0] += [ cards[0], cards[1] ]
    elif cards[1] > cards[0]:
        decks[1] += [ cards[1], cards[0] ]
    return decks

def recursive_combat( decks ):
    """
    Plays recursive combat game based on the additional rules defined in
    Part 2.
    """
    history = set()
    rounds = 1
    while all( [ len(deck)!=0 for deck in decks ] ):
        current_decks = ( ','.join( str(card) for card in decks[0] ),
                          ','.join( str(card) for card in decks[1] )  )
        if current_decks in history:
            return [ decks[0], [] ]
        history.add( current_decks ) 
        cards = [ deck.pop(0) for deck in decks ]
        flags = [ len(deck) >= card for (deck,card) in [(decks[0],cards[0]), (decks[1],cards[1]) ] ] 
        if all( flags ):
            #print( 'sub-game starts' )
            sub_decks = [ decks[0][:cards[0]], decks[1][:cards[1]] ]
            sub_decks = recursive_combat( sub_decks )
            #print( 'sub-game ends' )
            winner = [ player for (player,deck) in enumerate(sub_decks) if len(deck)!=0 ][0]
        else:
            winner = cards.index( max(cards) )
        won_cards = [ cards[winner], cards[1-winner] ]
        decks[winner] += won_cards
        #print( rounds, decks )
        rounds += 1
    return decks

def play_combat( decks, part2=False ):
    """
    Continue to play the card game until there is a winner.
    This function returns the score of the winner.
    """
    rounds = 1
    if not part2:
        while all( [ len(deck)!=0 for deck in decks ] ):
            decks = play_round( decks )
            rounds += 1
    else:
        decks = recursive_combat( decks )
    #print( 'final decks: ', decks )
    winner = [ player for (player,deck) in enumerate(decks) if len(deck)!=0 ][0]
    return calc_score( decks[ winner ] )

@pytest.mark.parametrize( 'test_input, expected', [ ('22.example1', 306) ] )
def test_part1( test_input, expected ):
    assert play_combat( get_inputs( test_input ) ) == expected
    
@pytest.mark.parametrize( 'test_input, expected', [ ('22.example1', 291), 
                                                    ('22.example2', 105) ] )
def test_part2( test_input, expected ):
    assert play_combat( get_inputs( test_input ), part2=True ) == expected

def main():
    print('Part 1 Solution = ', play_combat( get_inputs( '22.in' ) ) )
    print('Part 2 Solution = ', play_combat( get_inputs( '22.in' ), part2=True) )

if __name__ == '__main__':
    exit( main() )
