import json
import os
import shutil
from math import sqrt


class Map:
    def __init__(self, name, mode, private, world_path, cords):
        self.name = name
        self.mode = mode
        self.private = private
        self.world_path = world_path
        self.cords = cords


def convert_index_to_2d(index, num_columns):
    int_row = index // num_columns
    int_col = index % num_columns
    return int_row, int_col


with open("maps.json", "r") as readfile:
    raw_maps = json.load(readfile)

built_maps = []
largest_edge = 0

for raw_map in raw_maps:
    largest_edge = max(largest_edge, max(raw_map["world"]["cords"][2], raw_map["world"]["cords"][3]))
    for game_mode in raw_map["modes"]:
        built_maps.append(Map(raw_map["name"], game_mode, False, raw_map["world"]["name"], raw_map["world"]["cords"]))
        built_maps.append(Map(raw_map["name"], game_mode, True, raw_map["world"]["name"], raw_map["world"]["cords"]))

largest_edge += 10

shutil.rmtree("./tmp/world")
shutil.rmtree("./tmp/assets")
shutil.copytree("./world_template", "./tmp/world")
os.mkdir("./tmp/assets")

for i, built_map in enumerate(built_maps):
    row, col = convert_index_to_2d(i, int(sqrt(len(built_maps))))
    os.system(f"minecraft-world-splicer"
              f" --source-world=worlds/{built_map.world_path}"
              f" --source-x={built_map.cords[0]} --source-z={built_map.cords[1]}"
              f" --source-width={built_map.cords[2]} --source-height={built_map.cords[3]}"
              f" --target-world=tmp/world"
              f" --target-x={row * largest_edge} --target-z={col * largest_edge}")


print("Debug")
