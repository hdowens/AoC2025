from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations

def solve(data, joltage_length: int):
    tot = 0
    for rating in data:
        potent = ""
        max_dig = 9
        while max_dig > 0:
            found = rating.find(str(max_dig))
            if found == -1:
                max_dig -= 1
            
            #length of potential joltage
            #plus length of where it is in the string
            #should be greater than or equal to the length we want
            elif len(potent) + (len(rating) - found) >= joltage_length:
                if len(potent) < joltage_length:
                    potent += rating[found]
                    rating = rating[found+1:]
                    max_dig = 9
                else:
                    max_dig -= 1
            else:
                max_dig -= 1

        tot += int(potent) 
    return tot

def main(file_path: Path) -> None:
    
    with open(file_path, "r") as f:
        data = [l.strip() for l in f.readlines()]

    print(f"Part 1: {solve(data, joltage_length=2)}")
    print(f"Part 2: {solve(data, joltage_length=12)}")

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
    
    