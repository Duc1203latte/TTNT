import random


class DenseMaze:
    def __init__(self, rows, cols):
        """
        Khởi tạo mê cung Dense (Prim's Algorithm).
        Tự động điều chỉnh kích thước thành số lẻ.
        """
        # Đảm bảo kích thước là số lẻ để tường và đường đi xen kẽ đúng chuẩn
        self.rows = rows if rows % 2 != 0 else rows + 1
        self.cols = cols if cols % 2 != 0 else cols + 1

        self.WALL = 'X'
        self.PATH = ' '
        self.START = 'S'
        self.GOAL = 'G'

        # Khởi tạo toàn bộ là TƯỜNG
        self.grid = [[self.WALL for _ in range(self.cols)] for _ in range(self.rows)]

    def generate(self):
        """Sinh mê cung và trả về ma trận."""
        # 1. Bắt đầu khai phá từ ô (1,1)
        start_r, start_c = 1, 1
        self.grid[start_r][start_c] = self.PATH

        # Danh sách chứa các bức tường "ứng cử viên" để đục
        # Format: (r_middle, c_middle, r_next, c_next)
        walls = []

        # Hàm nội bộ thêm tường xung quanh một ô vào danh sách
        def add_walls(r, c):
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Kiểm tra biên và đảm bảo ô đích chưa được khai phá (vẫn là WALL)
                if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                    if self.grid[nr][nc] == self.WALL:
                        # Lưu tọa độ tường ở giữa và ô đích
                        walls.append((r + dr // 2, c + dc // 2, nr, nc))

        # Thêm tường xung quanh điểm xuất phát
        add_walls(start_r, start_c)

        # 2. Vòng lặp Prim (Randomized Prim's Algorithm)
        while walls:
            # Chọn ngẫu nhiên 1 bức tường trong danh sách
            rand_index = random.randint(0, len(walls) - 1)
            mid_r, mid_c, next_r, next_c = walls.pop(rand_index)

            # Nếu ô đích đằng sau bức tường vẫn chưa được khai phá
            if self.grid[next_r][next_c] == self.WALL:
                self.grid[mid_r][mid_c] = self.PATH  # Đục tường giữa
                self.grid[next_r][next_c] = self.PATH  # Đục ô đích

                # Tiếp tục thêm các tường xung quanh ô mới này vào danh sách
                add_walls(next_r, next_c)

        # 3. Đặt Start và Goal
        self.grid[1][1] = self.START
        self.grid[self.rows - 2][self.cols - 2] = self.GOAL

        return self.grid