import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UIDropDownMenu, UITextBox, UIPanel, UIScrollingContainer, UIImage
from pygame_gui.windows import UIMessageWindow

from datetime import datetime
import sys
sys.setrecursionlimit(20000)
#Tăng giới hạn phòng trường hợp đệ quy quá lớn

from Readdrawmaze import find_pos, visualize_maze_progress, display_maze
from BFS import bfs
from Astar import a_star_manhattan

#Import các thuật toán sinh Map
from dense_algo import DenseMaze
from zigzag_algo import ZigzagMaze
from GenUMaze import generate_U_maze
from GenOpenMaze import generate_open_maze

#Cấu hình màu sắc và kích thước
WINDOW_SIZE = (950,650)
MAZE_AREA_RECT = pygame.Rect(20,80,600,450) #Vùng xám hiển thị map
CELL_SIZE = 15 #Kích thước mặc định mỗi ô, sẽ tự điều chỉnh sau
COLOR_BG = (245,245,250)
COLOR_MAZE_BG = (200,200,200)
COLOR_WALL = (50, 50, 50)
COLOR_PATH = (255, 255, 255)
COLOR_START = (0, 255, 0)
COLOR_GOAL = (255, 0, 0)
COLOR_VISITED = (173, 216, 230) # Xanh nhạt
COLOR_FINAL_PATH = (0, 0, 255)  # Xanh đậm

#Quản lý trạng thái ứng dụng
class MazeApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tìm đường đi mê cung")
        self.window_surface = pygame.display.set_mode(WINDOW_SIZE)
        self.manager = pygame_gui.UIManager(WINDOW_SIZE)

        self.clock = pygame.time.Clock()
        self.is_running = True

        #Trạng thái dữ liệu
        self.current_maze = None
        self.start_pos = None
        self.goal_pos = None

        #Biến phục vụ Visualization
        self.viz_generator = None #Máy phát từng bước chạy
        self.viz_speed_delay = 20 #Tốc độ chạy
        self.last_viz_update = 0
        self.drawn_visited = []
        self.drawn_path = []

        # Lưu meta map + lịch sử
        self.current_maze_type = ""
        self.current_row = 0
        self.current_col = 0

        self.history = [] #list[dict]
        self.history_panel = None
        self.history_scroll = None
        self.history_close_btn = None

        #Khởi tạo giao diện
        self.setup_ui()

    def setup_ui(self):
        """Tạo các nút bấm, ô nhập liệu"""
        #Header: Tìm đường đi mê cung
        header_panel = UIPanel(relative_rect= pygame.Rect(20,10,300,50),
                               starting_height = 1,
                               manager = self.manager)
        UITextBox('<b>Tìm đường đi mê cung</b></font>',
                  relative_rect= pygame.Rect(0,0,300,50),
                  manager=self.manager, container= header_panel)
        #Panel điều khiển bên phải
        control_x = 640 #Tọa độ x bắt đầu của cột điều khiển
        UITextBox("Chọn kích thước map (hãng cột) (lẻ): ", pygame.Rect(control_x,80,280,35), self.manager)

        #Ô nhập hàng
        UITextBox("Hàng: ", pygame.Rect(control_x,110,70,35), self.manager)
        self.rows_input = UITextEntryLine(pygame.Rect(control_x + 70,115,60,35), self.manager, initial_text='41')
        self.rows_input.set_allowed_characters('numbers')
        #Ô nhập cột
        UITextBox("Cột: ", pygame.Rect(control_x + 140,115,60,35), self.manager)
        self.cols_input = UITextEntryLine(pygame.Rect(control_x + 200,115,60,35), self.manager, initial_text='51')
        self.cols_input.set_allowed_characters('numbers')

        UITextBox("Loại map:", pygame.Rect(control_x,165,280,35), self.manager)
        self.maze_type_dropdown = UIDropDownMenu(['Dense', 'Zigzag', 'Open maze', 'U-maze'],
                                                 'Dense',
                                                 pygame.Rect(control_x,200,260,35),
                                                 self.manager)

        # Nút tạo Map (Màu trắng viền đen trong thiết kế)
        self.btn_generate = UIButton(pygame.Rect(control_x, 250, 260, 50), "TẠO MAP MỚI", self.manager)

        UITextBox("Thuật toán:", pygame.Rect(control_x, 320, 280, 35), self.manager)
        self.algo_dropdown = UIDropDownMenu(['BFS', 'A* (Manhattan)'],
                                            'BFS',
                                            pygame.Rect(control_x, 355, 260, 35),
                                            self.manager)

        # Nút Chạy thuật toán (Màu xanh teal trong thiết kế)
        self.btn_run = UIButton(pygame.Rect(control_x, 410, 260, 60), "CHẠY THUẬT TOÁN", self.manager)

        # 3. Panel kết quả bên dưới (Màu hồng nhạt)
        result_panel = UIPanel(relative_rect=pygame.Rect(20, 550, 600, 80),
                               starting_height=1, manager=self.manager)

        # nút xem lịch sử
        self.btn_history = UIButton(pygame.Rect(control_x, 480, 260, 45), "LỊCH SỬ", self.manager)
        result_panel = UIPanel(relative_rect=pygame.Rect(20, 550, 600, 80),
                               starting_height=1, manager=self.manager)
        self.result_box = UITextBox("Kết quả sẽ hiện ở đây...", pygame.Rect(0, 0, 600, 80),
                                    manager=self.manager, container=result_panel)

    def get_dropdown_value(self, dropdown):
        """Hàm hỗ trợ lấy giá trị chuẩn từ menu (xử lý lỗi tuple)"""
        val = dropdown.selected_option
        if isinstance(val, tuple):
            return val[0]  # Lấy phần tử đầu tiên nếu là tuple
        return str(val)

    """def show_error(self, message):
        
        UIMessageWindow(rect=pygame.Rect(WINDOW_SIZE[0]//2 - 200, WINDOW_SIZE[1]//2 - 100, 400, 200),
                        html_message= f'<font color=#FF0000>{message}</font>',
                        manager=self.manager,window_title='Lỗi')"""

    def handle_generate_maze(self):
        """Xử lý khi bấm nút tạo map"""
        try:
            rows = int(self.rows_input.get_text())
            cols = int(self.cols_input.get_text())
            #Đảm bảo số lẻ
            if rows % 2 == 0: rows +=1
            if cols % 2 == 0: cols +=1
            self.rows_input.set_text(str(rows))
            self.cols_input.set_text(str(cols))
        except ValueError:
            self.result_box.set_text("Kích thước phải là số nguyên")
            return
        maze_type = self.get_dropdown_value(self.maze_type_dropdown)
        self.current_maze_type = maze_type
        self.current_rows = rows
        self.current_cols = cols

        # lưu mê cung để lưu vào lịch sử
        self.current_maze_type = maze_type
        self.current_row = rows
        self.current_col = cols

        self.current_maze = None #Reset map cũ

        status_msg = f"Đang tạo {maze_type} ({rows}x{cols})..."
        self.result_box.set_text(status_msg)
        print(status_msg)

        if 'Dense' in maze_type:
            self.current_maze = DenseMaze(rows, cols).generate()
        elif 'Zigzag' in maze_type:
            self.current_maze = ZigzagMaze(rows, cols).generate()
        elif 'Open maze' in maze_type:
            self.current_maze = generate_open_maze(rows, cols, braid_factor=0.3)
        elif 'U-maze' in maze_type:
            self.current_maze = generate_U_maze(rows, cols)

        if self.current_maze:
            self.start_pos = find_pos(self.current_maze, 'S')
            self.goal_pos = find_pos(self.current_maze, 'G')
            #Reset trạng thái visualization
            self.viz_generator = None;
            self.drawn_visited = []
            self.drawn_path = []

            #Tự động tính toán cell size để vẽ vừa khung
            map_w = len(self.current_maze[0])
            map_h = len(self.current_maze)
            global CELL_SIZE
            CELL_SIZE = min(MAZE_AREA_RECT.width//map_w, MAZE_AREA_RECT.height//map_h)
            if CELL_SIZE < 2: CELL_SIZE = 2
            self.result_box.set_text(f"Đã tạo {maze_type}. Sẵn sàng chạy thuật toán!")
        else:
            self.result_box.set_text("Lỗi không xác định khi tạo mê cung")

    def handle_run_algorithm(self):
        """Xử lý bấm nút khi chạy thuật toán"""
        if not self.current_maze:
            self.result_box.set_text("Chưa có bản đồ, vui lòng tạo bản đồ trước")
            return

        algo = self.get_dropdown_value(self.algo_dropdown)
        self.result_box.set_text(f"Đang chạy {algo}....")

        path,visited = [], []
        start_time = pygame.time.get_ticks()
        if algo == 'BFS':
            path,visited = bfs(self.current_maze, self.start_pos, self.goal_pos)
        elif 'A*' in algo:
            path, visited = a_star_manhattan(self.current_maze, self.start_pos, self.goal_pos)

        end_time = pygame.time.get_ticks()
        time_taken = end_time - start_time

        status = "<font color='#00FF00'>TÌM THẤY ĐƯỜNG!</font>" if path else "<font color='#FF0000'>KHÔNG TÌM THẤY!</font>"
        result_msg = (f"Thuật toán: {algo} | {status}<br>"
                      f"Độ dài: {len(path)} bước | Xét duyệt: {len(visited)} ô | Thời gian: {time_taken}ms")
        self.result_box.set_text(result_msg)

        # lưu lịch sử
        self.add_history_entry(algo, visited, path, time_taken)

        if visited:
            self.viz_generator = self.create_visualization_generator(visited, path)
            self.drawn_visited = []
            self.drawn_path = []

    def create_visualization_generator(self,visited_order,path):
        """Tạo ra một generator để yield từng bước vẽ"""
        #Vẽ các ô đã duyệt
        for node in visited_order:
            yield ('visited', node)
        #Vẽ đường đi cuối
        if path:
            for node in path:
                yield ('path', node)
        yield ('done', None)

    def update(self, time_delta):
        """Cập nhật logic mỗi khung hình"""
        self.manager.update(time_delta)

        #Xử lý hoạt hình
        if self.viz_generator:
            current_time = pygame.time.get_ticks()
            #Kiểm tra xem đã đến lúc vẽ bước tiếp theo chưa
            if current_time - self.last_viz_update > self.viz_speed_delay:
                try:
                    type, node = next(self.viz_generator)
                    if type == 'visited':
                        self.drawn_visited.append(node)
                    elif type == 'path':
                        self.drawn_path.append(node)
                        self.viz_speed_delay = 50 #Chậm lại khi vẽ đường cuối
                    elif type == 'done':
                        self.viz_generator = None # Kết thúc
                        self.viz_speed_delay = 20 #Reset tốc độ
                    self.last_viz_update = current_time
                except StopIteration:
                    self.viz_generator = None

    def render_maze_snapshot(self, visited=None, path=None, thumb_size=(220, 160)):
        """Vẽ mê cung + visited + path lên surface offscreen rồi scale thành thumbnail."""
        surf = pygame.Surface((MAZE_AREA_RECT.width, MAZE_AREA_RECT.height))
        surf.fill(COLOR_MAZE_BG)

        if not self.current_maze:
            return pygame.transform.smoothscale(surf, thumb_size)

        rows = len(self.current_maze)
        cols = len(self.current_maze[0])

        offset_x = (MAZE_AREA_RECT.width - cols * CELL_SIZE) // 2
        offset_y = (MAZE_AREA_RECT.height - rows * CELL_SIZE) // 2

        # nền mê cung
        for r in range(rows):
            for c in range(cols):
                cell_val = self.current_maze[r][c]
                color = COLOR_WALL if cell_val == 'X' else COLOR_PATH
                rect = pygame.Rect(offset_x + c * CELL_SIZE, offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surf, color, rect)

        # visited
        if visited:
            for r, c in visited:
                rect = pygame.Rect(offset_x + c * CELL_SIZE, offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surf, COLOR_VISITED, rect)

        # path
        if path:
            for r, c in path:
                rect = pygame.Rect(offset_x + c * CELL_SIZE, offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surf, COLOR_FINAL_PATH, rect)

        # S/G
        if self.start_pos:
            r, c = self.start_pos
            rect = pygame.Rect(offset_x + c * CELL_SIZE, offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surf, COLOR_START, rect)

        if self.goal_pos:
            r, c = self.goal_pos
            rect = pygame.Rect(offset_x + c * CELL_SIZE, offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surf, COLOR_GOAL, rect)

        return pygame.transform.smoothscale(surf, thumb_size)

    def add_history_entry(self, algo, visited, path, time_taken_ms):
        thumb = self.render_maze_snapshot(visited=visited, path=path, thumb_size=(220, 160))

        entry = {
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "maze_type": self.current_maze_type,
            "rows": self.current_rows,
            "cols": self.current_cols,
            "algo": algo,
            "visited_count": len(visited) if visited else 0,
            "path_len": len(path) if path else 0,
            "time_ms": time_taken_ms,
            "thumb": thumb
        }

        self.history.append(entry)

        # Giới hạn lịch sử để tránh nặng RAM
        if len(self.history) > 30:
            self.history = self.history[-30:]

        # Nếu đang mở trang lịch sử thì refresh
        if self.history_panel is not None:
            self.build_history_page()

    def toggle_history_page(self):
        if self.history_panel is not None:
            self.history_panel.kill()
            self.history_panel = None
            self.history_scroll = None
            self.history_close_btn = None
            return self.build_history_page()

    def build_history_page(self):
        # refresh: xoá cũ dựng mới
        if self.history_panel is not None:
            self.history_panel.kill()

        self.history_panel = UIPanel(
            relative_rect=pygame.Rect(60, 50, 830, 560),
            starting_height=3,
            manager=self.manager
        )

        UITextBox(
            "<b>LỊCH SỬ CHẠY THUẬT TOÁN</b>",
            pygame.Rect(15, 10, 650, 35),
            self.manager,
            container=self.history_panel
        )

        self.history_close_btn = UIButton(
            pygame.Rect(740, 10, 75, 35),
            "ĐÓNG",
            self.manager,
            container=self.history_panel
        )

        self.history_scroll = UIScrollingContainer(
            relative_rect=pygame.Rect(15, 55, 800, 490),
            manager=self.manager,
            container=self.history_panel
        )

        scroll_container = self.history_scroll.scrollable_container

        if len(self.history) == 0:
            UITextBox(
                "Chưa có lần chạy nào. Hãy tạo map và chạy thuật toán trước!",
                pygame.Rect(0, 0, 760, 60),
                self.manager,
                container=scroll_container
            )
            self.history_scroll.set_scrollable_area_dimensions((780, 80))
            return

        item_h = 190
        content_w = 780
        content_h = len(self.history) * item_h + 10

        y = 0
        # mới nhất lên trước
        for i, entry in enumerate(reversed(self.history), start=1):
            item_panel = UIPanel(
                relative_rect=pygame.Rect(0, y, content_w, item_h - 10),
                starting_height=1,
                manager=self.manager,
                container=scroll_container
            )

            UIImage(
                relative_rect=pygame.Rect(10, 10, entry["thumb"].get_width(), entry["thumb"].get_height()),
                image_surface=entry["thumb"],
                manager=self.manager,
                container=item_panel
            )

            info_html = (
                f"<b>#{i}</b> | <b>{entry['algo']}</b><br>"
                f"Thời gian chạy: <b>{entry['time_ms']} ms</b><br>"
                f"Ngày giờ: {entry['time']}<br>"
                f"Map: {entry['maze_type']} ({entry['rows']}x{entry['cols']})<br>"
                f"Ô duyệt: <b>{entry['visited_count']}</b> | "
                f"Ô đường đi: <b>{entry['path_len']}</b>"
            )

            UITextBox(
                info_html,
                pygame.Rect(245, 10, 520, 160),
                self.manager,
                container=item_panel
            )

            y += item_h

        self.history_scroll.set_scrollable_area_dimensions((content_w, content_h))

    def draw_maze_area(self):
        """Vẽ mê cung và các bước visualization"""
        #Vẽ nền
        pygame.draw.rect(self.window_surface, COLOR_MAZE_BG, MAZE_AREA_RECT)
        if not self.current_maze: return

        rows = len(self.current_maze)
        cols = len(self.current_maze[0])

        #Tính offset để căn giữa map trong vùng
        offset_x = MAZE_AREA_RECT.x + (MAZE_AREA_RECT.width - cols * CELL_SIZE) // 2
        offset_y = MAZE_AREA_RECT.y + (MAZE_AREA_RECT.height - rows * CELL_SIZE) // 2

        #vẽ nền mê cung tĩnh
        for r in range(rows):
            for c in range(cols):
                cell_val = self.current_maze[r][c]
                color = COLOR_WALL if cell_val == 'X' else COLOR_PATH
                rect = pygame.Rect(offset_x + c*CELL_SIZE, offset_y+ r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.window_surface, color, rect)

        #vẽ các ô đã duyệt
        for r,c in self.drawn_visited:
            rect = pygame.Rect(offset_x + c*CELL_SIZE, offset_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.window_surface, COLOR_VISITED, rect)

        #Vẽ đường đi cuối
        for r,c in self.drawn_path:
            rect = pygame.Rect(offset_x + c*CELL_SIZE, offset_y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.window_surface, COLOR_FINAL_PATH, rect)

        #Vẽ lại S và G đè lên trên cùng
        if self.start_pos:
            r,c = self.start_pos
            rect = pygame.Rect(offset_x+ c*CELL_SIZE, offset_y+ r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.window_surface, COLOR_START, rect)
        if self.goal_pos:
            r,c = self.goal_pos
            rect = pygame.Rect(offset_x+c*CELL_SIZE, offset_y+ r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.window_surface, COLOR_GOAL, rect)

    def draw(self):
        self.window_surface.fill(COLOR_BG)

        self.draw_maze_area()

        self.manager.draw_ui(self.window_surface)
        pygame.display.update()

    def run(self):
        """Vòng lặp chính của game"""
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0 #Giói hạn 60 FPS

            #Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                #Truền sự kiện cho pygame_gui xử lý
                self.manager.process_events(event)
                #Bắt sự kiện click nút
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.btn_generate:
                        self.handle_generate_maze()
                    elif event.ui_element == self.btn_run:
                        self.handle_run_algorithm()
                    elif event.ui_element == self.btn_history:
                        self.toggle_history_page()
                    elif self.history_close_btn is not None and event.ui_element == self.history_close_btn:
                        self.toggle_history_page()

            #Cập nhật logic và vẽ
            self.update(time_delta)
            self.draw()

        pygame.quit()

#Chay chương trình
if __name__ == "__main__":
    app = MazeApp()
    app.run()

