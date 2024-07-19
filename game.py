import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (169, 169, 169)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Choice Reaction Test')

# Shapes
CIRCLE = 'circle'
SQUARE = 'square'
SHAPES = [CIRCLE, SQUARE]

# Keys
CIRCLE_KEY = pygame.K_q
SQUARE_KEY = pygame.K_p
START_KEY = pygame.K_RETURN
QUIT_KEY = pygame.K_ESCAPE

# Game duration
GAME_DURATION = 30  # seconds (2 minutes)
PENALTY_POINTS = 50  # points to deduct for wrong response
BASE_SCORE = 1000  # base score for reaction time

# Variables
running = True
game_started = False
clock = pygame.time.Clock()
reaction_times = []
wrong_responses = 0
shape_display_time = 4000  # milliseconds
time_decrease_rate = 20  # milliseconds
min_display_time = 1200  # milliseconds
score = 0
last_reaction_time = 0

# Load font
font = pygame.font.Font(pygame.font.match_font('couriernew', bold=True), 24)

# Function to draw shapes
def draw_shape(shape, position):
    screen.fill(BLACK)
    draw_top_bar(score, last_reaction_time)
    if shape == CIRCLE:
        pygame.draw.circle(screen, BLUE, position, 30)  # Smaller circle
    elif shape == SQUARE:
        pygame.draw.rect(screen, RED, (*position, 60, 60))  # Smaller square
    pygame.display.flip()

# Function to draw the top bar
def draw_top_bar(score, reaction_time):
    pygame.draw.rect(screen, GREY, (0, 0, SCREEN_WIDTH, 50))
    score_text = font.render(f"Score: {score}", True, BLACK)
    reaction_time_text = font.render(f"Time: {reaction_time:.2f} ms", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(reaction_time_text, (SCREEN_WIDTH - 300, 10))

# Function to display welcome screen
def display_welcome_screen():
    screen.fill(BLACK)
    welcome_text = [
        "Welcome to the Choice Reaction Test!",
        "Press 'q' when you see a BLUE circle.",
        "Press 'p' when you see a RED square.",
        "The shapes will appear in random positions.",
        "Press Enter to start the game.",
        "Press ESC to quit at any time."
    ]
    for i, line in enumerate(welcome_text):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 100 + i * 40))
    pygame.display.flip()

# Function to display result screen
def display_result_screen(avg_reaction_time, wrong_responses, score):
    screen.fill(BLACK)
    result_text = [
        "Game Over!",
        f"Average Reaction Time: {avg_reaction_time:.2f} ms",
        f"Number of Wrong Responses: {wrong_responses}",
        f"Final Score: {score}",
        "Press ESC to quit."
    ]
    for i, line in enumerate(result_text):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 100 + i * 40))
    pygame.display.flip()

    # Wait for the user to press ESC to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == QUIT_KEY):
                waiting = False
                return False  # Exit the game
    return True

# Main loop
while running:
    if not game_started:
        display_welcome_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == QUIT_KEY):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == START_KEY:
                game_started = True
                start_time = time.time()
                last_shape_time = start_time
        continue
    
    # Check if the game duration has passed
    elapsed_time = time.time() - start_time
    if elapsed_time > GAME_DURATION:
        avg_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0
        running = display_result_screen(avg_reaction_time, wrong_responses, score)
        game_started = False
        continue
    
    shape = random.choice(SHAPES)
    position = (random.randint(50, SCREEN_WIDTH - 100), random.randint(50, SCREEN_HEIGHT - 100))
    draw_shape(shape, position)
    shape_shown_start_time = time.time()
    shape_shown = True

    while shape_shown and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == QUIT_KEY):
                running = False
                shape_shown = False
            elif event.type == pygame.KEYDOWN:
                reaction_time = (time.time() - shape_shown_start_time) * 1000  # Convert to milliseconds
                if shape == CIRCLE and event.key == CIRCLE_KEY:
                    reaction_times.append(reaction_time)
                    score += max(0, BASE_SCORE - int(reaction_time))  # Higher score for faster reactions
                    shape_shown = False
                elif shape == SQUARE and event.key == SQUARE_KEY:
                    reaction_times.append(reaction_time)
                    score += max(0, BASE_SCORE - int(reaction_time))  # Higher score for faster reactions
                    shape_shown = False
                else:
                    wrong_responses += 1
                    score -= PENALTY_POINTS  # Deduct points for wrong response
                    shape_shown = False
        
        if not shape_shown:
            last_reaction_time = reaction_time
            screen.fill(BLACK)
            draw_top_bar(score, last_reaction_time)
            pygame.time.wait(max(200, int(reaction_time)))  # Wait time between shapes depends on reaction time

    shape_display_time = max(min_display_time, shape_display_time - time_decrease_rate)
    clock.tick(60)

# Quit pygame
pygame.quit()
