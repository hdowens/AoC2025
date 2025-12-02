from pathlib import Path
from argparse import ArgumentParser

def part1(data):
    invalid_id_sum = 0
    for start, end in data:
        for num in range(int(start), int(end)+1):
            num = str(num)
            if num[:len(num) // 2] == num[len(num) // 2:]:
                invalid_id_sum += int(num)
    return invalid_id_sum

def part2_invalid(num):
    num = str(num)
    length = len(num)
    for i in range(1, (length // 2) + 1):
        if length % i == 0 and num[:i] * (length // i) == num:
            return True

    return False


def part2(data):
    invalid_id_sum = 0
    for start, end in data:
        for num in range(int(start), int(end)+1):
            if part2_invalid(num):
                invalid_id_sum += num
    return invalid_id_sum


def main(file_path: Path) -> None:
    
    with open(file_path, "r") as f:
        data = [ran.split("-") for ran in f.read().split(",")]

    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")

    


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
