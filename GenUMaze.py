import random


def generate_U_maze(rows, cols):
    # Đảm bảo kích thước lẻ
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1

    # Kích thước tối thiểu để vẽ được chữ U
    if rows < 15 or cols < 15:
        print("Cảnh báo: Kích thước quá nhỏ để tạo U-Maze. Đang tăng lên 21x21.")
        rows = max(rows, 21)
        cols = max(cols, 21)

    WALL = 'X'
    PATH = ' '
    START = 'S'
    GOAL = 'G'

    maze = [[WALL for _ in range(cols)] for _ in range(rows)]
    cx, cy = cols // 2, rows // 2

    # --- 1. Tạo hình chữ U ---
    u_wall_cells = set()
    # Tự động tính toán độ lớn chữ U dựa trên kích thước map (chiếm khoảng 50% map)
    u_radius_w = cols // 4
    u_radius_h = rows // 4

    u_left_x = cx - u_radius_w
    u_right_x = cx + u_radius_w
    u_top_y = cy - u_radius_h
    u_bottom_y = cy + u_radius_h

    for y in range(u_top_y, u_bottom_y + 1):
        u_wall_cells.add((u_left_x, y))
        u_wall_cells.add((u_right_x, y))
    for x in range(u_left_x, u_right_x + 1):
        u_wall_cells.add((x, u_bottom_y))

    # --- 2. DFS đục lỗ (Tránh tường U) ---
    start_pos = (cx, cy)
    maze[start_pos[1]][start_pos[0]] = PATH
    stack = [start_pos]
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            wx, wy = x + dx // 2, y + dy // 2  # Tường trung gian

            if 0 < nx < cols - 1 and 0 < ny < rows - 1:
                if maze[ny][nx] == WALL:
                    # Logic quan trọng: Không được đục trúng tường chữ U
                    if (wx, wy) not in u_wall_cells and (nx, ny) not in u_wall_cells:
                        neighbors.append((nx, ny, wx, wy))

        if neighbors:
            nx, ny, wx, wy = random.choice(neighbors)
            maze[wy][wx] = PATH
            maze[ny][nx] = PATH
            stack.append((nx, ny))
        else:
            stack.pop()

    # Mở đường thoát ở mép trên
    for x in range(1, cols - 1):
        maze[1][x] = PATH

    # --- 3. Đặt Start / Goal ---
    maze[cy][cx] = START

    goal_x = cx
    goal_y = min(u_bottom_y + 2, rows - 2)  # Đảm bảo goal nằm dưới đáy U nhưng trong map

    maze[goal_y][goal_x] = GOAL

    # Khoan ngược từ Goal lên để đảm bảo có đường vào
    cur_y = goal_y - 1
    while cur_y > 0:
        if (goal_x, cur_y) in u_wall_cells: break
        if maze[cur_y][goal_x] == PATH: break
        maze[cur_y][goal_x] = PATH
        cur_y -= 1

    return maze