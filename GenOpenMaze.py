import random

# Directions: lên, xuống, trái, phải
DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

def generate_open_maze(rows, cols, braid_factor):
    # Đảm bảo rows, cols là số lẻ
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1

    # Tạo toàn tường
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    def carve(x, y):
        maze[x][y] = 0
        my_dirs = list(DIRS)
        random.shuffle(my_dirs)
        
        for dx, dy in my_dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < rows-1 and 1 <= ny < cols-1 and maze[nx][ny] == 1:
                maze[x + dx//2][y + dy//2] = 0
                carve(nx, ny)

    carve(1, 1)

    # Duyệt qua các ô tường nội bộ và ngẫu nhiên phá vỡ chúng (Làm thoáng mê cung)
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            
            if maze[r][c] == 1:
                
                # Đây là các ô tường nằm giữa hai đường đi, không phải tường ngoài
                # Các ô tường nội bộ luôn có 1 tọa độ chẵn và 1 tọa độ lẻ
                is_interior_wall = (r % 2 == 0 and c % 2 != 0) or \
                                   (r % 2 != 0 and c % 2 == 0)
                
                if is_interior_wall:
                    # Kiểm tra xem bức tường này có nằm giữa hai đường đi đã được tạo không
                    # Nếu nó ngăn cách hai ô đã mở (0, S, G), ta có thể phá nó
                    
                    if r % 2 == 0: # Tường ngang
                        cell1 = maze[r-1][c]
                        cell2 = maze[r+1][c]
                    else: # Tường dọc 
                        cell1 = maze[r][c-1]
                        cell2 = maze[r][c+1]
                        
                    # Nếu cả hai ô liền kề đều là đường đi (khác 1)
                    if cell1 != 1 and cell2 != 1:
                        # Dùng random.random() để quyết định có phá tường không
                        if random.random() < braid_factor:
                            maze[r][c] = 0 # Phá tường -> tạo thêm đường đi/vòng lặp

    # Đánh dấu S và G
    maze[1][1] = 'S'
    maze[rows-2][cols-2] = 'G'
    return maze

def save_maze_to_txt(maze, filename="maze.txt"):
    """
    Lưu mê cung vào file txt với định dạng:
    # : Tường
      : Đường đi (dấu cách)
    S : Điểm bắt đầu
    G : Điểm kết thúc
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for row in maze:
                line_str = ""
                for cell in row:
                    if cell == 1:
                        line_str += "X"
                    elif cell == 0:
                        line_str += " " # Dấu cách
                    else:
                        line_str += str(cell) # Giữ nguyên 'S' hoặc 'G'
                
                f.write(line_str + "\n") # Xuống dòng sau mỗi hàng
        
        print(f"Đã lưu mê cung thành công vào file: {filename}")
        
    except Exception as e:
        print(f"Có lỗi khi lưu file: {e}")

# --- CHẠY CHƯƠNG TRÌNH ---

# 1. Tạo mê cung trong bộ nhớ
rows = 31
cols = 41
my_maze = generate_open_maze(rows, cols, braid_factor=0.2)

# 2. Lưu ra file txt để chương trình khác dùng
save_maze_to_txt(my_maze, "open_maze.txt")