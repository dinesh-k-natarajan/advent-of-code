import pytest
from collections import defaultdict

def get_inputs( filename ):
    """
    The input file has a number in each line. 
    This function returns the numbers as a list.
    """
    with open( filename, 'r') as input_file:
        inputs = [ int(item) for item in input_file.read().splitlines() ]
    return sorted(inputs)

def jolt_differences( data ):
    """
    To the given data, add the jolts of the charging outlet at the start and 
    jolt of the device to the end of the adapters list. Since all the adapters 
    have to be used, the difference between the sorted adapters are computed. 
    The 1's and 3's are counted and their multiple is returned. 
    """
    adapters    = [0] + data + [ max(data)+3 ]
    differences = [ adapters[i+1] - adapters[i] for i in range(len(adapters)-1) ]
    return differences.count(1) * differences.count(3)

def count_paths( data ):
    """
    The goal is to find the number of possible paths to connect the charging outlet
    to the device. From the charging outlet, there is only way to connect to the
    next adapter. Then, the number of paths have to be accumulated upto the device
    itself. The problem of finding possible paths from outlet to device is a Forward 
    Dynamic Program. 
    
    The adapters can have a jolt difference of 1 upto 3 jolts, which means any of the
    previous 3 integers are eligible adapter jolts for the current adapter. Thus, the 
    number of paths to connect a given adapter is equal to the sum of number of paths 
    that can connect to the previous 3 adapters. The `paths` dictionary would contain
    keys ranging from 0 to device jolts. Some of these keys will not be adapter jolts.
    Further slicing can be done based on the adapters list to obtain the actual adapter
    paths. Nevertheless, the last entry will remain unchanged. The total number of paths
    for a given list of adapters would then be the number of paths at the last adapter. 
    
    Starting from 1 path at the outlet, 43,406,276,662,336 paths are possible to 
    connect to the device. 
    """
    adapters = [0] + data + [ max(data)+3 ]
    paths    = defaultdict( int )
    paths[0] = 1
    for adapter in adapters[1:]:
        paths[ adapter ] = paths[ adapter-1 ] + paths[ adapter-2 ] + paths[ adapter-3 ]
    adapter_paths = { key:paths[key] for key in set(adapters) & set(paths) } 
    assert list( adapter_paths.keys() ) == adapters
    return adapter_paths[ adapters[-1] ]  

@pytest.mark.parametrize( 'test_input, expected', [ ('10.example', 220) ] )
def test_part1( test_input, expected ):
    assert jolt_differences( get_inputs(test_input) ) == expected

@pytest.mark.parametrize( 'test_input, expected', [ ('10.example', 19208) ] )
def test_part2( test_input, expected ):
    assert count_paths( get_inputs(test_input) ) == expected

def main():
    print('Part 1 Solution = ', jolt_differences( get_inputs('10.in') ) )
    print('Part 2 Solution = ', count_paths(      get_inputs('10.in') ) )

if __name__ == '__main__':
    exit( main())
