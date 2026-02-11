from pathlib import Path
from argparse import ArgumentParser
import heapq

def euclid_distance(p, q):
    return (
        (p[0] - q[0])**2 + (p[1] - q[1])**2 + (p[2] - q[2])**2
    )**0.5


def main(file_path: Path) -> None:

    with open(file_path, "r") as f:
        data = [line.strip() for line in f.read().splitlines()]

    boxes = [tuple(map(int, line.split(","))) for line in data]

    heap = []
    for i, box in enumerate(boxes):
        for neigh in boxes[i+1:]:
            dist = euclid_distance(box, neigh)
            heapq.heappush(heap, (dist, {box, neigh}))


    circuits = []
    for c in range(10_000):

        # heappop will always give us the smallest distance first
        _, connection = heapq.heappop(heap)


        matches = []
        for idx, circuit in enumerate(circuits):
            if circuit & connection:
                matches.append(idx)

        # neither are in a circuit, so make a new circuit
        if len(matches) == 0:
            circuits.append(connection)

        # one of them is in a circuit, so union them to get all
        # elementss in each, i.e. adding to the bigger set
        elif len(matches) == 1:
            circuits[matches[0]] |= connection

        # they are both in circuits, in which case union with the first
        # and drop the second. Important that the second one gets popped out
        elif len(matches) == 2:
            circuits[matches[0]] |= circuits.pop(matches[1])

        if c == 1000 - 1:
            ans = sorted(circuits, key=len, reverse=True)
            print(f"Part 1: {len(ans[0]) * len(ans[1]) * len(ans[2])}")


        # if any of them are the length of the input then we 
        # have found our breaking condition
        if any(len(c) == len(boxes) for c in circuits):
            x, y = connection
            print(f"Part 2: {x[0] * y[0]}")
            break


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
    
    