import pygame
import random

# 🚀 Khởi tạo
pygame.init()
W, H, SIZE, SPEED = 800, 600, 20, 15
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# 🍎 Sinh tọa độ thức ăn (không trùng rắn)
def spawn_food(snake):
    while True:
        fx = random.randrange(0, W, SIZE)
        fy = random.randrange(0, H, SIZE)
        if [fx, fy] not in snake:
            return fx, fy

# 🐍 Vẽ rắn
def draw_snake(snake):
    for seg in snake:
        pygame.draw.rect(screen, WHITE, (*seg, SIZE, SIZE))

# 🧮 Hiển thị điểm
def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# 🟥 Màn hình Game Over
def show_game_over(score):
    screen.fill(BLACK)
    f = pygame.font.SysFont(None, 50)
    lines = [
        f.render("Game Over!", True, WHITE),
        f.render("Q - Quit | R - Restart", True, WHITE),
        f.render(f"Score: {score}", True, WHITE)
    ]
    for i, line in enumerate(lines):
        screen.blit(line, (W // 6, H // 3 + i * 50))
    pygame.display.update()

# 🎮 Vòng lặp game chính
def main():
    while True:
        x, y = W // 2, H // 2
        dx, dy = 0, 0
        snake = []
        length = 1
        score = 0
        food = spawn_food(snake)
        game_over = False

        while not game_over:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT and dx == 0: dx, dy = -SIZE, 0
                    elif e.key == pygame.K_RIGHT and dx == 0: dx, dy = SIZE, 0
                    elif e.key == pygame.K_UP and dy == 0: dx, dy = 0, -SIZE
                    elif e.key == pygame.K_DOWN and dy == 0: dx, dy = 0, SIZE

            x += dx
            y += dy

            # ❌ Va chạm tường
            if x < 0 or x >= W or y < 0 or y >= H:
                break

            head = [x, y]
            snake.append(head)
            if len(snake) > length:
                snake.pop(0)

            # ❌ Cắn chính mình
            if head in snake[:-1]:
                break

            # ✅ Ăn thức ăn
            if head == list(food):
                length += 1
                score += 1
                food = spawn_food(snake)

            # 🎨 Vẽ màn hình
            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, (*food, SIZE, SIZE))
            draw_snake(snake)
            draw_score(score)
            pygame.display.update()
            clock.tick(SPEED)

        # 🟥 Game Over
        show_game_over(score)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        return
                    elif e.key == pygame.K_r:
                        break
            else:
                continue
            break

# ▶️ Bắt đầu game
main()
pygame.quit()
