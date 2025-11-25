import pygame
import time


# ===============================
# Đọc và xử lý mê cung
# ===============================
def read_maze(filename):
    """Đọc mê cung từ file txt trả về list 2 chiều."""
    try:
        with open(filename, "r") as f:
            maze = [list(line.rstrip("\n")) for line in f]
        return maze
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {filename}")
        return []


def find_pos(maze, target):
    """Tìm tọa độ (x, y) của ký tự target (ví dụ 'S' hoặc 'G')."""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == target:
                return (i, j)
    return None


# ===============================
# Visualization (Pygame)
# ===============================
def display_maze(maze, cell_size=25):
    """Hiển thị mê cung tĩnh."""
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Preview")

    colors = {
        'X': (50, 50, 50),  # Tường
        ' ': (255, 255, 255),  # Đường đi
        'S': (0, 255, 0),  # Start
        'G': (255, 0, 0)  # Goal
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                color = colors.get(maze[y][x], (200, 200, 200))
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (180, 180, 180), rect, 1)

        pygame.display.flip()

    pygame.quit()


def visualize_maze_progress(maze, visited_order, path=None, cell_size=20, delay=0.01):
    """Mô phỏng quá trình tìm đường."""
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    width, height = cols * cell_size, rows * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Search Visualization")

    colors = {
        'X': (40, 40, 40),
        ' ': (255, 255, 255),
        'S': (0, 255, 0),
        'G': (255, 0, 0),
    }

    # Vẽ nền mê cung một lần để tối ưu
    def draw_base_maze():
        for i in range(rows):
            for j in range(cols):
                cell = maze[i][j]
                color = colors.get(cell, (255, 255, 255))
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    draw_base_maze()
    pygame.display.flip()

    # Animation các node đã duyệt
    for step, (x, y) in enumerate(visited_order):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Vẽ visited node hiện tại
        rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (173, 216, 230), rect)  # Màu xanh nhạt

        # Vẽ lại điểm Start và Goal nếu bị đè
        if maze[x][y] == 'S':
            pygame.draw.rect(screen, colors['S'], rect)
        elif maze[x][y] == 'G':
            pygame.draw.rect(screen, colors['G'], rect)

        pygame.display.update(rect)  # Chỉ update phần thay đổi
        time.sleep(delay)

    # Vẽ đường đi cuối (Path)
    if path:
        for (x, y) in path:
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 255), rect)  # Màu xanh dương đậm
            pygame.display.update(rect)
            time.sleep(delay * 2)

    # Chờ đóng cửa sổ
    print("Visualization finished. Close the window to continue.")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()