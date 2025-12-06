import random
import sys

# Tăng giới hạn đệ quy vì thuật toán DFS đi rất sâu (đặc biệt với map lớn)
sys.setrecursionlimit(20000)


class ZigzagMaze:
    def __init__(self, rows, cols):
        """
        Khởi tạo mê cung Zigzag (DFS Algorithm).
        Tự động điều chỉnh kích thước thành số lẻ.
        """
        # Đảm bảo kích thước là số lẻ
        self.rows = rows if rows % 2 != 0 else rows + 1
        self.cols = cols if cols % 2 != 0 else cols + 1

        self.WALL = 'X'
        self.PATH = ' '
        self.START = 'S'
        self.GOAL = 'G'

        # Tạo lưới toàn tường
        self.grid = [[self.WALL for _ in range(self.cols)] for _ in range(self.rows)]

    def generate(self):
        """Sinh mê cung và trả về ma trận."""
        # Bắt đầu đào từ ô (1,1)
        self.grid[1][1] = self.PATH
        self._dfs(1, 1)

        # Đặt điểm Start và Goal
        self.grid[1][1] = self.START
        # Đặt Goal ở góc dưới cùng bên phải
        self.grid[self.rows - 2][self.cols - 2] = self.GOAL

        return self.grid

    def _dfs(self, r, c):
        """Hàm đệ quy đào đường (Recursive Backtracker)"""
        # 4 hướng di chuyển: Lên, Xuống, Trái, Phải (Bước nhảy 2)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)  # Xáo trộn để tạo đường đi ngẫu nhiên

        for dr, dc in directions:
            nr, nc = r + dr, c + dc  # Ô đích đến
            wr, wc = r + dr // 2, c + dc // 2  # Ô tường ở giữa

            # Kiểm tra xem ô đích có nằm trong biên và có phải là Tường chưa phá không
            if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                if self.grid[nr][nc] == self.WALL:
                    # Đục thông tường ở giữa và ô đích
                    self.grid[wr][wc] = self.PATH
                    self.grid[nr][nc] = self.PATH

                    # Gọi đệ quy tiếp từ ô mới
                    self._dfs(nr, nc)