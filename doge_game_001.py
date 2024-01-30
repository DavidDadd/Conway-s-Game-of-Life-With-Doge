import pygame
import numpy as np
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 3
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 215, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Function to initialize the grid from an image
def create_grid_from_image(image_path, desired_pixels):
    image = Image.open(image_path)
    image = image.convert('1')  # Convert to black and white
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    # Calculate new dimensions while maintaining the aspect ratio
    if aspect_ratio > 1:
        print("bigger than 1")
        new_width = desired_pixels
        new_height = int(desired_pixels / aspect_ratio)
    else:
        print("smaller than 1")
        new_height = desired_pixels
        new_width = int(desired_pixels * aspect_ratio)

    image = image.resize((new_width, new_height))
    data = np.array(image)
    grid = np.where(data == 0, 1, 0)  # Convert black to alive and white to dead
    return grid

# Function to draw the grid
def draw_grid(screen, grid, cell_size):
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            color = WHITE if grid[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size - 1, cell_size - 1))

# Function to update the grid
def update_grid(grid):
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            state = grid[row][col]
            # Count living neighbors with wrap-around
            neighbors = sum([grid[(row + i) % ROWS][(col + j) % COLS] for i in range(-1, 2) for j in range(-1, 2)]) - state
            # Apply Conway's rules
            if state == 0 and neighbors == 3:
                new_grid[row][col] = 1
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row][col] = 0
    return new_grid

# Main game loop
def game_loop(grid):
    global CELL_SIZE
    ROWS, COLS = grid.shape
    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Zoom in
                    CELL_SIZE = min(CELL_SIZE + 1, 20)  # Increase cell size, max 20 for example
                    print("zoom in")
                elif event.key == pygame.K_MINUS:  # Zoom out
                    CELL_SIZE = max(CELL_SIZE - 1, 1)  # Decrease cell size, min 1
                    print("zoom out")
                # Recalculate ROWS and COLS based on new CELL_SIZE
                ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
            elif paused:  # Handle mouse input only when paused
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    row, col = mouseY // cell_size, mouseX // cell_size
                    if event.button == 1:  # Left click
                        grid[row % ROWS][col % COLS] = 1  # Set cell to alive
                        print(f"Cell set to alive at ({row % ROWS}, {col % COLS})")
                    elif event.button == 3:  # Right click
                        grid[row % ROWS][col % COLS] = 0  # Set cell to dead
                        print(f"Cell set to dead at ({row % ROWS}, {col % COLS})")

        if not paused:
            grid = update_grid(grid)
        
        screen.fill(BLACK)
        draw_grid(screen, grid, CELL_SIZE)
        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


if __name__ == "__main__":
    desired_pixels = 200  # Customize the number of pixels here
    grid = create_grid_from_image("Capture.png", desired_pixels)
    ROWS, COLS = grid.shape  # Update grid dimensions
    game_loop(grid)
