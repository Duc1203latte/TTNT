import random
import sys
from maze_base import MazeBase, WALL, PATH

# Tăng giới hạn đệ quy cho mê cung lớn
sys.setrecursionlimit(10000)

class ZigzagMaze(MazeBase):
    def generate(self):
        # Bắt đầu tại (1,1)
        self.grid[1][1] = PATH
        self._dfs(1, 1)
        
        # Đặt S và G
        self.set_start_goal()
        return self.grid

    def _dfs(self, r, c):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions) # Xáo trộn ngẫu nhiên hướng đi

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self._in_bounds(nr, nc) and self.grid[nr][nc] == WALL:
                # Đục tường giữa và ô tiếp theo
                self.grid[r + dr // 2][c + dc // 2] = PATH
                self.grid[nr][nc] = PATH
                
                # Gọi đệ quy (tạo nhánh dài ngoằn ngoèo)
                self._dfs(nr, nc)