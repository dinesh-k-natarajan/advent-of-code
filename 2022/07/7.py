import time
import pytest

# Custom Directory class
class Directory:
    def __init__(self, name, parent_dir=None):
        self.name = name
        self.parent_dir = parent_dir
        self.contents = None

    def add_contents(self, contents):
        self.contents = contents
    
    def get_contents(self):
        return [item.name for item in self.contents]

    def get_child_dir(self):
        child_dirs = [item for item in self.contents if isinstance(item, Directory)]
        for item in child_dirs:
            grandchild_dirs = item.get_child_dir()
            if grandchild_dirs is not None:
                child_dirs += grandchild_dirs
        return list(set(child_dirs)) # AFTER DEBUGGING: use sets to avoid duplicates
        
    def get_size(self):
        self.size = 0
        for item in self.contents: 
            self.size += item.get_size()
        return self.size

# Custom File class
class File:
    def __init__(self, name=None, size=None, parent_dir=None):
        self.name = name
        self.size = size
        self.parent_dir = parent_dir
    
    def get_size(self):
        return self.size

# Parsing function
def parse_input( filename ):
    with open(filename,'r') as input_file:
        groups = input_file.read().split('$ ')[1:]
        groups = [[item for item in group.split('\n') if item!=''] for group in groups]
        filesystem = Directory(name='/', parent_dir=None)
        current_dir = filesystem
        for group in groups:
            # if cd command
            if len(group)==1 and group[0].startswith('cd'):
                dest_dir = group[0].split('cd ')[-1]
                if dest_dir == '..': # go up a directory
                    current_dir = current_dir.parent_dir
                elif dest_dir == '/': # go to root directory
                    current_dir = filesystem
                elif dest_dir not in ['..', '/']:
                    # if dest_dir does not exist inside current_dir
                    if dest_dir not in current_dir.get_contents():
                        current_dir = Directory(name=dest_dir, parent_dir=current_dir)
                    # if dest_dir already exists inside current_dir
                    if dest_dir in current_dir.get_contents(): 
                        idx = current_dir.get_contents().index(dest_dir)
                        current_dir = current_dir.contents[idx]
                else: 
                    raise ValueError('Unknown directory used in cd command!')
            # if ls command
            if len(group)>1 and group[0].startswith('ls'):
                contents = [line.split(' ') for line in group[1:]]
                for idx, item in enumerate(contents):
                    ## if directory
                    if item[0]=='dir':
                        item_ = Directory(name=item[1], parent_dir=current_dir)
                    ## if file
                    if item[0].isdigit():
                        item_ = File(name=item[1], size=int(item[0]), parent_dir=current_dir)
                    ## Replace item in contents with the categorized item_
                    contents[idx] = item_
                # Add categorized contents to the current_dir
                current_dir.add_contents(contents)
        return filesystem

TOTAL_DISK = 70000000
MIN_UNUSED_SPACE = 30000000

def compute_size( filesystem, part2=False):
    total_size = filesystem.get_size()
    dir_sizes = [total_size] + [item.size for item in filesystem.get_child_dir()]
    if not part2:
        # find sum of sizes of directories with atmost 100000 size
        return sum([size for size in dir_sizes if size<=100000])
    elif part2:
        # find size of smallest directory to delete to have atleast MIN_UNUSED_SPACE free
        unused_space = TOTAL_DISK - dir_sizes[0]
        return min([size for size in dir_sizes if (size+unused_space>=MIN_UNUSED_SPACE)])

@pytest.mark.parametrize( 'test_input,expected', [ ('7.example', 95437) ] )
def test_part1( test_input, expected ):
    assert compute_size( parse_input(test_input) ) == expected

@pytest.mark.parametrize( 'test_input,expected', [ ('7.example', 24933642) ] )
def test_part2( test_input, expected ):
    assert compute_size( parse_input(test_input), part2=True ) == expected

def main():
    start_time = time.perf_counter()
    print('Part 1 Solution = ', compute_size( parse_input('7.in') ))
    print('Part 2 Solution = ', compute_size( parse_input('7.in'), part2=True ))
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()