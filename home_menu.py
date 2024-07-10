import pygame
import sys
from education_screen import education_screen

pygame.init()
# pygame.mixer.init()
# # Screen dimensions
# screen_width = 1280
# screen_height = 960
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption('Phishing Awareness Ping Pong')

# # Load background image and music
# background_image = pygame.image.load('HomeScreenImage.png')
# pygame.mixer.music.load('home_music.mp3')
# pygame.mixer.music.play(-1)

# # Colors and fonts
# light_grey = (200, 200, 200)
# font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
# pygame.init()
# pygame.mixer.init()

# Screen dimensions
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Phishing Awareness Ping Pong')

# Load background image
background_image = pygame.image.load('HomeScreenImage.png')

# Load and play music
try:
    pygame.mixer.music.load('home_music.mp3')
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}")

# Colors and fonts
light_grey = (200, 200, 200)
try:
    font = pygame.font.Font(None, 74)
except pygame.error as e:
    print(f"Error loading music: {e}")

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Main menu function
def home_menu():
    click = False
    while True:
        screen.blit(pygame.transform.scale(background_image, (screen_width, screen_height)), (0, 0))
        draw_text('Phishing Awareness Ping Pong', font, light_grey, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text('Start', small_font, light_grey, screen, screen_width // 2, screen_height // 2)
        draw_text('Education', small_font, light_grey, screen, screen_width // 2, screen_height // 2 + 60)
        draw_text('Quit', small_font, light_grey, screen, screen_width // 2, screen_height // 2 + 120)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50)
        button_2 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 35, 200, 50)
        button_3 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 95, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                pygame.mixer.music.stop()
                return  # Return to main to start the game
        if button_2.collidepoint((mx, my)):
            if click:
                education_screen()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, light_grey, button_1, 2)
        pygame.draw.rect(screen, light_grey, button_2, 2)
        pygame.draw.rect(screen, light_grey, button_3, 2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        pygame.time.Clock().tick(60)
