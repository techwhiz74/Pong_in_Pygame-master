import pygame
import sys

def education_screen():
    pygame.init()

    screen_width = 1280
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Phishing Awareness Education')

    bg_color = pygame.Color('#2F373F')
    text_color = (200, 200, 200)
    font = pygame.font.Font(None, 36)

    # Education content
    education_content = [
        "How to Spot a Phishing Attack:",
        "",
        "1. Check the sender's email address. Look for slight misspellings.",
        "2. Hover over links to see the actual URL. Phishing links often look similar to real ones.",
        "3. Look for spelling and grammar mistakes.",
        "4. Be cautious of urgent or threatening language.",
        "5. Verify requests for personal information. Legitimate companies rarely ask for this via email.",
        "6. Don't download attachments from unknown senders.",
        "7. Use two-factor authentication whenever possible.",
        "8. Keep your software and antivirus up to date."
    ]

    click = False
    while True:
        screen.fill(bg_color)

        # Display education content
        for i, line in enumerate(education_content):
            text = font.render(line, True, text_color)
            screen.blit(text, (50, 50 + i * 40))

        # Draw 'Back' button
        draw_text('Back', font, text_color, screen, screen_width // 2, screen_height - 100)

        mx, my = pygame.mouse.get_pos()
        back_button = pygame.Rect(screen_width // 2 - 50, screen_height - 130, 100, 50)

        if back_button.collidepoint((mx, my)):
            if click:
                return  # Return to main menu or previous screen

        pygame.draw.rect(screen, text_color, back_button, 2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
