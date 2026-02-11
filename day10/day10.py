import re
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations
from functools import lru_cache
from collections import defaultdict

def parse_input(line: str):
    
    diagram, *buttons, joltages = (
        part[1:-1] for part in line.split()
    )

    diagram = [1 if d == '#' else 0 for d in diagram]
    
    buttons = [list(map(int, re.findall(r'\d+', b))) for b in buttons]

    joltages = list(map(int, re.findall(r'\d+', joltages)))

    return diagram, buttons, joltages

def design_diagram(diagram, buttons):
    for i in range(1, len(buttons)):
        for combo in combinations(buttons, i):
            
            state = [0] * len(diagram) 
            
            for lights in list(combo):
                for light in lights:
                    state[light] ^= 1

            if state == diagram:
                return i


def all_states(diagram, buttons):
    states = defaultdict(list)

    for i in range(len(buttons) + 1):
        for combo in combinations(buttons, i):

            state = [0] * len(diagram)

            for lights in combo:
                for light in lights:
                    state[light] ^= 1

            state_key = tuple(state)
            states[state_key].append(combo)

    return states


def part2(joltages, solutions):

    @lru_cache(maxsize=None)
    def get_minimum_button_presses(joltages):
        
        if not any(joltages):
            return 0
        
        lights = tuple(
            j%2 for j in joltages
        )

        res = None
        for solution in solutions[lights]:
            
            l_joltages = list(joltages)

            for buttons in solution:
                for light in buttons:
                    l_joltages[light] -= 1

            if any(j < 0 for j in l_joltages):
                continue

            half_target = tuple(j // 2 for j in l_joltages)
            half_target_presses = get_minimum_button_presses(half_target)
            if half_target_presses is None:
                continue

            tot_presses = len(solution) + 2 * half_target_presses

            if res is None:
                res = tot_presses
            else:
                res = min(res, tot_presses)

        return res
    
    return get_minimum_button_presses(tuple(joltages))



def main(file_path: Path) -> None:

    with open(file_path, "r") as f:
        data = [line.strip() for line in f.read().splitlines()]

    p1_tot = 0
    p2_tot = 0
    for line in data:
        diagram, buttons, joltages = parse_input(line)
                
        p1_tot += design_diagram(diagram, buttons)
        
        solutions = all_states(diagram, buttons)
        p2_tot += part2(joltages, solutions)

    print(f"Part 1: {p1_tot}")
    print(f"Part 2: {p2_tot}")
        

if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--test', action='store_true', help='Read from test_input.txt')
    group.add_argument('-p', '--puzzle', action='store_true', help='Read from puz_input.txt')
    
    args = parser.parse_args()
    script_dir = Path(__file__).parent
    if args.test:
        file_path = script_dir / Path("test_input.txt")
    elif args.puzzle:
        file_path = script_dir / Path("puz_input.txt")
    
    main(file_path)
    
    