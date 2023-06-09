import json

with open("../config/properties.json", "r") as readfile:
    properties = json.load(readfile)
with open("~/ServerInstance/server.properties", "r") as readfile:
    property_string = readfile.read()
    for propertyy in properties:
        property_string.replace(propertyy[0], propertyy[1])
with open("~/ServerInstance/server.properties", "w") as writefile:
    writefile.write(property_string)