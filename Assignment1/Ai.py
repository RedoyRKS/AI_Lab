from heapq import heapify, heappop, heappush
import math
import csv
from collections import defaultdict

COORDINATES_FILE = "Assignment1\Coordinates.csv"
DISTANCE_FILE = "Assignment1\distances.csv"

x_points = []
y_points = []
z_points = []
stars = []


def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


coordinates = {}
adjacency_list = defaultdict(list)


with open(COORDINATES_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for star_name, x, y, z in reader:
        stars.append(star_name)
        x_points.append(int(x))
        y_points.append(int(y))
        z_points.append((int(z)))
        coordinates[star_name] = (int(x), int(y), int(z))

with open(DISTANCE_FILE, "r") as file:
    reader = csv.reader(file)
    for source, destination, dist in reader:
        adjacency_list[source].append((destination, int(dist)))

SOURCE_STAR = "TRAPPIST-1"
DESTINATION_STAR = "55 Cancri"
# DESTINATION_STAR = "Upsilon Andromedae"


def checkNum(enteredVal):
    match enteredVal:
        case "1":
            return True
        case "2":
            return False


print("Which algorithm you want to use for seaerch?\n")
print("1. Dijkstra's algorithm")
print("2. A* algorithm\n")
enteredVal = int(input("Your Answer: "))

DIJKSTRA = checkNum(enteredVal)
print(f"From {SOURCE_STAR} to {DESTINATION_STAR}")

priority_queue = [(0, SOURCE_STAR, None, 0)]
visited = set()
parent_map = {}

while priority_queue:
    key, current_star, parent, path_distance_from_src = heappop(priority_queue)

    if current_star in visited:
        continue

    parent_map[current_star] = parent

    if current_star == DESTINATION_STAR:
        print("The distance is " + str(path_distance_from_src))
        break
    visited.add(current_star)

    for neigborstar_name, neigborstar_distance in adjacency_list[current_star]:

        new_path_distance_from_src = path_distance_from_src + neigborstar_distance

        if DIJKSTRA:
            heappush(priority_queue, (new_path_distance_from_src,
                     neigborstar_name, current_star, new_path_distance_from_src))

        else:
            heappush(priority_queue, (new_path_distance_from_src + distance(
                *coordinates[neigborstar_name], *coordinates[DESTINATION_STAR]), neigborstar_name, current_star, new_path_distance_from_src))
