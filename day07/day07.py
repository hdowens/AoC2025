from pathlib import Path
from argparse import ArgumentParser

def part1(data, splitters):
    beams = {data[0].index('S')}
    splits = 0

    for i in range(1, len(data)):
        new_beams = set()

        row_splitters = [s for s in splitters if s[0] == i]
        for spt in row_splitters:
            if spt[1] in beams:
                splits += 1
                beams.remove(spt[1])
                beams.add(spt[1]-1)
                beams.add(spt[1]+1)

        new_beams |= beams

    return splits

def part2(data, splitters):

    col_count = [0] * len(data[0])
    beams = {data[0].index('S')}
    col_count[data[0].index('S')] += 1

    for i in range(1, len(data)):

        new_beams = set()
        old_beams = set()

        row_splitters = [s for s in splitters if s[0] == i and s[1] in beams]

        if len(row_splitters) == 0:
            continue

        for spt in row_splitters:
            old_beams.add(spt[1])
            new_beams.add(spt[1] - 1)
            new_beams.add(spt[1] + 1)

            col_count[spt[1] - 1] += col_count[spt[1]]
            col_count[spt[1] + 1] += col_count[spt[1]]
            col_count[spt[1]] = 0
        
        beams = (beams | new_beams) - old_beams

    return sum(col_count)

def main(file_path: Path) -> None:
    
    with open(file_path, "r") as f:
        data = [line.strip() for line in f.readlines()]
    
    splitters = {
        (r, c)
        for r, line in enumerate(data)
        for c, ch in enumerate(line)
        if ch == "^"
    }

    print(f"Part 1: {part1(data, splitters)}")
    print(f"Part 2: {part2(data, splitters)}")

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
    
    