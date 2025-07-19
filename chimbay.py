import pygame as pg, random, sys
pg.init()

# ⚙️ Cấu hình
W, H, G, P, GAP, FPS = 800, 600, 100, 78, 175, 60
DEBUG_HITBOX = True  # Bật/Tắt vẽ vùng va chạm
font = pg.font.SysFont("Arial", 32)
IMG = lambda name: pg.image.load(f"TAI_NGUYEN/Image/{name}").convert_alpha()

# 🔄 Va chạm hình tròn và hình chữ nhật
def circle_rect_collide(c, r, rect):
    x, y = max(rect.left, min(c[0], rect.right)), max(rect.top, min(c[1], rect.bottom))
    return (c[0]-x)**2 + (c[1]-y)**2 <= r**2

# 🐤 Chim
class Bird:
    def __init__(self):
        flaps = ["downflap", "midflap", "upflap"]
        imgs = [IMG(f"yellowbird-{f}.png") for f in flaps]
        self.imgs = [pg.transform.scale(i, (int(i.get_width()*1.15), int(i.get_height()*1.15))) for i in imgs]
        self.x, self.y, self.v = 80, H//2, 0

    def update(self): self.v += 0.4; self.y += self.v
    def flap(self): self.v = -8

    def draw(self, s):
        idx = 0 if self.v < -2 else 2 if self.v > 2 else 1
        img = pg.transform.rotate(self.imgs[idx], -self.v*3)
        s.blit(img, img.get_rect(center=(self.x, self.y)).topleft)

        # 🔴 Vẽ hitbox hình tròn
        if DEBUG_HITBOX:
            c, r = self.get_circle()
            pg.draw.circle(s, (255, 0, 0), c, r, width=2)

    def get_circle(self):
        w, h = self.imgs[1].get_size()
        offset_x, offset_y, scale = 0, 0, 0.7
        cx = int(self.x + w * offset_x)
        cy = int(self.y + h * offset_y)
        radius = int(min(w, h) * scale)
        return (cx, cy), radius

# 🧱 Ống nước
class Pipe:
    def __init__(self, x):
        self.img = pg.transform.scale(IMG("pipe-green.png"), (P, 400))
        self.x = x
        self.h = random.randint(50, H - GAP - G - 50)
        self.passed = False

    def update(self, spd): self.x -= spd

    def draw(self, s):
        s.blit(pg.transform.flip(self.img, 0, 1), (self.x, self.h - self.img.get_height()))
        s.blit(self.img, (self.x, self.h + GAP))

        # 🟩 Vẽ hitbox hình chữ nhật
        if DEBUG_HITBOX:
            for rect in self.rects():
                pg.draw.rect(s, (0, 255, 0), rect, width=2)

    def rects(self):
        top = pg.Rect(self.x, 0, P, self.h)
        bot = pg.Rect(self.x, self.h + GAP, P, H - self.h - GAP - G)
        return top, bot

# 🎮 Game chính
class Game:
    def __init__(self):
        self.s = pg.display.set_mode((W, H))
        pg.display.set_caption("Flappy Bird")
        self.bg = pg.transform.scale(IMG("background-day.png"), (W, H))
        self.clock = pg.time.Clock()
        self.reset()

    def reset(self):
        self.bird, self.pipes = Bird(), []
        self.score, self.spd, self.run = 0, 3, True

    def loop(self):
        global DEBUG_HITBOX
        t = 0
        while self.run:
            self.clock.tick(FPS)
            t += 1
            if t % (5 * FPS) == 0: self.spd += 0.5

            for e in pg.event.get():
                if e.type == pg.QUIT: sys.exit()
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_SPACE: self.bird.flap()
                    elif e.key == pg.K_d: DEBUG_HITBOX = not DEBUG_HITBOX  # Toggle hitbox

            self.bird.update()

            if not self.pipes or self.pipes[-1].x < W - 300:
                self.pipes.append(Pipe(W))

            for p in self.pipes[:]:
                p.update(self.spd)
                if p.x + P < 0: self.pipes.remove(p)
                if not p.passed and p.x + P < self.bird.x:
                    self.score += 1
                    p.passed = True

                # Kiểm tra va chạm
                for r in p.rects():
                    if circle_rect_collide(*self.bird.get_circle(), r):
                        self.run = False

            if self.bird.y < -50 or self.bird.y > H - G:
                self.run = False

            self.draw()

        self.over()

    def draw(self):
        self.s.blit(self.bg, (0, 0))
        for p in self.pipes: p.draw(self.s)
        self.bird.draw(self.s)
        pg.draw.rect(self.s, (222, 184, 135), (0, H - G, W, G))
        self.text(f"Score: {self.score}", 10, 10)
        pg.display.flip()

    def text(self, t, x, y): self.s.blit(font.render(t, True, (0, 0, 0)), (x, y))

    def over(self):
        self.text("Game Over", W//2 - 80, H//2 - 50)
        self.text(f"Score: {self.score}", W//2 - 60, H//2)
        self.text("Press SPACE to play again", W//2 - 140, H//2 + 50)
        pg.display.flip(); pg.time.wait(500)

        while True:
            for e in pg.event.get():
                if e.type == pg.QUIT: sys.exit()
                if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                    self.reset(); self.loop()
            self.clock.tick(FPS)

# ▶️ Chạy game
if __name__ == "__main__":
    Game().loop()
