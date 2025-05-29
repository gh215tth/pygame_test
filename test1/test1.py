import pygame
import random
import os

pygame.init()
WIDTH, HEIGHT = 580, 640
ROWS, COLS = 8, 8
TILE_SIZE = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match-3 Candy Game")

font = pygame.font.SysFont(None, 32)
start_time = pygame.time.get_ticks()
time_limit = 30
score = 0

background = pygame.image.load("candies/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

image_folder = "candies"
all_images = []
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        img = pygame.image.load(os.path.join(image_folder, filename)).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        all_images.append(img)

NUM_TYPES = len(all_images)

grid = [[random.randint(0, NUM_TYPES - 1) for _ in range(COLS)] for _ in range(ROWS)]
selected = []

def draw_info():
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = max(0, time_limit - elapsed)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Time: {remaining}s", True, (200, 255, 0))
    screen.blit(score_text, (20, 10))
    screen.blit(time_text, (WIDTH - 150, 10))

def draw_board():
    screen.blit(background, (0, 0))
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE + 50
            y = row * TILE_SIZE + 50
            tile_type = grid[row][col]
            if tile_type >= 0:
                screen.blit(all_images[tile_type], (x, y))
            if [row, col] in selected:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, TILE_SIZE, TILE_SIZE), 3)
    draw_info()

def swap(a, b):
    grid[a[0]][a[1]], grid[b[0]][b[1]] = grid[b[0]][b[1]], grid[a[0]][a[1]]

def is_adjacent(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def find_matches():
    matched = []

    for row in range(ROWS):
        for col in range(COLS - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matched.extend([[row, col], [row, col + 1], [row, col + 2]])

    for col in range(COLS):
        for row in range(ROWS - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matched.extend([[row, col], [row + 1, col], [row + 2, col]])

    return matched

def remove_matches(matches):
    for row, col in matches:
        grid[row][col] = -1

def drop_candies():
    for col in range(COLS):
        for row in range(ROWS - 1, -1, -1):
            if grid[row][col] == -1:
                for k in range(row - 1, -1, -1):
                    if grid[k][col] != -1:
                        grid[row][col], grid[k][col] = grid[k][col], -1
                        break
                else:
                    grid[row][col] = random.randint(0, NUM_TYPES - 1)

clock = pygame.time.Clock()
running = True

while running:
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    if elapsed >= time_limit:
        print("⏰ Time out! Score:", score)
        running = False
        continue

    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - 50) // TILE_SIZE
            row = (y - 50) // TILE_SIZE

            if 0 <= row < ROWS and 0 <= col < COLS:
                selected.append([row, col])
                if len(selected) == 2:
                    a, b = selected
                    if is_adjacent(a, b):
                        swap(a, b)
                        matches = find_matches()
                        if matches:
                            score += len(matches) * 10
                            time_limit += len(matches) - 2
                            remove_matches(matches)
                            drop_candies()
                        else:
                            swap(a, b)
                    selected = []

    while True:
        matches = find_matches()
        if matches:
            remove_matches(matches)
            drop_candies()
        else:
            break
    clock.tick(60)

pygame.quit()
