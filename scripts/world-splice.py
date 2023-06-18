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


def search_for_relocatable(parent):
    for tag in parent:
        if isinstance(tag["data"], list):
            search_for_relocatable(tag["data"])
        if "X" in tag["tag"]:
            tag["data"]["value"] += (row * largest_edge * 16 - built_map.cords[0] * 16)
        if "Z" in tag["tag"] and not "Zone" in tag["tag"]:
            tag["data"]["value"] += (col * largest_edge * 16 - built_map.cords[1] * 16)


def search_for_renamable(parent, tag_name, replace):
    for tag in parent:
        if isinstance(tag["data"], list):
            search_for_renamable(tag["data"], tag_name, replace)
        if tag["tag"] == tag_name:
            tag["data"]["value"] = replace


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

shutil.rmtree("./tmp/world", True)
shutil.rmtree("./tmp/assets", True)
shutil.copytree("./world_template", "./tmp/world")
os.makedirs("./tmp/assets/maps")
os.mkdir("./tmp/assets/games")

map_rotation = {}

for i, built_map in enumerate(built_maps):
    if not built_map.private:
        if built_map.mode not in map_rotation:
            map_rotation[built_map.mode] = []
        map_rotation[built_map.mode].append(built_map.name)
    row, col = convert_index_to_2d(i, int(sqrt(len(built_maps))))
    os.system(f"minecraft-world-splicer"
              f" --source-world=worlds/{built_map.world_path}"
              f" --source-x={built_map.cords[0]} --source-z={built_map.cords[1]}"
              f" --source-width={built_map.cords[2]} --source-height={built_map.cords[3]}"
              f" --target-world=tmp/world"
              f" --target-x={row * largest_edge} --target-z={col * largest_edge}")
    with open(f"games_and_maps/{built_map.name}.json", "r") as readfile:
        map_json = json.load(readfile)
        if built_map.private:
            search_for_renamable(map_json, "name", f"{built_map.name}-Private")
    with open(f"tmp/assets/maps/{built_map.name}{'-Private' if built_map.private else ''}.json", "w") as writefile:
        json.dump(map_json, writefile)
    with open(f"games_and_maps/{built_map.mode}_{built_map.name.lower()}.json") as readfile:
        game_json = json.load(readfile)
        search_for_relocatable(game_json)
        if built_map.private:
            search_for_renamable(game_json, "name", f"{built_map.mode}_{built_map.name.lower()}{'_private' if built_map.private else ''}")
            search_for_renamable(game_json, "map", f"{built_map.name}-Private")
    with open(
            f"tmp/assets/games/{built_map.mode}_{built_map.name.lower()}{'_private' if built_map.private else ''}.json",
            "w") as writefile:
        json.dump(game_json, writefile)
with open("../config/patch.maps.json", "r") as readfile:
    map_json = json.load(readfile)
    map_json["maps"] = map_rotation
with open("../config/patch.maps.json", "w") as writefile:
    json.dump(map_json, writefile)
