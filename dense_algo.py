import random
from maze_base import MazeBase, WALL, PATH

class DenseMaze(MazeBase):
    def generate(self):
        # Bắt đầu tại (1,1)
        start_r, start_c = 1, 1
        self.grid[start_r][start_c] = PATH
        walls = []
        
        # Hàm nội bộ thêm tường
        def add_walls(r, c):
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if self._in_bounds(nr, nc) and self.grid[nr][nc] == WALL:
                    walls.append((r + dr // 2, c + dc // 2, nr, nc))

        add_walls(start_r, start_c)

        while walls:
            # Chọn ngẫu nhiên 1 tường (Tạo độ ngẫu nhiên cao -> Dày đặc)
            rand_index = random.randint(0, len(walls) - 1)
            mid_r, mid_c, next_r, next_c = walls.pop(rand_index)

            if self.grid[next_r][next_c] == WALL:
                self.grid[mid_r][mid_c] = PATH   # Đục tường giữa
                self.grid[next_r][next_c] = PATH # Đục ô đích
                add_walls(next_r, next_c)
        
        # Đặt điểm S và G sau khi tạo xong đường đi
        self.set_start_goal()
        return self.grid