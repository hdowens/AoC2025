from pathlib import Path
from argparse import ArgumentParser

def part1(data):
    dial = 50
    z_count = 0
    for instr in data:
        sign = instr[0]
        num = instr[1:]
        
        if sign == "L":
            dial = (dial - int(num)) % 100
        elif sign == "R":
            dial = (dial + int(num)) % 100

        if dial == 0:
            z_count +=1 

    return z_count

def part2(data):
    dial = 50
    z_count_p2 = 0
    for instr in data:
        sign = instr[0]
        num = int(instr[1:])

        # brute force :)
        # smarter solution below.. 
        for _ in range(num):
            if sign == "L":
                dial = (dial - 1) % 100

            elif sign == "R":
                dial = (dial + 1) % 100

            if dial == 0:
                z_count_p2 += 1

    return z_count_p2    

def main(file_path: Path) -> None:

    with open(file_path, "r") as f:
        data = [l.strip() for l in f.readlines()]

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
    


"""   

    This is the proper solution, I spent so long on trying to get this modulus maths to work
    and eventually gave up and brute forces lol. I knew for the positive direction 
    it would just be // 100 every time but I could not figure out what to do for the 
    negative direction, and the ring theory I learnt at uni did not come back quickly.... 

    A solution I found online and then implemented in my own codebase is the following. It is 
    as explained but for the negative direction you can swap the sign of the dial. An identity
    of modulus is: 100 − x ≡ −x (mod 100) . Since for the number of times we cross 0 it doesnt
    actually matter the direction we are going in, if we can find the equivalent to go right
    then we can use the same counting strategy as the RHS turns. 

    So, the dial is (100-dial)%100 and you get the swapped dial. Then you can just add your 
    turns and integer divide by 100 again. Much more elegant!

    dial = 50
    z_count_p2 = 0
    for instr in data:
        sign = instr[0]
        num = int(instr[1:])
        
        if sign == "L":
            swapped_dial = (100-dial)%100
            z_count_p2 += (swapped_dial + num) // 100
            dial = (dial - num) % 100

        elif sign == "R":
            z_count_p2 += (dial + num) // 100
            dial = (dial + num) % 100

        print(f"Instr: {instr}, z_count: {z_count_p2}")
        
    print(z_count_p2)

    
    Another cool solution was that someone used collections.deque, as in that library there is a 
    rotate function, which literally does what the dial is doing, and supports negative too.

"""