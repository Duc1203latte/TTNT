import random

# Định nghĩa các hướng đi: Lên, Xuống, Trái, Phải (bước nhảy 2)
DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# Định nghĩa ký tự cho thống nhất với hệ thống
WALL = 'X'
PATH = ' '
START = 'S'
GOAL = 'G'


def generate_open_maze(rows, cols, braid_factor=0.2):
    """
    Sinh mê cung kiểu 'Open/Braid' (có vòng lặp, ít ngõ cụt).
    Trả về: Ma trận (List 2 chiều).
    """
    # 1. Đảm bảo rows, cols là số lẻ
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1

    # 2. Khởi tạo toàn bộ là TƯỜNG ('X')
    maze = [[WALL for _ in range(cols)] for _ in range(rows)]

    # Hàm đục tường đệ quy (giống DFS)
    def carve(x, y):
        maze[x][y] = PATH
        my_dirs = list(DIRS)
        random.shuffle(my_dirs)

        for dx, dy in my_dirs:
            nx, ny = x + dx, y + dy
            # Kiểm tra biên và xem ô đích có phải tường không
            if 1 <= nx < rows - 1 and 1 <= ny < cols - 1 and maze[nx][ny] == WALL:
                maze[x + dx // 2][y + dy // 2] = PATH  # Đục tường giữa
                carve(nx, ny)

    # Bắt đầu đục từ (1, 1)
    carve(1, 1)

    # 3. Kỹ thuật Braiding: Phá bỏ ngõ cụt tạo vòng lặp
    # Duyệt qua các ô tường nội bộ
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):

            if maze[r][c] == WALL:
                # Kiểm tra tường nội bộ (tường lẻ-chẵn hoặc chẵn-lẻ)
                is_interior_wall = (r % 2 == 0 and c % 2 != 0) or \
                                   (r % 2 != 0 and c % 2 == 0)

                if is_interior_wall:
                    # Xác định 2 ô bên cạnh bức tường
                    if r % 2 == 0:  # Tường nằm ngang -> check trên dưới
                        cell1 = maze[r - 1][c]
                        cell2 = maze[r + 1][c]
                    else:  # Tường nằm dọc -> check trái phải
                        cell1 = maze[r][c - 1]
                        cell2 = maze[r][c + 1]

                    # Nếu bức tường này đang ngăn cách 2 con đường (PATH)
                    if cell1 == PATH and cell2 == PATH:
                        # Tung xúc xắc xem có phá không
                        if random.random() < braid_factor:
                            maze[r][c] = PATH  # Phá tường -> Tạo vòng lặp

    # 4. Đặt Start và Goal
    maze[1][1] = START
    maze[rows - 2][cols - 2] = GOAL

    return maze