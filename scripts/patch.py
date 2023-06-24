import json
import os
import time


class Patch:
    def __init__(self, path, replace):
        self.path = path
        self.replace = replace

    def apply(self):
        os.system(f"krak2 dis {self.path}.class --out {self.path}.j")

        with open(f"{self.path}.j", "r") as readfile:
            filedata = readfile.read()
        for edit in self.replace:
            filedata = filedata.replace(edit[0], edit[1])
        with open(f"{self.path}.j", "w") as writefile:
            writefile.write(filedata)

        os.system(f"krak2 asm {self.path}.j --out {self.path}.class")


bfjarname = "bf.jar"
libjarname = "library-2.4.4.jar"
bf_patchlist = []
lib_patchlist = []

start = time.time()
print("Reading patch file...")
with open("../config/patch.json", "r") as readfile:
    patchjson = json.load(readfile)
    for patch in patchjson["bf_patches"]:
        print(f"Found {len(patchjson['bf_patches'][patch])} bf patches for {patch}...")
        bf_patchlist.append(Patch(path=patch, replace=patchjson["bf_patches"][patch]))
    for patch in patchjson["lib_patches"]:
        print(f"Found {len(patchjson['lib_patches'][patch])} lib patches for {patch}...")
        lib_patchlist.append(Patch(path=patch, replace=patchjson["lib_patches"][patch]))

print("Reading list of custom maps...")
with open("../config/patch.maps.json", "r") as readfile:
    patchjson = json.load(readfile)
    for game_type in patchjson["maps"]:
        schema = patchjson[game_type]
        patchstring = ""
        for n, game in enumerate(patchjson["maps"][game_type]):
            patchstring += schema[0].replace(schema[1], game)
            for line_remap in schema[2]:
                patchstring = patchstring.replace(line_remap[0], line_remap[1].replace("X", str(n)))
        print(f"Found {len(patchjson['maps'][game_type])} maps for gamemode {game_type}")
        bf_patchlist.append(Patch(path=patchjson["map_class"], replace=[[schema[0], patchstring]]))

print("Reading list of custom shop items...")
with open("../config/patch.shop.json", "r") as readfile:
    patchjson = json.load(readfile)
    schema = patchjson["schema"]
    patchstring = ""
    for n, item in enumerate(patchjson["items"]):
        patchstring += schema[0]\
            .replace(schema[1], item[0])\
            .replace(schema[2], item[1])
        for line_remap in schema[3]:
            patchstring = patchstring.replace(line_remap[0], line_remap[1].replace("X", str(n)))
    patchstring += schema[0]
    print(f"Found {len(patchjson['items'])} custom shop items")
    bf_patchlist.append(Patch(path=patchjson["shop_class"], replace=[[schema[0], patchstring]]))

print("Applying bf patches...")
for patch in bf_patchlist:
    print(f"Extracting {patch.path}...")
    os.system(f"jar xf ./{bfjarname} {patch.path}.class")
    print(f"Modifying {patch.path}...")
    patch.apply()
    os.system(f"jar uf ./{bfjarname} {patch.path}.class")

print("Extracting library...")
os.system(f"jar xf ./{bfjarname} META-INF/jarjar/{libjarname}")

print("Applying library patches...")
for patch in lib_patchlist:
    print(f"Extracting {patch.path}...")
    os.system(f"jar xf META-INF/jarjar/{libjarname} {patch.path}.class")
    print(f"Modifying {patch.path}...")
    patch.apply()
    os.system(f"jar uf META-INF/jarjar/{libjarname} {patch.path}.class")

print("Inserting library into jar...")
os.system(f"jar uf ./{bfjarname} META-INF/jarjar/{libjarname}")
end = time.time()
print(f"Done took {(end - start):.2f}s")
