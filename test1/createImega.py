import os
import pygame
import random
import math

# Đường dẫn thư mục trên Windows
output_dir = "candies"
os.makedirs(output_dir, exist_ok=True)

# Khởi tạo pygame và thiết lập thông số
pygame.init()
SIZE = 64  # Kích thước ảnh

# Danh sách màu và hình dạng
colors = {
    "red": (255, 0, 0),
    "green": (0, 200, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (160, 32, 240)
}

shapes = ["circle", "square", "triangle", "diamond", "star", "hexagon"]

# Hàm vẽ các hình học
def draw_shape(surface, shape, color):
    center = (SIZE // 2, SIZE // 2)
    if shape == "circle":
        pygame.draw.circle(surface, color, center, SIZE // 3)
    elif shape == "square":
        pygame.draw.rect(surface, color, (SIZE // 4, SIZE // 4, SIZE // 2, SIZE // 2))
    elif shape == "triangle":
        points = [(SIZE // 2, SIZE // 4), (SIZE // 4, 3 * SIZE // 4), (3 * SIZE // 4, 3 * SIZE // 4)]
        pygame.draw.polygon(surface, color, points)
    elif shape == "diamond":
        points = [(SIZE // 2, SIZE // 8), (SIZE // 8, SIZE // 2), (SIZE // 2, 7 * SIZE // 8), (7 * SIZE // 8, SIZE // 2)]
        pygame.draw.polygon(surface, color, points)
    elif shape == "star":
        cx, cy = center
        outer_radius = SIZE // 2.5
        inner_radius = SIZE // 5
        points = []
        for i in range(10):
            angle = i * math.pi / 5  # 36 độ mỗi bước
            r = outer_radius if i % 2 == 0 else inner_radius
            x = cx + r * math.cos(angle - math.pi / 2)
            y = cy + r * math.sin(angle - math.pi / 2)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
    elif shape == "hexagon":
        r = SIZE // 3
        cx, cy = center
        points = [(cx + r * math.cos(i * math.pi / 3), cy + r * math.sin(i * math.pi / 3)) for i in range(6)]
        pygame.draw.polygon(surface, color, points)

# Tạo ảnh từ từng cặp màu + hình
generated_files = []
for color_name, color in colors.items():
    for shape in shapes:
        surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        draw_shape(surface, shape, color)
        filename = f"{color_name}_{shape}.png"
        path = os.path.join(output_dir, filename)
        pygame.image.save(surface, path)
        generated_files.append(path)

pygame.quit()
print("✅ Đã tạo ảnh thành công trong thư mục:", output_dir)
