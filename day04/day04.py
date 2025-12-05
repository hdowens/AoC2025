from pathlib import Path
from argparse import ArgumentParser

directions = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
]

def find_remove_rolls(rolls: dict):

    tot = 0
    removed_rolls = set()
    for line_no, char_no in rolls:

        paper_count = 0
        for direction in directions:
            check_x = line_no + direction[0]
            check_y = char_no + direction[1]
            if (check_x, check_y) in rolls:
                paper_count += 1
        
        if paper_count < 4:
            tot += 1
            removed_rolls.add((line_no, char_no))

    return tot, removed_rolls

def main(file_path: Path) -> None:
    
    with open(file_path, "r") as f:
        data = [line.strip() for line in f.read().splitlines()]

    rolls = {
        (r, c)
        for r, line in enumerate(data)
        for c, ch in enumerate(line)
        if ch == '@'
    }

    tot = 0
    round_tot = -1
    p1 = False
    while round_tot != 0:
        round_tot, removed = find_remove_rolls(rolls)

        if not p1:
            print(f"Part 1: {round_tot}")
            p1 = True

        rolls -= removed
        tot += round_tot

    print(f"Part 2: {tot}")

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
    
    