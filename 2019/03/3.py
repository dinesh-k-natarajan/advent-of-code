import pytest

def get_inputs():
    with open('3.in','r') as input_file:
        inputs = input_file.read().splitlines()
        inputs = [ item.split(',') for item in inputs ]
    return inputs

def split_paths( wire_path ):
    directions = [ instruction[0] for instruction in wire_path ]
    deltas = [ int(instruction[1:]) for instruction in wire_path ]
    return directions, deltas

def trace_paths( wire_path, central_port ):
    directions, deltas = split_paths( wire_path )
    logs = [] 
    steps = []
    logs.append( central_port )
    steps.append(0)
    for direction, delta in zip(directions, deltas):
        if direction == 'R':
            new_points = [ (logs[-1][0]+(dx+1), logs[-1][1]) for dx in range(delta) ]
        elif direction == 'L':
            new_points = [ (logs[-1][0]-(dx+1), logs[-1][1]) for dx in range(delta) ]
        elif direction == 'U':
            new_points = [ (logs[-1][0], logs[-1][1]+(dy+1)) for dy in range(delta) ]
        else:
            assert direction == 'D'
            new_points = [ (logs[-1][0], logs[-1][1]-(dy+1)) for dy in range(delta) ]
        logs  += new_points
        steps += [ steps[-1]+(step+1) for step in range(len(new_points)) ]
    return logs, steps

def compute_distance( intersection_points, central_port ):
    distances = []
    for point in intersection_points:
        distances.append( abs(point[0]-central_port[0]) + abs(point[1]-central_port[1]) )
    return min(distances)

def compute_steps( intersections, logs_1, logs_2, steps_counter_1, steps_counter_2 ):
    combined_steps = []
    for point in list(intersections):
        steps_to_int_1 = steps_counter_1[ logs_1.index( point ) ] 
        steps_to_int_2 = steps_counter_2[ logs_2.index( point ) ]
        combined_steps.append( steps_to_int_1 + steps_to_int_2 )
    return min( combined_steps )

def get_solution( wires_paths, part2=False ):
    central_port = ( 0,0 )
    wire1_logs, wire1_steps = trace_paths( wires_paths[0], central_port )
    wire2_logs, wire2_steps = trace_paths( wires_paths[1], central_port )
    intersection_points = set(wire1_logs) & set(wire2_logs)
    intersection_points.discard( central_port )
    if not part2:
        return compute_distance( intersection_points, central_port )
    else:
        return compute_steps( intersection_points, wire1_logs, wire2_logs, wire1_steps, wire2_steps )

@pytest.mark.parametrize( 'test_input, expected',
                          [ ([ ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
                               ['U62','R66','U55','R34','D71','R55','D58','R83'] ], 159),
                            ([ ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
                               ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7'] ], 135) ] )
def test_part1( test_input, expected ):
    assert get_solution( test_input ) == expected

@pytest.mark.parametrize( 'test_input, expected',
                          [ ([ ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
                               ['U62','R66','U55','R34','D71','R55','D58','R83'] ], 610),
                            ([ ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
                               ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7'] ], 410) ] )
def test_part2( test_input, expected ):
    assert get_solution( test_input, part2=True ) == expected

def main():
    wires_paths = get_inputs()
    # Part 1
    manhattan_distance = get_solution( wires_paths )
    print('Part 1 Solution = ', manhattan_distance )
    
    # Part 2
    fewest_steps = get_solution( wires_paths, part2=True )
    print('Part 2 Solution = ', fewest_steps )

if __name__ == '__main__':
    exit( main() )
