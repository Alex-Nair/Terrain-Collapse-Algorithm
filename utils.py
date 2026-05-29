import os
import msvcrt

# Global clear, should work on most OS types.
def clear():
    os.system("cls" if os.name == 'nt' else "clear")

# Global function, clears the input buffer to prevent keyboard from interfering with inputs.
def empty_buffer():
    while msvcrt.kbhit():
        msvcrt.getch()