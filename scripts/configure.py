import json

with open("../config/properties.json","r") as readfile:
    properties = json.load(readfile)
with open("~/ServerInstance/server.properties", "rw") as rwfile:
    property_string = rwfile.read()
    for propertyy in properties:
        property_string.replace(propertyy[0], propertyy[1])
    rwfile.write(property_string)