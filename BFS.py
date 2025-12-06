from collections import deque


def bfs(maze, start, goal):
    """
    Thuật toán Breadth-First Search.
    Trả về: (path, visited_order)
    """
    queue = deque([start]) #Hàng đợi chứa các ô cần duyệt
    visited = {start: None} #Lưu vết {Ô hiện tại} dạng {con:cha}
    visited_order = [] #Danh sách thứ tự duyệt

    found = False

    while queue:
        current = queue.popleft() #Lấy ô đầu hàng đợi ra để xét
        visited_order.append(current)

        if current == goal: #Nếu chạm địch thì dừng lại
            found = True
            break

        x, y = current
        # Các hướng di chuyển: Lên, Xuống, Trái, Phải
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy #Tọa độ hàng xóm mới

            # Kiểm tra biên và tường
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]): #Kiểm tra xem có nằm trong khung mê cung không
                if maze[nx][ny] != 'X' and (nx, ny) not in visited: #Kiểm tra xem có phải tường không và đã đi qua chưa
                    visited[(nx, ny)] = current #Con (nx,ny) được sinh ra từ cha curent
                    queue.append((nx, ny)) #Xếp hàng xóm vào hàng đợi để xét sau

    if not found:
        return [], visited_order

    # Truy vết đường đi (Reconstruct path)
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = visited[node]
    path.reverse()

    return path, visited_order