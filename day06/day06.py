from pathlib import Path
from argparse import ArgumentParser
from functools import reduce

def part1(data):
    tot = 0
    for problem in zip(*data):
        if problem[-1] == "+":
            tot += sum(map(int, problem[:-1]))
        elif problem[-1] == "*":
            tot += reduce(lambda x, y: x * y, map(int, problem[:-1]))
    return tot

def main(file_path: Path) -> None:
    with open(file_path, "r") as f:
        data = [line for line in f.readlines()]

    print(f"Part 1: {part1([d.strip().split() for d in data])}")

    rows = [row.replace("\n", "")[::-1] for row in data]

    tot = 0
    tmp_list = []
    for i in range(len(rows[0])):
        nums = [rows[i] for rows in rows[:-1]]

        if i == len(rows[0])-1:
            tmp_list.append(int(''.join(i for i in nums)))
            operator = rows[-1][i]
            match operator:
                case '+':
                    tot += sum(tmp_list)
                case '*':
                    tot += reduce(lambda x, y: x * y, tmp_list)

        if all(n == ' ' for n in nums):
            operator = rows[-1][i-1]
            match operator:
                case '+':
                    tot += sum(tmp_list)
                case '*':
                    tot += reduce(lambda x, y: x * y, tmp_list)
            tmp_list = []

        else:
            tmp_list.append(int(''.join(i for i in nums)))


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
    
    