import keyboard
import os
import msvcrt

biomes = {}
keyLocations = {}

# Global clear, should work on most OS types.
def clear():
    os.system("cls" if os.name == 'nt' else "clear")

# Global function, clears the input buffer to prevent keyboard from interfering with inputs.
def empty_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()

def world_generation_menu():
    global biomes, keyLocations

    def wait_for_key_release():
        while any(keyboard.is_pressed(k) for k in ("up", "down", "enter")):
            pass

    def menu(title, options):
        selected = 0

        clearScreen = True
        buffer = True

        while True:
            if clearScreen:
                clear()
                clearScreen = False

                print(f"=== {title} ===\n")

                for i, option in enumerate(options):
                    prefix = "►" if i == selected else " "
                    print(f"{prefix} {option}")

            if keyboard.is_pressed("up") and not buffer:
                while True:
                    selected = (selected - 1) % len(options)

                    if options[selected] != "":
                        break
                
                clearScreen = True
                buffer = True

            elif keyboard.is_pressed("down") and not buffer:
                while True:
                    selected = (selected + 1) % len(options)

                    if options[selected] != "":
                        break

                clearScreen = True
                buffer = True

            elif keyboard.is_pressed("enter") and not buffer:
                wait_for_key_release()
                empty_buffer()
                return selected
            
            elif not(keyboard.is_pressed("up") or keyboard.is_pressed("down") or keyboard.is_pressed("enter")):
                buffer = False

    def pause(message="\nPress ENTER to continue..."):
        input(message)

    def get_nonempty_name(prompt, existing_names):
        while True:
            name = input(prompt).strip()

            if not name:
                print("Name cannot be empty.")
                continue

            if name in existing_names:
                print("That name already exists.")
                continue

            return name

    def get_int(prompt, minimum=None, maximum=None):
        while True:
            try:
                value = int(input(prompt))

                if minimum is not None and value < minimum:
                    print(f"Value must be at least {minimum}.")
                    continue

                if maximum is not None and value > maximum:
                    print(f"Value must be at most {maximum}.")
                    continue

                return value

            except ValueError:
                print("Please enter a valid integer.")

    def get_rgb(existing=None):
        if existing:
            print(f"Current RGB: {existing}")

        r = get_int("R (0-255): ", 0, 255)
        g = get_int("G (0-255): ", 0, 255)
        b = get_int("B (0-255): ", 0, 255)

        return [r, g, b]

    def choose_entry(data, title):
        if not data:
            clear()
            print(f"No {title.lower()} available.")
            pause()
            return None

        names = list(data.keys())
        selection = menu(f"Select {title}", names + ["Back"])

        if selection == len(names):
            return None

        return names[selection]

    def add_biome():
        clear()

        name = get_nonempty_name(
            "Biome name: ",
            biomes.keys()
        )

        frequency = get_int("Frequency: ", 0)
        min_distance = get_int("Minimum distance: ", 0)

        print("\nRGB Colour:")
        colour = get_rgb()

        biomes[name] = [
            frequency,
            min_distance,
            colour
        ]

    def add_location():
        clear()

        name = get_nonempty_name(
            "Location name: ",
            keyLocations.keys()
        )

        min_distance = get_int(
            "Minimum distance: ",
            0
        )

        print("\nRGB Colour:")
        colour = get_rgb()

        keyLocations[name] = [
            min_distance,
            colour
        ]

    def edit_biome():
        name = choose_entry(biomes, "Biome")
        if not name:
            return

        while True:
            biome = biomes[name]

            choice = menu(
                f"Edit Biome: {name}",
                [
                    f"Frequency ({biome[0]})",
                    f"Minimum Distance ({biome[1]})",
                    f"RGB Colour ({biome[2]})",
                    "Rename",
                    "Back"
                ]
            )

            if choice == 0:
                clear()
                biome[0] = get_int(
                    "New frequency: ",
                    0
                )

            elif choice == 1:
                clear()
                biome[1] = get_int(
                    "New minimum distance: ",
                    0
                )

            elif choice == 2:
                clear()
                biome[2] = get_rgb(biome[2])

            elif choice == 3:
                clear()

                new_name = get_nonempty_name(
                    "New name: ",
                    [n for n in biomes if n != name]
                )

                biomes[new_name] = biomes.pop(name)
                name = new_name

            else:
                return

    def edit_location():
        name = choose_entry(
            keyLocations,
            "Location"
        )

        if not name:
            return

        while True:
            location = keyLocations[name]

            choice = menu(
                f"Edit Location: {name}",
                [
                    f"Minimum Distance ({location[0]})",
                    f"RGB Colour ({location[1]})",
                    "Rename",
                    "Back"
                ]
            )

            if choice == 0:
                clear()
                location[0] = get_int(
                    "New minimum distance: ",
                    0
                )

            elif choice == 1:
                clear()
                location[1] = get_rgb(location[1])

            elif choice == 2:
                clear()

                new_name = get_nonempty_name(
                    "New name: ",
                    [n for n in keyLocations if n != name]
                )

                keyLocations[new_name] = keyLocations.pop(name)
                name = new_name

            else:
                return

    def remove_biome():
        name = choose_entry(biomes, "Biome")
        if name:
            del biomes[name]

    def remove_location():
        name = choose_entry(
            keyLocations,
            "Location"
        )

        if name:
            del keyLocations[name]

    isDone = False
    while not isDone:
        choice = menu(
            "World Generation Settings",
            [
                f"Add Biome ({len(biomes)})",
                "Edit Biome",
                "Remove Biome",
                "",
                f"Add Key Location ({len(keyLocations)})",
                "Edit Key Location",
                "Remove Key Location",
                "",
                "Finish"
            ]
        )

        match choice:
            case 0:
                add_biome()
            
            case 1:
                edit_biome()
            
            case 2:
                remove_biome()
            
            case 4:
                add_location()
            
            case 5:
                edit_location()
            
            case 6:
                remove_location()
            
            case 8:
                isDone = True


def configure_settings(settings):
    """
    settings format:

    {
        "World Width": ["INT", 100, 10000],
        "World Name": ["STRING"],
        "Generate Rivers": ["BOOL"]
    }
    """

    values = {}

    for setting_name, setting_data in settings.items():

        setting_type = setting_data[0]

        while True:

            try:

                if setting_type == "INT":

                    minimum = setting_data[1]
                    maximum = setting_data[2]

                    value = int(
                        input(
                            f"{setting_name} ({minimum}-{maximum}): "
                        )
                    )

                    if minimum <= value <= maximum:
                        values[setting_name] = value
                        break

                    print(
                        f"Please enter a value between "
                        f"{minimum} and {maximum}."
                    )

                elif setting_type == "STRING":

                    value = input(
                        f"{setting_name}: "
                    )

                    values[setting_name] = value
                    break

                elif setting_type == "BOOL":

                    value = input(
                        f"{setting_name} (True/False): "
                    ).strip().lower()

                    if value in (
                        "true",
                        "t",
                        "yes",
                        "y",
                        "1"
                    ):
                        values[setting_name] = True
                        break

                    elif value in (
                        "false",
                        "f",
                        "no",
                        "n",
                        "0"
                    ):
                        values[setting_name] = False
                        break

                    print(
                        "Please enter True or False."
                    )

                else:

                    print(
                        f"Unknown setting type: "
                        f"{setting_type}"
                    )

                    break

            except ValueError:

                print(
                    "Invalid input. Please try again."
                )

    return values

# Testing Purposes Only
world_generation_menu()

clear()

settings = configure_settings({
    "World Width:": ["INT", 10, 10000],
    "World Name": ["STRING"],
    "Generate Rivers": ["BOOL"]
})

print(settings)