import time
import pytest
import re
import math

def parse_input(filename):
    with open(filename,'r') as input_file:
        groups  = input_file.read().split('\n\n')
        monkeys = []
        for group in groups:
            lines     = group.splitlines()
            contents  = [int(item) for item in re.findall(r'\d+', lines[1])]
            operation = lines[2].split('Operation: ')[1].split('new = ')[1].split(' ')
            divider   = int(re.findall(r'\d+',lines[3])[0])
            if_true   = int(re.findall(r'\d+', lines[4])[0])
            if_false  = int(re.findall(r'\d+', lines[5])[0])
            monkeys.append({
                'contents' : contents,
                'operation': operation,
                'divider'  : divider,
                'if_true'  : if_true,
                'if_false' : if_false
            })
        return monkeys

def compute_new_worry(worry, operation):
    # Example: operation = ['old', '*', '6'] => new = old * 6
    if operation[1] == '*':
        op = lambda operand1,operand2: operand1 * operand2
    elif operation[1] == '+':
        op = lambda operand1,operand2: operand1 + operand2
    if operation[2].isdigit():
        number = int(operation[2])
    elif operation[2] == 'old':
        number = worry
    return op(worry,number)

def compute_monkey_business(monkeys, n_rounds=20, part2=False):
    for monkey in monkeys:
        monkey['n_inspected'] = 0 # Keep track of how many items the monkeys inspect
    LCM = math.lcm(*[monkey['divider'] for monkey in monkeys])
    for _ in range(n_rounds):
        for monkey in monkeys:
            while len(monkey['contents']) > 0: # iterate until monkey has no items
                monkey['n_inspected'] += 1
                # remove item under inspection from start of list
                item = monkey['contents'].pop(0) 
                item = compute_new_worry(item, monkey['operation'])
                if not part2: # Integer division of worry levels by 3 is used
                    item = item//3
                else: # Modulus of worry levels with LCM of dividers is used
                    item = item % LCM
                # throw the item to another monkey and add it to end of list
                if item % monkey['divider'] == 0: # if divisible
                    monkeys[monkey['if_true']]['contents'].append(item)
                else: 
                    monkeys[monkey['if_false']]['contents'].append(item)
    # Compute the product of n_inspected of the two most active monkeys
    active_monkeys = sorted([monkey['n_inspected'] for monkey in monkeys], reverse=True)
    return active_monkeys[0]*active_monkeys[1]

@pytest.mark.parametrize('test_input,expected', [('11.example',10605)])
def test_part1(test_input,expected):
    assert compute_monkey_business(parse_input(test_input)) == expected

@pytest.mark.parametrize('test_input,expected', [('11.example',2713310158)])
def test_part2(test_input,expected):
    assert compute_monkey_business(parse_input(test_input), n_rounds=10000, part2=True) == expected

def main():
    start_time = time.perf_counter()
    print(f"Part 1 Solution = {compute_monkey_business(parse_input('11.in'))}")
    print(f"Part 2 Solution = {compute_monkey_business(parse_input('11.in'), n_rounds=10000, part2=True)}")
    end_time = time.perf_counter()
    print(f'Execution took {(end_time-start_time):.5f} s')

if __name__ == '__main__':
    main()

"""
NOTE: 'Worry levels are no longer divided by three after each item is inspected; 
you'll need to find another way to keep your worry levels manageable.'

Trick to speed-up part 2 from r/adventofcode comment by u/wojtek-graj
Link: https://www.reddit.com/r/adventofcode/comments/zifqmh/comment/izr3h4t/

The item values keep increasing for longer rounds, thus item % divider is costly.
Computing item % divider is equivalent to computing (item % LCM(all dividers)) % divider, 
as shown below (comment by u/Fickle_Dragonfly4381)

91238 % 5 = 3
91238 % 7 = 0

91238 % (5 * 7) = 28
28 % 5 = 3
28 % 7 = 0   

Thus, for part 2, instead of worry level//3, I use worry level % LCM(dividers) 
"""