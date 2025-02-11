import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Negative object
GREEN = (0, 255, 0)  # Positive object
YELLOW = (255, 255, 0)  # Power-up
DARK_BLUE = (25, 25, 50)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 0, 255)

# Fonts
title_font = pygame.font.Font(None, 48)
text_font = pygame.font.SysFont("Segoe UI Emoji", 16)  
button_font = pygame.font.Font(None, 30)

# Function to show welcome screen
def show_welcome_screen():
    screen.fill(DARK_BLUE)  # Background color

    # Title
    title_text = title_font.render("Catch the Falling Objects!", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Instruction Box
    box_rect = pygame.Rect(30, 120, WIDTH - 60, 320)
    pygame.draw.rect(screen, LIGHT_GRAY, box_rect, border_radius=15)

    # Instructions Text
    instructions = [
        "Rules:",
        "🔹 Move the basket left & right to catch objects.",
        "✅ Catch GREEN objects (+1 point).",
        "❌ Avoid RED objects (-1 point).",
        "⭐ YELLOW power-ups give extra life or slow time.",
        "⚠️ Missing GREEN objects decreases lives.",
        "⏳ The game speeds up over time!",
    ]

    y_pos = 140
    for index, line in enumerate(instructions):
        bold = index == 0  # Make "Rules:" bold
        text = text_font.render(line, True, BLACK if not bold else RED)
        screen.blit(text, (box_rect.x + 20, y_pos))
        y_pos += 40

    # "Press Any Key" Button
    pygame.draw.rect(screen, RED, (140, 470, 220, 50), border_radius=15)
    button_text = button_font.render("Press Any Key to Start", True, WHITE)
    screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, 480))

    pygame.display.flip()

    # Wait for key press to start
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Show the welcome screen before starting the game
show_welcome_screen()

pygame.mixer.init()
catch_sound = pygame.mixer.Sound("catch.wav")  # Sound for catching objects
miss_sound = pygame.mixer.Sound("miss.wav")  # Sound when missing an object
powerup_sound = pygame.mixer.Sound("powerup.wav")  # Sound when collecting power-up

# Player (Basket)
basket_width = 80
basket = pygame.Rect(WIDTH // 2 - basket_width // 2, HEIGHT - 50, basket_width, 20)

# Falling Objects
object_size = 20
falling_objects = []

# Object types: Dictionary with color and attributes
object_types = [
    {'color': GREEN, 'points': 1},  # Normal object
    {'color': RED, 'points': -1},   # Negative object (avoid)
    {'color': YELLOW, 'power': True}  # Power-up
]

# Game Variables
speed = 5
score = 0
lives = 3
slow_mode = False
slow_duration = 0

# Clock
clock = pygame.time.Clock()
running = True

# Game Loop
while running:
    screen.fill(WHITE)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.x > 0:
        basket.x -= 7
    if keys[pygame.K_RIGHT] and basket.x < WIDTH - basket_width:
        basket.x += 7

    # Generate Falling Objects
    if random.randint(1, 30) == 1:  # Random spawn rate
        obj_type = random.choice(object_types)
        x_pos = random.randint(0, WIDTH - object_size)
        rect = pygame.Rect(x_pos, 0, object_size, object_size)  # Create rect
        falling_objects.append({'rect': rect, 'color': obj_type['color'], 'points': obj_type.get('points', 0), 'power': obj_type.get('power', False)})

    # Move Objects
    for obj in falling_objects[:]:
        obj['rect'].y += speed
        if obj['rect'].colliderect(basket):  # Collision with basket
            falling_objects.remove(obj)
            if obj['power']:  # Power-up logic
                powerup_sound.play()
                if random.choice([True, False]):  # 50% chance to slow down objects
                    slow_mode = True
                    slow_duration = 100  # Lasts for 100 frames
                else:
                    lives += 1  # Extra life
            else:
                score += obj['points']
                if obj['points'] > 0:
                    catch_sound.play()
                else:
                    miss_sound.play()
        elif obj['rect'].y > HEIGHT:  # Missed object
            falling_objects.remove(obj)
            if obj['points'] > 0:
                lives -= 1
                miss_sound.play()

    # Draw Basket & Objects
    pygame.draw.rect(screen, BLUE, basket)
    for obj in falling_objects:
        pygame.draw.rect(screen, obj['color'], obj['rect'])

    # Display Score & Lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    # Game Over
    if lives <= 0:
        screen.fill(WHITE)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Increase difficulty over time
    if score % 10 == 0 and score > 0:
        speed += 0.01  # Increase speed slightly

    # Handle Slow Mode
    if slow_mode:
        speed = 3  # Slow down objects
        slow_duration -= 1
        if slow_duration <= 0:
            slow_mode = False
            speed = 5  # Restore normal speed

    pygame.display.flip()
    clock.tick(30)  # Frame rate

pygame.quit()
