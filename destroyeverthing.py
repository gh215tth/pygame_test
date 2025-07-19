import pygame, random, sys, os

# === INIT ===
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obstacle Destruction Game")
clock = pygame.time.Clock()

# === CONSTANTS ===
TANK_W, TANK_H = 50, 30
OBSTACLE_SIZE = 100
BULLET_SIZE = 10
TANK_SPEED = 10
BULLET_SPEED = 15
OBSTACLE_SPAWN_RATE = 30
OBSTACLE_SPEED_RANGE = (3, 8)

# === COLORS ===
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# === FONTS ===
font_small = pygame.font.SysFont(None, 36)
font_large = pygame.font.SysFont(None, 72)

# === CLASS: Tank ===
class Tank:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 50, TANK_W, TANK_H)

    def move(self, dx):
        self.rect.x = max(0, min(WIDTH - TANK_W, self.rect.x + dx))

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - 5, self.rect.top - 10, 10, 10))

# === CLASS: Bullet ===
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE)

    def update(self):
        self.rect.y -= BULLET_SPEED
        return self.rect.bottom < 0

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# === CLASS: Obstacle ===
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - OBSTACLE_SIZE), -OBSTACLE_SIZE, OBSTACLE_SIZE, OBSTACLE_SIZE)
        self.speed = random.randint(*OBSTACLE_SPEED_RANGE)
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))

    def update(self):
        self.rect.y += self.speed
        return self.rect.top > HEIGHT

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# === VA CHẠM ===
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# === MAIN GAME LOOP ===
def main():
    tank = Tank()
    bullets, obstacles = [], []
    score, high_score = 0, 0
    game_active = True

    # Load high score
    if os.path.exists("highscore.txt"):
        with open("highscore.txt") as f:
            high_score = int(f.read().strip() or 0)
    else:
        with open("highscore.txt", "w") as f:
            f.write("0")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bullets.append(Bullet(tank.rect.centerx - BULLET_SIZE//2, tank.rect.top - BULLET_SIZE))
                elif event.key == pygame.K_r and not game_active:
                    tank.reset()
                    bullets.clear()
                    obstacles.clear()
                    score = 0
                    game_active = True

        if game_active:
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * TANK_SPEED
            tank.move(dx)

            # Spawn obstacles
            if random.randint(1, OBSTACLE_SPAWN_RATE) == 1:
                obstacles.append(Obstacle())

            # Update bullets
            bullets = [b for b in bullets if not b.update()]

            # Update obstacles + xử lý va chạm
            remaining_obstacles = []
            for ob in obstacles:
                if ob.update(): continue

                hit = False
                for b in bullets:
                    if ob.rect.colliderect(b.rect):
                        bullets.remove(b)
                        score += 1
                        hit = True
                        break
                if hit: continue

                if ob.rect.colliderect(tank.rect):
                    game_active = False
                else:
                    remaining_obstacles.append(ob)
            obstacles = remaining_obstacles

            # Draw game
            screen.fill(DARK_BLUE)
            tank.draw()
            for b in bullets: b.draw()
            for ob in obstacles: ob.draw()
            screen.blit(font_small.render(f"Score: {score}", True, WHITE), (10, 10))
            screen.blit(font_small.render(f"High Score: {high_score}", True, WHITE), (10, 50))

        else:
            # Game Over screen
            if score > high_score:
                high_score = score
                with open("highscore.txt", "w") as f:
                    f.write(str(high_score))

            screen.fill(BLACK)
            screen.blit(font_large.render("GAME OVER", True, RED), (WIDTH//2 - 160, HEIGHT//2 - 100))
            screen.blit(font_small.render(f"Score: {score}", True, WHITE), (WIDTH//2 - 50, HEIGHT//2))
            screen.blit(font_small.render("Press R to restart", True, WHITE), (WIDTH//2 - 100, HEIGHT//2 + 50))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
