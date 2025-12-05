from pathlib import Path
from argparse import ArgumentParser

def part1(ranges, fruits):
    return sum(
        1
        for fruit in fruits
        if any(low <= fruit <= high for (low, high) in ranges)
    )

def main(file_path: Path) -> None:
    with open(file_path, "r") as f:
        ranges, fruits = f.read().split("\n\n")

    ranges = [tuple(map(int, r.split("-"))) for r in ranges.split("\n")]
    fruits = [int(f) for f in fruits.split("\n")]
    
    print(f"Part 1: {part1(ranges, fruits)}")

    overlap_ranges = set()
    for ran in ranges:
        lb = ran[0]
        ub = ran[1]
        
        # current logic
        # there are 3 ways ranges can be merged
        # 1. if a new range swallows a range in its entirety, if it does then do that
        # 2. if the range lb and ub fits within other ranges, find max and min of those
        #    based on the lb and ub, add the new min and max as a range and get rid of 
        #    rest.
        # 3. lb fits in a lower range OR ub fits in an upper range. Find min or max
        #    respectively. For lb, merge the new low and ub from the range, and vice 
        #    versa for the ub.

        # implemented this all in sets, I think it reads very clearly. Probs far too
        # verbose.... ?
        swallow = {(low, high) for (low, high) in overlap_ranges if lb < low  and ub > high}
        lb_ranges = {(low, high) for (low, high) in overlap_ranges if low <= lb <= high}
        ub_ranges = {(low, high) for (low, high) in overlap_ranges if low <= ub <= high}

        if len(ub_ranges) == 0 and len(lb_ranges) == 0 and len(swallow) == 0:
            overlap_ranges.add(ran)

        elif len(swallow) != 0:
            overlap_ranges -= swallow
            overlap_ranges.add(ran)

        elif len(ub_ranges) != 0 and len(lb_ranges) != 0:

            # sets are unordered, im just using them because operations are faster
            # sorting sets turn them back into a list
            lowest_lb = min(ran[0] for ran in sorted(lb_ranges))
            highest_ub = max(ran[1] for ran in sorted(ub_ranges))

            # we now know what new range to put into the set
            # but we need to get rid of any ranges from the original
            # that are squashed into this
            overlap_ranges -= (ub_ranges | lb_ranges)
            overlap_ranges.add((lowest_lb, highest_ub))


        elif len(ub_ranges) != 0 and len(lb_ranges) == 0:
            highest_ub = max(ran[1] for ran in sorted(ub_ranges))
            overlap_ranges -= ub_ranges
            overlap_ranges.add((lb, highest_ub))

        elif len(ub_ranges) == 0 and len(lb_ranges) != 0:
            lowest_lb = min(ran[0] for ran in sorted(lb_ranges))
            overlap_ranges -= lb_ranges
            overlap_ranges.add((lowest_lb, ub))


    print(f"Part 2: {sum(ran[1]-ran[0]+1 for ran in overlap_ranges)}")

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
    
    