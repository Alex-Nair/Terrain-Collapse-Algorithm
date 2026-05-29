import os
import msvcrt

# Global clear, should work on most OS types.
def clear():
    os.system("cls" if os.name == 'nt' else "clear")

# Global function, clears the input buffer to prevent keyboard from interfering with inputs.
def empty_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()

# Helper function, calculates manhattan distance between two points.
def calculate_distance(point1, point2, absolute = True):
    output = point2[0] + point2[1] - point1[0] - point1[1]
    return abs(output) if absolute else output