import pygame
import random
import os

# === Cấu hình cơ bản ===
pygame.init()
WIDTH, HEIGHT = 480, 640
ROWS, COLS = 8, 8
TILE_SIZE = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match-3 Candy Game")

# === Tải hình ảnh viên kẹo ===
image_folder = "candies"
all_images = []
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        img = pygame.image.load(os.path.join(image_folder, filename)).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        all_images.append(img)

NUM_TYPES = len(all_images)

# === Lưới viên kẹo ===
grid = [[random.randint(0, NUM_TYPES - 1) for _ in range(COLS)] for _ in range(ROWS)]
selected = []  # lưu 2 ô được chọn

# === Hàm hỗ trợ ===
def draw_board():
    screen.fill((30, 30, 30))
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE_SIZE + 50
            y = row * TILE_SIZE + 50
            tile_type = grid[row][col]
            screen.blit(all_images[tile_type], (x, y))
            # Vẽ khung nếu được chọn
            if [row, col] in selected:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, TILE_SIZE, TILE_SIZE), 3)


def swap(a, b):
    grid[a[0]][a[1]], grid[b[0]][b[1]] = grid[b[0]][b[1]], grid[a[0]][a[1]]


def is_adjacent(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def find_matches():
    matched = []

    # Theo hàng
    for row in range(ROWS):
        for col in range(COLS - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matched.extend([[row, col], [row, col + 1], [row, col + 2]])

    # Theo cột
    for col in range(COLS):
        for row in range(ROWS - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matched.extend([[row, col], [row + 1, col], [row + 2, col]])

    return matched


def remove_matches(matches):
    for row, col in matches:
        grid[row][col] = -1  # gán -1 để xóa


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

# === Vòng lặp chính ===
clock = pygame.time.Clock()
running = True

while running:
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
                            remove_matches(matches)
                        else:
                            swap(a, b)  # hoàn tác nếu không match
                    selected = []

    matches = find_matches()
    if matches:
        remove_matches(matches)
        drop_candies()

    clock.tick(60)

pygame.quit()

