import pytest

def get_inputs( filename ):
    """
    The input notes consists of two lines. 
    Line 1 - estimate of earliest timestamp of departure
    Line 2 - bus IDs in service, where 'x' = out of service
    This function returns a dict with the time, buses in service and their offsets
    """
    with open( filename, 'r' ) as input_file:
        raw_data = input_file.read().splitlines()
    time   = int(raw_data[0])
    buses  = [ int(item) for item in raw_data[1].split(',') if item != 'x']
    offsets = [ raw_data[1].split(',').index( str(item) ) for item in buses ]
    return { 'time': time, 'buses': buses, 'offsets': offsets }


def earliest_bus( notes ):
    """
    Setup: 
    All buses depart at 0 mins. Trip duration of each bus = bus ID in minutes. 
    i.e., every 'ID' mins, the bus with that ID departs from the starting point. 
    Thus, if the time is divisible by the bus ID, that bus will start its departure. 

    Method:
    The remainder between current time and bus ID denotes the time in mins to the 
    previous departure of each bus. Subtracting this value from the bus ID gives
    the time in mins to the next departure of each bus. 

    Task:
    Given the time and available buses, this function returns the product of ID of 
    next earliest bus and minutes to wait to catch that bus. 
    """
    time      = notes[ 'time'  ]
    buses     = notes[ 'buses' ]
    deltas    = [ bus - ( time % bus ) for bus in buses ]
    wait_time = min( deltas )
    next_bus  = buses[ deltas.index( wait_time ) ]
    return wait_time * next_bus

def get_timestamp( notes ):
    """
    Setup:
    Considering only the buses in service and their offsets in the list, the goal is to
    find the starting time such the buses depart in offsets after 'offsets' minutes from
    that starting time.

    Method:
    Assume t = 0 for the first bus. The step should be bus ID of first bus. Every t + step
    satisfies the contest rule w.r.t first bus. 

    For the second bus, find t such that t + offset is divisible by bus ID. Instead of
    stepping through all possible t's, it is sufficient to step through t with step of the
    previous bus ID. After finding the t that satisfies both the buses, update the step as
    the multiple of the currently satisfied bus IDs. 

    This process is repeated over all the buses, while updating the step size as the multiple
    of the previous IDs. After looping through all the buses, the t now satisfies the contest
    rules.
    
        ** Solution partly inspired by reddit user: passwordsniffer ** 
    
    NOTE: This problem could also be solved using the Chinese Remainder Theorem (TODO)

    Task: 
    This function returns the earliest timestamp that satisfies the contest rules
    """
    buses       = notes[ 'buses' ]
    offsets     = notes[ 'offsets' ]
    timestamp   = 0
    step        = buses[0]
    for bus, offset in zip( buses[1:], offsets[1:] ):
        while ( timestamp + offset ) % bus != 0:
            timestamp += step
        step *= bus
    return timestamp

@pytest.mark.parametrize( 'test_input, expected', [ ('13.example', 295) ] )
def test_part1( test_input, expected ):
    assert earliest_bus( get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('13.example', 1068781) ] )
def test_part2( test_input, expected ):
    assert get_timestamp( get_inputs(test_input) ) == expected

def main():
    print('Part 1 Solution = ', earliest_bus(  get_inputs( '13.in' ) ) )
    print('Part 2 Solution = ', get_timestamp( get_inputs( '13.in' ) ) )

if __name__ == '__main__':
    exit( main() )
