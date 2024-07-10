import pygame
import sys
import random
import csv


class Button:
    def __init__(self, x, y, width, height, text, font, callback, toggle=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.color = (100, 200, 255)
        self.text_color = (0, 0, 0)
        self.toggle = toggle
        self.toggled = False  # To keep track of toggle state


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                if self.toggle:
                    self.toggled = not self.toggled  # Toggle the state
                    self.text = "Play" if self.toggled else "Pause"

class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, size=(100, 30)):
        super().__init__()
        if path:
            self.image = pygame.image.load(path).convert_alpha()
        else:
            self.image = pygame.Surface(size)
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, link_group=None):
        self.rect.y += self.movement
        self.screen_constrain()

class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, link_group):
        if self.rect.top < link_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > link_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

class LegitimateLink(Block):
    def __init__(self, text, x_pos, y_pos, speed_x, speed_y, paddles, link_type, sounds, fonts, screen_dimensions, screen, email_links):
        super().__init__(None, x_pos, y_pos, size=(50, 15))
        self.font = fonts['basic_font']
        self.text = str(text)
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0
        self.link_type = link_type
        self.email_links = email_links
        self.paused = False
        self.screen_width, self.screen_height = screen_dimensions
        self.screen = screen

        self.plob_sound = sounds['plob_sound']
        self.score_sound = sounds['score_sound']

    def update(self):
        if not self.paused:
            if self.active:
                self.rect.x += self.speed_x
                self.rect.y += self.speed_y
                self.collisions()
            else:
                self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            pygame.mixer.Sound.play(self.plob_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(self.plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0]
            if abs(self.rect.right - collision_paddle.rect.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.rect.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.rect.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.rect.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.rect.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.rect.top
                self.speed_y *= -1

    def reset_link(self, text, link_type):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (self.screen_width / 2, self.screen_height / 2)
        pygame.mixer.Sound.play(self.score_sound)
        self.text = str(text)
        self.link_type = link_type
        self.image = self.font.render(self.text, True, (255, 255, 255))

    def restart_counter(self):
        if not self.paused:
            current_time = pygame.time.get_ticks()
            countdown_number = 5  # Start countdown from 5

            if current_time - self.score_time <= 1000:
                countdown_number = 5
            if 1000 < current_time - self.score_time <= 2000:
                countdown_number = 4
            if 2000 < current_time - self.score_time <= 3000:
                countdown_number = 3
            if 3000 < current_time - self.score_time <= 4000:
                countdown_number = 2
            if 4000 < current_time - self.score_time <= 5000:
                countdown_number = 1
            if current_time - self.score_time > 5000:
                self.active = True

            time_counter = self.font.render(str(countdown_number), True, (255, 255, 255))
            time_counter_rect = time_counter.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

            rect_width = 70  # Width of the rectangle
            rect_height = 50  # Height of the rectangle
            background_rect = pygame.Rect(0, 0, rect_width, rect_height)
            background_rect.center = (self.screen_width / 2, self.screen_height / 2 - 50)

            pygame.draw.rect(self.screen, (0, 0, 0), background_rect)
            self.screen.blit(time_counter, time_counter.get_rect(center=background_rect.center))

    def check_off_screen(self):
        chosen_link = random.choice(self.email_links)
        self.reset_link(chosen_link['domain'], 'phishing' if chosen_link['label'] == '1' else 'legitimate')
        
class GameManager:
    def __init__(self, link_group, paddle_group, email_links):
        self.player_score = 0
        self.opponent_score = 0
        self.link_group = link_group
        self.paddle_group = paddle_group
        self.email_links = email_links

    def run_game(self, update=True):
        if update:
            self.paddle_group.draw(screen)
            self.link_group.draw(screen)
            self.check_off_screen()

        self.paddle_group.update(self.link_group)
        self.link_group.update()
        
        self.draw_score()
    
    def draw_game_state(self):
        # Draw all game elements without updating
        self.run_game(update=False)

    def check_off_screen(self):
        if self.link_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            chosen_link = random.choice(self.email_links)
            self.link_group.sprite.reset_link(chosen_link['domain'], 'phishing' if chosen_link['label'] == '1' else 'legitimate')
        if self.link_group.sprite.rect.left <= 0:
            self.player_score += 1
            chosen_link = random.choice(self.email_links)
            self.link_group.sprite.reset_link(chosen_link['domain'], 'phishing' if chosen_link['label'] == '1' else 'legitimate')

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, 40 ))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, 40))

        pygame.draw.rect(screen, (0, 0, 0), player_score_rect.inflate(20, 10))  # Inflate for padding
        pygame.draw.rect(screen, (0, 0, 0), opponent_score_rect.inflate(20, 10))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

def extract_links_from_csv(filename):
    links = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            links.append({'domain': row['domain'], 'label': row['label']})
    return links

def main_game():
    # General setup
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    clock = pygame.time.Clock()

    # Main Window
    global screen, screen_width, screen_height, basic_font, plob_sound, score_sound, middle_strip, bg_color, accent_color
    screen_width = 1280
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Phishing Awareness Ping Pong')

    #create restart button
    font = pygame.font.Font('freesansbold.ttf', 32)
    button_width = 140
    button_height = 60
    restart_button = Button(screen_width - button_width -30, 30, button_width, button_height, "Restart", font, restart_game)
    
    running = True

    paused = False  

    def toggle_pause_play():
        nonlocal paused
        paused = not paused
        for link in link_group:
            link.paused = paused  # Assuming link_group contains LegitimateLink objects
    
    #create pause and
    pause_button = Button(30, 30, button_width, button_height, "Pause", font, toggle_pause_play, toggle=True)

    global link_group, paddle_group  # Declare them global if they are modified globally
    link_group = pygame.sprite.Group()
    paddle_group = pygame.sprite.Group()

    # Global Variables
    bg_color = pygame.Color('#2F373F')
    accent_color = (27, 35, 43)
    basic_font = pygame.font.Font('freesansbold.ttf', 32)
    plob_sound = pygame.mixer.Sound("pong.ogg")
    score_sound = pygame.mixer.Sound("score.ogg")
    middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

    sounds = {
        'plob_sound': plob_sound,
        'score_sound': score_sound
    }

    fonts = {
        'basic_font': basic_font
    }

    screen_dimensions = (screen_width, screen_height)
    links = extract_links_from_csv('phishing_links.csv')
    # Choose a random email link
    chosen_link = random.choice(links)
    link_text = chosen_link
    link_type = 'legitimate'

    # Game objects
    player = Player('Paddle.png', screen_width - 20, screen_height / 2, 5)
    opponent = Opponent('Paddle.png', 20, screen_height / 2, 5)
    paddle_group = pygame.sprite.Group()
    paddle_group.add(player)
    paddle_group.add(opponent)

    link = LegitimateLink(str(link_text), screen_width / 2, screen_height / 2, 4, 4, paddle_group, link_type, sounds, fonts, screen_dimensions, screen, links)
    link_group = pygame.sprite.GroupSingle()
    link_group.add(link)

    game_manager = GameManager(link_group, paddle_group, links)

    
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            restart_button.handle_event(event)
            pause_button.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.movement -= player.speed
                if event.key == pygame.K_DOWN:
                    player.movement += player.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed

        screen.fill(bg_color)
        pygame.draw.rect(screen, accent_color, middle_strip)

        if not paused:
            # Run the game
            game_manager.run_game()
        else:
            game_manager.draw_game_state()

        # Always draw the pause button and update the display
        restart_button.draw(screen)
        pause_button.draw(screen)
        # Rendering
        pygame.display.flip()
        clock.tick(120)

def restart_game():
    global link_group, paddle_group  # Reset these or other necessary components
    # Add logic to reset scores, player positions, etc.
    link_group.empty()  # Assuming you have something like this
    paddle_group.empty()
    main_game()  