from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations

def part1(corners):
    return max(
        (abs(corner[0]-op_corn[0]) + 1) * (abs(corner[1] - op_corn[1]) + 1)
        for corner, op_corn in combinations(corners, 2)
    )

def get_polygon_border(corners):
    border = set()

    # zip statement creates a list connecting first to last
    # and bundles them into a list. It creates a polygon.
    for cor, op in zip(corners, corners[1:] + corners[:1]):
        
        #vertical
        if cor[0] == op[0]:
            y1, y2 = sorted([cor[1], op[1]])
            for y in range(y1, y2+1):
                border.add((cor[0], y))

        #horizontal
        if cor[1] == op[1]:
            x1, x2 = sorted([cor[0], op[0]])
            for x in range(x1, x2+1):
                border.add((x, cor[1]))
    
    return border

def fill_polygon(border):
    polygon_points = border.copy()

    min_x = 1e9
    min_y = 1e9

    for x, _ in border:
        min_x = x if x < min_x else min_x
    for y in [y for x, y in border if x == min_x]:
        min_y = y if y < min_y else min_y

    x, y = min_x + 1, min_y + 1
    directions = [
        (-1, 0),
        (1, 0),
        (0, 1),
        (0, -1)
    ]

    # given that we now have a point guaranteed to be inside
    # the polygon, we can do a search to fill in the polygon by looking
    # for empty spaces to fill.
    check = [(x + dx, y + dy) for dx, dy in directions]
    while len(check) > 0:
        x, y = check.pop()

        # border or already added, ignore
        if (x,y) in polygon_points:
            continue
        
        # as we are inside, add a point and add all directions
        polygon_points.add((x,y))
        for dx, dy in directions:
            check.append((x+dx, y+dy))

    return polygon_points

def square_in_polygon(polygon, x1, y1, x2, y2):
    x1, x2 = sorted([x1,x2])
    y1, y2 = sorted([y1,y2])

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if not (x, y) in polygon:
                return False
    return True


def main(file_path: Path) -> None:
    with open(file_path, "r") as f:
        data = [line.strip() for line in f.read().splitlines()]

    corners = [tuple(map(int, line.split(","))) for line in data]
    print(f"Part 1: {part1(corners)}")



    compressed_x, compressed_y = {}, {}
    uncomp_x, uncomp_y = {}, {}

    unique_xs = set([c[0] for c in corners])
    unique_ys = set([c[1] for c in corners])

    for i, x in enumerate(sorted(unique_xs)):
        compressed_x[x] = i*2
        uncomp_x[i*2] = x

    for i, y in enumerate(sorted(unique_ys)):
        compressed_y[y] = i*2
        uncomp_y[i*2] = y

    compressed_corners = [
        (compressed_x[corners[i][0]],compressed_y[corners[i][1]])
        for i in range(len(corners))
    ]

    compressed_border = get_polygon_border(compressed_corners)
    polygon = fill_polygon(compressed_border)

    biggest_area = 0
    for corner, op_corn in combinations(compressed_corners, 2):
        
        cor_comp_x, cor_comp_y = corner
        op_comp_x, op_comp_y = op_corn

        # reverse out of compressed space
        cor_x, cor_y = uncomp_x[cor_comp_x], uncomp_y[cor_comp_y]
        op_x, op_y = uncomp_x[op_comp_x], uncomp_y[op_comp_y]

        # check if the area is bigger than we have found
        # if it is, then we head back to check that all points exist
        # within the polygon in compressed space
        area = (abs(cor_x-op_x) + 1) * (abs(cor_y - op_y) + 1)
        if area > biggest_area:
            if square_in_polygon(polygon, cor_comp_x, cor_comp_y, op_comp_x, op_comp_y):
                biggest_area = area

    print(f"Part 2: {biggest_area}")




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
    
    