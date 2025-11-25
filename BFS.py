from collections import deque


def bfs(maze, start, goal):
    """
    Thuật toán Breadth-First Search.
    Trả về: (path, visited_order)
    """
    queue = deque([start])
    visited = {start: None}
    visited_order = []

    found = False

    while queue:
        current = queue.popleft()
        visited_order.append(current)

        if current == goal:
            found = True
            break

        x, y = current
        # Các hướng di chuyển: Lên, Xuống, Trái, Phải
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # Kiểm tra biên và tường
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
                if maze[nx][ny] != 'X' and (nx, ny) not in visited:
                    visited[(nx, ny)] = current
                    queue.append((nx, ny))

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