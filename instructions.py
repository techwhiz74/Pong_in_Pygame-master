import pygame
import sys

pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Instructions')

# Colors and fonts
light_grey = (200, 200, 200)
font = pygame.font.Font(None, 36)

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

# Instructions function
def show_instructions():
    instructions = [
        "Welcome to the interactive phishing awareness game designed for university students.",
        "In this engaging experience, you'll learn how to identify and protect yourself against",
        "phishing attacks commonly encountered in your digital life.",
        "",
        "Before we dive into the game, let's take a moment to understand the basics.",
        "Phishing is a malicious attempt to deceive individuals into providing sensitive",
        "information such as usernames, passwords, and credit card details by",
        "disguising as a trustworthy entity in electronic communication.",
        "",
        "This game consists of several scenarios, each representing a different phishing attack.",
        "Your task is to navigate through these scenarios, make decisions, and identify whether",
        "the situation is legitimate or a phishing attempt.",
        "By participating in this game, you'll develop critical thinking skills and enhance your",
        "ability to spot suspicious emails.",
        "",
        "Press any key to continue..."
    ]
    while True:
        screen.fill((0, 0, 0))
        y = 50
        for line in instructions:
            draw_text(line, font, light_grey, screen, 50, y)
            y += 40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # Exit instructions and start the game

        pygame.display.update()
        pygame.time.Clock().tick(60)
