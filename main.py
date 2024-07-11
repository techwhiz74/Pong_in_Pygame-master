
import pygame
import sys
from home_menu import home_menu
from instructions import show_instructions
from game import main_game

def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Error initializing mixer: {e}")

    try:
        pygame.font.init()
    except pygame.error as e:
        print(f"Error initializing font: {e}")

    # Call the home menu
    home_menu()

    # Show the instructions
    show_instructions()

    # Start the main game loop
    main_game()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
