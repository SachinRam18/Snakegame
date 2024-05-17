import pygame
import random
import pygame.freetype

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_YELLOW = (255, 255, 0)
NEON_GREEN = (57, 255, 20)
NEON_BLUE= (0,255,255)
RED = (255, 0, 0)

# Snake properties
BLOCK_SIZE = 40
SNAKE_SPEED = 7

# Direction
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Game over flag
game_over = False

# Score
score = 0

# Function to display text on the screen
def display_text(font, text, color, size, x, y):
    text_surface, _ = font.render(text, size=size, fgcolor=color)
    screen.blit(text_surface, (x, y))

# Function to draw retry button
def draw_retry_button(font):
    pygame.draw.rect(screen, BLACK, retry_button_pos + retry_button_size)
    display_text(font, "Retry", NEON_GREEN, 100, retry_button_pos[0] , retry_button_pos[1] + 10)

# Function to generate food
def generate_food():
    food_x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    food_y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return food_x, food_y

# Function to restart the game
def restart_game():
    global snake, snake_direction, score, game_over
    snake = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
    snake_direction = RIGHT
    score = 0
    game_over = False
    # Generate new food position
    generate_food()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Initialize snake
snake = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
snake_direction = RIGHT

# Initial food position
food_x, food_y = generate_food()

# Initialize font
font = pygame.freetype.Font("Oswald-Regular.ttf")

# Retry button dimensions and positions
retry_button_size = (200, 50)
retry_button_pos = ((SCREEN_WIDTH - retry_button_size[0]) // 2, (SCREEN_HEIGHT - retry_button_size[1]) // 2)

# Button dimensions and positions
button_size = 100
button_margin = 20

# Load arrow images
arrow_up_img = pygame.image.load('arrow_up.png')
arrow_down_img = pygame.image.load('arrow_down.png')
arrow_left_img = pygame.image.load('arrow_left.png')
arrow_right_img = pygame.image.load('arrow_right.png')

# Resize arrow images
arrow_up_img = pygame.transform.scale(arrow_up_img, (button_size, button_size))
arrow_down_img = pygame.transform.scale(arrow_down_img, (button_size, button_size))
arrow_left_img = pygame.transform.scale(arrow_left_img, (button_size, button_size))
arrow_right_img = pygame.transform.scale(arrow_right_img, (button_size, button_size))

button_up = pygame.Rect((SCREEN_WIDTH - button_size) / 2, SCREEN_HEIGHT - 3 * button_size - 2 * button_margin, button_size, button_size)
button_down = pygame.Rect((SCREEN_WIDTH - button_size) / 2, SCREEN_HEIGHT - button_size - button_margin, button_size, button_size)
button_left = pygame.Rect(button_margin, SCREEN_HEIGHT - 2 * button_size - button_margin, button_size, button_size)
button_right = pygame.Rect(SCREEN_WIDTH - button_size - button_margin, SCREEN_HEIGHT - 2 * button_size - button_margin, button_size, button_size)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if game_over and retry_button_pos[0] <= mouse_pos[0] <= retry_button_pos[0] + retry_button_size[0] and \
                    retry_button_pos[1] <= mouse_pos[1] <= retry_button_pos[1] + retry_button_size[1]:
                restart_game()
            elif not game_over:
                if button_up.collidepoint(mouse_pos) and snake_direction != DOWN:
                    snake_direction = UP
                elif button_down.collidepoint(mouse_pos) and snake_direction != UP:
                    snake_direction = DOWN
                elif button_left.collidepoint(mouse_pos) and snake_direction != RIGHT:
                    snake_direction = LEFT
                elif button_right.collidepoint(mouse_pos) and snake_direction != LEFT:
                    snake_direction = RIGHT

    # Move the snake if the game is not over
    if not game_over:
        if snake_direction == UP:
            new_head = [snake[0][0], snake[0][1] - BLOCK_SIZE]
        elif snake_direction == DOWN:
            new_head = [snake[0][0], snake[0][1] + BLOCK_SIZE]
        elif snake_direction == LEFT:
            new_head = [snake[0][0] - BLOCK_SIZE, snake[0][1]]
        elif snake_direction == RIGHT:
            new_head = [snake[0][0] + BLOCK_SIZE, snake[0][1]]

        snake.insert(0, new_head)
        # Check if the snake eats food
        if new_head[0] == food_x and new_head[1] == food_y:
            score += 10
            food_x, food_y = generate_food()
        else:
            snake.pop()  # Remove the last segment if not eating food

        # Wrap the snake around the screen edges
        snake[0][0] %= SCREEN_WIDTH
        snake[0][1] %= SCREEN_HEIGHT

        # Check for collision with itself
        for block in snake[1:]:
            if snake[0] == block:
                game_over = True
                break

    # Clear the screen
    screen.fill(BLACK)

    # Draw the snake
    for block in snake:
        pygame.draw.rect(screen, NEON_BLUE,  [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

    # Draw food
    pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

    # Draw arrow buttons
    screen.blit(arrow_up_img, button_up)
    screen.blit(arrow_down_img, button_down)
    screen.blit(arrow_left_img, button_left)
    screen.blit(arrow_right_img, button_right)

    # Display the score
    display_text(font, f"Score: {score}", NEON_GREEN, 40, 10, 10)

    # If game over, draw retry button
    if game_over:
        draw_retry_button(font)

    # Update the display
    pygame.display.update()

    # Set the game FPS
    clock.tick(SNAKE_SPEED)
