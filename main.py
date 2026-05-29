from settings import *
from utils import *

import math
import random
import json

if __name__ == "__main__":
    # Step 1 - Gather initial inputs (biomes, key locations, extra settings).
    while True:
        biomeData, locationData = world_generation_menu()

        if len(biomeData.keys()) > 0:
            break


    clear()
    settings = configure_settings({
        "Map Dimensions": ["INT", 10, 10000],
        "Maximum Blob Size": ["INT", 10, 10000],
        "Starting Location Name": ["STRING"]
    })

    # Step 2 - Set up initial parameters, primarily those being the biomes as well as where the starting location will be.
    clear()
    print("Generating initial settings...")

    map = [[None for _ in range(settings["Map Dimensions"])] for _ in range(settings["Map Dimensions"])]

    biomes = {}
    totalFrequency = sum([biome[0] for biome in biomeData.values()])

    for biome in biomeData.keys():
        data = biomeData[biome]

        biomes[biome] = {
            "Amount": math.ceil(settings["Map Dimensions"]**2 * (data[0] / totalFrequency)),
            "Frequency": data[0],
            "Minimum Distance": data[1],
            "RGB": data[2]
        }
    
    startingLocation = [math.floor(settings["Map Dimensions"] / 2) for _ in range(2)]

    # Step 3 - Start by placing blobs across the map, being fair as to ensure that each biome apperas at least once on the map (in most scenarios)
    print("Creating blob map...")

    validSpaces = []
    for i in range(settings["Map Dimensions"]):
        for j in range(settings["Map Dimensions"]):
            validSpaces.append([i, j])
    
    currentBiomeIndex = 0

    while sum(biomes[biome]["Amount"] for biome in biomes.keys()) > 0 and len(validSpaces) > 0:
        chosenBiome = list(biomes.keys())[currentBiomeIndex]
        data = biomes[chosenBiome]

        if data["Amount"] > 0:
            # Select a valid space that is far enough away.
            validBiomeSpaces = validSpaces[:]
            chosenSpace = None

            while len(validBiomeSpaces) > 0 and chosenSpace == None:
                chosenSpace = random.choice(validBiomeSpaces)

                if calculate_distance(startingLocation, chosenSpace) < data["Minimum Distance"]:
                    validBiomeSpaces.remove(chosenSpace)
                    chosenSpace = None
            
            if chosenSpace != None:
                reviewSpaces = [chosenSpace[:]]

                # Found a space, so start generating from it.
                spacesToPlace = random.choice(range(9, settings["Maximum Blob Size"])) - 1

                def find_expansion_spaces(origin):
                    spaces = []
                    
                    for direction in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                        newLocation = [origin[0] + direction[0], origin[1] + direction[1]]

                        if 0 <= newLocation[0] <= settings["Map Dimensions"] - 1 and 0 <= newLocation[1] <= settings["Map Dimensions"] - 1 and calculate_distance(startingLocation, newLocation) >= data["Minimum Distance"]:
                            spaces.append(newLocation)
                    
                    return spaces

                expansionSpaces = find_expansion_spaces(chosenSpace)

                while len(expansionSpaces) > 0 and spacesToPlace > 0 and biomes[chosenBiome]["Amount"] > 0:
                    spacesToPlace -= 1
                    biomes[chosenBiome]["Amount"] -= 1

                    targetSpace = random.choice(expansionSpaces)

                    map[targetSpace[0]][targetSpace[1]] = [chosenBiome, data["RGB"]]
                    
                    expansionSpaces.remove(targetSpace)
                    reviewSpaces.append(targetSpace[:])

                    newSpaces = find_expansion_spaces(targetSpace)

                    for space in newSpaces:
                        if not space in expansionSpaces and map[space[0]][space[1]] == None:
                            expansionSpaces.append(space)
                    
                # Invalidate any spaces we passed over.
                for space in reviewSpaces:
                    if space in validSpaces:
                        validSpaces.remove(space)

            else:
                # This biome can no longer be placed on the map, so get rid of it.
                biomes[chosenBiome]["Amount"] = 0
        
        currentBiomeIndex = (currentBiomeIndex + 1) % len(biomes.keys())
    
    # As a failsafe, fill in any empty spaces with the first biome.
    print("Filling in holes...")

    defaultBiome = list(biomes.keys())[0]
    data = biomes[defaultBiome]

    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == None:
                map[row][col] = [defaultBiome, data["RGB"]]
    
    # Step 4 - Place the starting location as well as every other key location.
    print("Placing starting and key locations...")

    map[startingLocation[0]][startingLocation[1]] = [settings["Starting Location Name"], [255, 255, 255]]

    takenSpaces = []

    for keyLocation in locationData.keys():
        data = locationData[keyLocation]

        chosenSpace = None

        while chosenSpace == None:
            chosenSpace = [random.choice(range(0, settings["Map Dimensions"] - 1)), random.choice(range(0, settings["Map Dimensions"] - 1))]

            if chosenSpace in takenSpaces or calculate_distance(chosenSpace, startingLocation) < data[0]:
                chosenSpace = None
            
            else:
                takenSpaces.append(chosenSpace[:])
    
        map[chosenSpace[0]][chosenSpace[1]] = [keyLocation, data[1]]
    
    # Step 5 - Export the final map to JSON.
    with open("map.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "size": len(map[0]),
                "tiles": map
            },
            file,
            indent=4
        )