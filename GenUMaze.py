import random

def generate_U_maze():
    # Cấu hình theo kích thước
    WIDTH = 41
    HEIGHT = 31
    
    WALL = 'X'
    PATH = ' '
    START = 'S'
    GOAL = 'G'

    maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)] # Tạo toàn tường
    cx, cy = WIDTH // 2, HEIGHT // 2

    # 2. Định nghĩa bức tường chữ U 
    u_wall_cells = set()
    u_radius_w = 10 
    u_radius_h = 8 
    
    u_left_x = cx - u_radius_w
    u_right_x = cx + u_radius_w
    u_top_y = cy - u_radius_h
    u_bottom_y = cy + u_radius_h

    # Tạo set chứa tọa độ tường chữ U
    for y in range(u_top_y, u_bottom_y + 1):
        u_wall_cells.add((u_left_x, y))
        u_wall_cells.add((u_right_x, y))
    for x in range(u_left_x, u_right_x + 1):
        u_wall_cells.add((x, u_bottom_y))

    # 3. Thuật toán tạo mê cung 
    start_pos = (cx, cy)
    maze[start_pos[1]][start_pos[0]] = PATH
    stack = [start_pos]
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            wx, wy = x + dx // 2, y + dy // 2
            if 0 < nx < WIDTH - 1 and 0 < ny < HEIGHT - 1:
                if maze[ny][nx] == WALL:
                    if (wx, wy) not in u_wall_cells and (nx, ny) not in u_wall_cells:
                        neighbors.append((nx, ny, wx, wy))
        if neighbors:
            nx, ny, wx, wy = random.choice(neighbors)
            maze[wy][wx] = PATH
            maze[ny][nx] = PATH
            stack.append((nx, ny))
        else:
            stack.pop()
    # Khoét mép trên để đảm bảo hai bên chữ U đều có đường đi
    for x in range (3, WIDTH -3):
        maze[1][x] = PATH

    # 4. Đặt vị trí Start và Goal
    maze[start_pos[1]][start_pos[0]] = START
    
    goal_y = u_bottom_y + 3
    goal_x = cx
    
    # Đảm bảo Goal không bao giờ vượt ra ngoài biên
    if goal_y >= HEIGHT - 1: goal_y = HEIGHT - 2
    
    maze[goal_y][goal_x] = GOAL

    # Sửa lỗi G bị tường bao
    cur_y = goal_y - 1 
    
    # Khoan ngược lên trên cho đến khi gặp U-Wall hoặc đường đi
    while cur_y > 0:
        # Điều kiện dừng 1: Chạm phải chính bức tường chữ U (không được phá)
        if (goal_x, cur_y) in u_wall_cells:
            break
            
        # Điều kiện dừng 2: Đã nối vào đường đi chính
        if maze[cur_y][goal_x] == PATH:
            break
        
        # Khoan: Biến tường thành đường
        maze[cur_y][goal_x] = PATH
        cur_y -= 1
    # ------------------------------------------------------------------

    # 5. Xuất file
    filename = "U_maze.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for row in maze:
            f.write("".join(row) + "\n")
            
    print(f"Đã tạo xong mê cung chữ U với kích thước {WIDTH}x{HEIGHT} tại file: {filename}")

generate_U_maze()