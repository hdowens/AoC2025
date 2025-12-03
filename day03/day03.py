from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations

def main(file_path: Path) -> None:
    
    with open(file_path, "r") as f:
        data = [l.strip() for l in f.readlines()]


    # seems like its the largest two digit number you can make from 
    # consecutive digits? -> combinations

    print("Part 1: ", end="")
    print(sum(
        max([int(''.join(i)) for i in combinations(rating, 2)])
        for rating in data
    ))

    # cant brute force part 2 :(
    tot = 0
    str_len_wanted = 12
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

            elif len(potent) + (len(rating) - found) >= str_len_wanted:
                if len(potent) < str_len_wanted:
                    potent += rating[found]
                    rating = rating[found+1:]
                    max_dig = 9
                else:
                    max_dig -= 1
            else:
                max_dig -= 1

        #print(f"{potent}")
        tot += int(potent) 

    print(f"Tot: {tot}")

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
    
    