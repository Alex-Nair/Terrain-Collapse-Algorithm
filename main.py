from settings import *
from utils import *

if __name__ == "__main__":
    # Step 1 - Gather initial inputs (biomes, key locations, extra settings).
    biomeData, locationData = world_generation_menu()
    clear()
    settings = configure_settings({
        "Map Dimensions": ["INT", 10, 10000],
        "Maximum Blob Size": ["INT", 10, 10000],
        "Starting Location Name": ["STRING"],
        "Generate Diagonal Rivers": ["BOOL"]
    })

    print(biomeData, locationData, settings)