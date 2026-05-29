from settings import *
from utils import *

import math

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
        "Starting Location Name": ["STRING"],
        "Generate Diagonal Rivers": ["BOOL"]
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

    print(startingLocation)
    print(biomes)