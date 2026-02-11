from pathlib import Path
from argparse import ArgumentParser
from functools import reduce
import operator

def parse_input(data):

    sections = data.split("\n\n")
    presents = sections[:len(sections)-1]
    regions  = sections[-1].split("\n")

    regions = [reg.split(":") for reg in regions]
    regions = [
        (
            reduce(operator.mul, map(int, size.split("x"))),
            shapes.strip()
        ) 
        for size, shapes in regions
    ]
    return presents, regions

def main(file_path: Path) -> None:
    
    with open(file_path, "r") as f:
        data = f.read()

    presents, regions = parse_input(data)
    tot = 0
    for reg in regions:
        total_size, shapes = reg

        if (sum(map(int, shapes.split(" "))) * 8) < total_size:
            tot += 1

    print(f"Part 1: {tot}")
    print(f"Part 2: -----WINNAR----")

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
    
    