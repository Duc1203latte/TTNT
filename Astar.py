from heapq import heappush, heappop


def heuristic_manhattan(a, b):
    """Tính khoảng cách Manhattan giữa 2 điểm."""
    (x1, y1), (x2, y2) = a, b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_manhattan(maze, start, goal):
    """
    Thuật toán A* với heuristic Manhattan.
    Trả về: (path, visited_order)
    """
    open_list = [] #Danh sách các ô chờ xét
    # Priority Queue lưu tuple: (f_score, (x, y))
    heappush(open_list, (0, start))

    came_from = {} #Truy vết đường đi
    g_score = {start: 0} #Chi phí thực tế đi từ start đến đây
    visited_order = []

    while open_list:
        _, current = heappop(open_list)
        visited_order.append(current)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_order

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            #Kiểm tra biên và tường
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 'X':
                tentative_g = g_score[current] + 1 #Gi thực tế mới

                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g
                    f = tentative_g + heuristic_manhattan((nx, ny), goal) #Tính F=G+H
                    heappush(open_list, (f, (nx, ny)))
                    came_from[(nx, ny)] = current

    return [], visited_order





