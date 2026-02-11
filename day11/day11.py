from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict
from functools import lru_cache

def parse_input(data):
    wires = defaultdict(list)
    for line in data:
        device, output = line.strip().split(":")
        wires[device] = output.split() 

    return wires

def part1(wires, starting_state="you") -> int:
    count = 0
    
    S = [starting_state]
    while len(S) > 0:
        v = S.pop()

        if v == "out":
            count += 1

        for edge in wires[v]:
            S.append(edge)

    return count

# ITERATIVE CASE IS SO SLOW
# NEED TO MOVE IT TO RECURSIVE CASE
# SO WE CAN ENABLE MEMOISATION
# WE ALSO THEN CAN DITCH THE PATHS AS 
# WE DONT ACTUALLY CARE ABOUT THE WHOLE PATH

#def part2(wires, starting_state="svr"):
#    all_paths = []
#
#    S = [(starting_state, [starting_state])]
#    while len(S) > 0:
#        v, path = S.pop()
#
#        if v == "out":
#            all_paths.append(path)
#
#        for edge in wires[v]:
#            S.append((edge, [edge] + path))
#
#    return len([i for i in all_paths if "fft" in i and "dac" in i])

def part2(wires, starting_state="svr"):

    # we dont actually care about the path
    # we only care if "dac" and "fft" have 
    # been seen in the path. Therfore, we
    # setup the definition of the DFS with
    # these flags
    @lru_cache(maxsize=None)
    def dfs(node, seen_fft, seen_dac):

        if node == "out":
            return int(seen_fft and seen_dac)

        total = 0
        for edge in wires[node]:
            total += dfs(
                edge, 
                seen_fft or (edge == "fft"),
                seen_dac or (edge == "dac")
            )
        return total

    return dfs(starting_state, False, False)



def main(file_path: Path) -> None:
    with open(file_path, "r") as f:
        data = f.readlines()

    tree = parse_input(data)
    print(f"Part 1: {part1(tree)}")
    print(f"Part 2: {part2(tree)}")





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
    


""" 
def main(file_path: Path) -> None:
    with open(file_path, "r") as f:
        data = f.readlines()

    tree = parse_input(data)
    
    count = 0
    discovered = []
    S = ["you"]
    while len(S) > 0:
        v = S.pop()

        if v == "out":
            count += 1

        if v not in discovered:
            discovered.append(v)
            for edge in tree[v]:
                S.append(edge)


    print(count)



"""