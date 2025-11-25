from Readdrawmaze import read_maze, find_pos, display_maze, visualize_maze_progress
from BFS import bfs
from Astar import a_star_manhattan


def main():
    # 1. Cấu hình file map
    map_file = "maze_1.txt"  # Đảm bảo file này tồn tại cùng thư mục

    # 2. Đọc dữ liệu
    maze = read_maze(map_file)
    if not maze:
        return

    start = find_pos(maze, 'S')
    goal = find_pos(maze, 'G')

    if not start or not goal:
        print("Lỗi: Không tìm thấy điểm Start (S) hoặc Goal (G) trong mê cung.")
        return

    print(f"Start: {start}, Goal: {goal}")
    print("=== Đóng cửa sổ Pygame để tiếp tục chương trình ===")

    # Xem trước mê cung (tùy chọn)
    # display_maze(maze)

    # 3. Chạy BFS
    print("\n--- Running BFS ---")
    path_bfs, visited_bfs = bfs(maze, start, goal)
    print(f"BFS Path Length: {len(path_bfs)}")
    if path_bfs:
        visualize_maze_progress(maze, visited_bfs, path_bfs)
    else:
        print("BFS không tìm thấy đường đi!")

    # 4. Chạy A* (Manhattan)
    print("\n--- Running A* (Manhattan) ---")
    path_astar, visited_astar = a_star_manhattan(maze, start, goal)
    print(f"A* Path Length: {len(path_astar)}")
    if path_astar:
        visualize_maze_progress(maze, visited_astar, path_astar)
    else:
        print("A* không tìm thấy đường đi!")


if __name__ == "__main__":
    main()