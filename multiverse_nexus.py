import math
import os
import sys
import time

# Cấu hình kích thước hiển thị của màn hình Terminal
WIDTH = 80
HEIGHT = 38

# Định nghĩa mã màu ANSI để tô màu từng thế giới năng lượng
COLOR_PHYSICAL = "\033[93m"  # Màu vàng (Duy Vật)
COLOR_SPIRITUAL = "\033[95m" # Màu tím sen (Tâm Linh)
COLOR_DIGITAL = "\033[96m"   # Màu xanh lục bảo (Kỹ Thuật Số)
COLOR_LOVE = "\033[38;5;205m" # Màu hồng rực rỡ (TÌNH YÊU)
COLOR_RESET = "\033[0m"       # Khôi phục màu mặc định
COLOR_GRAY = "\033[90m"       # Màu xám cho lưới không gian

# Khởi tạo 16 đỉnh của Tesseract 4D
# Mỗi đỉnh có 4 tọa độ (x, y, z, w)
vertices_4d = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w in [-1, 1]:
                vertices_4d.append([x, y, z, w])

# Khởi tạo 32 cạnh kết nối các đỉnh (chỉ kết nối khi khác nhau đúng 1 tọa độ)
edges = []
for i in range(16):
    for j in range(i + 1, 16):
        diff_count = sum(1 for k in range(4) if vertices_4d[i][k] != vertices_4d[j][k])
        if diff_count == 1:
            edges.append((i, j))


class MultiverseEngine:
    def __init__(self):
        # Các góc xoay ban đầu trong không gian 4D
        self.angle_xw = 0.0
        self.angle_yw = 0.0
        self.angle_zw = 0.0
        self.angle_xy = 0.0
        
        # Chỉ số khởi đầu của các vũ trụ
        self.love_resonance = 40.0
        self.start_time = time.time()
        
        # Nhật ký hệ thống đa vũ trụ
        self.logs = [
            "Hệ thống Python đã kích hoạt thành công.",
            "Đang dò tìm luồng dữ liệu trục Số...",
            "Đã kết nối màng lưới lượng tử 4D."
        ]

    def add_log(self, message):
        """Thêm nhật ký và giữ lại tối đa 4 dòng gần nhất để hiển thị"""
        self.logs.append(message)
        if len(self.logs) > 4:
            self.logs.pop(0)

    def rotate_4d(self, vertex, theta, plane):
        """Xoay tọa độ 4D quanh các mặt phẳng không gian"""
        x, y, z, w = vertex
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        
        # Tạo bản sao để tính toán tránh đè dữ liệu
        rx, ry, rz, rw = x, y, z, w
        
        if plane == 0:    # Xoay mặt phẳng XW
            rx = x * cos_t - w * sin_t
            rw = x * sin_t + w * cos_t
        elif plane == 1:  # Xoay mặt phẳng YW
            ry = y * cos_t - w * sin_t
            rw = y * sin_t + w * cos_t
        elif plane == 2:  # Xoay mặt phẳng ZW
            rz = z * cos_t - w * sin_t
            rw = z * sin_t + w * cos_t
        elif plane == 3:  # Xoay mặt phẳng XY
            rx = x * cos_t - y * sin_t
            ry = x * sin_t + y * cos_t
            
        return [rx, ry, rz, rw]

    def project_4d_to_3d(self, vertex, distance):
        """Chiếu phối cảnh từ không gian 4D xuống không gian 3D"""
        x, y, z, w = vertex
        # w đóng vai trò quyết định độ sâu phối cảnh 4D
        factor = 1.0 / (distance - w)
        return [x * factor, y * factor, z * factor]

    def project_3d_to_2d(self, vertex_3d, scale):
        """Chiếu phối cảnh từ không gian 3D xuống màn hình phẳng 2D"""
        x, y, z = vertex_3d
        distance_3d = 2.0
        factor = scale / (distance_3d - z)
        # Bù trừ tỷ lệ ký tự dòng lệnh (thường cao gấp đôi rộng) bằng cách nhân hệ số 1.85 cho x
        screen_x = int(WIDTH / 2 + x * factor * 1.85)
        screen_y = int(HEIGHT / 2 + y * factor)
        return (screen_x, screen_y)

    def draw_line(self, buffer, p0, p1, char, color_code):
        """Thuật toán vẽ đường thẳng Bresenham trên bộ đệm ký tự màu"""
        x0, y0 = p0
        x1, y1 = p1
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                buffer[y0][x0] = (char, color_code)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x0 += sx
            if e2 < dx:
                err += dx; y0 += sy

    def run(self):
        # Ẩn con trỏ terminal để hiển thị mượt mà hơn
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        
        try:
            while True:
                # Tính toán thời gian thực thi
                elapsed = time.time() - self.start_time
                
                # Tiến trình năng lượng Tình Yêu hội tụ
                self.love_resonance = min(100.0, 40.0 + elapsed * 2.8)
                speed_mult = 1.0 + (self.love_resonance / 50.0)
                
                # Tăng các góc xoay dựa trên tốc độ cộng hưởng
                self.angle_xw += 0.022 * speed_mult
                self.angle_yw += 0.018 * speed_mult
                self.angle_zw += 0.014 * speed_mult
                self.angle_xy += 0.008 * speed_mult

                # Tạo ngẫu nhiên log hệ thống dựa theo tiến trình hội tụ
                if int(elapsed) % 4 == 0 and len(self.logs) < 10:
                    if self.love_resonance < 60:
                        self.add_log("[Duy Vật] Các hạt nguyên tử đang gia tăng tần số tự thân.")
                    elif self.love_resonance < 90:
                        self.add_log("[Tâm Linh] Khai mở luân xa kết nối, đồng bộ dòng thời gian song song.")
                    else:
                        self.add_log("[Hệ Thống] Kích hoạt trạng thái Vô Song: Không thể phá vỡ.")

                # Khởi tạo bộ đệm màn hình rỗng: Mỗi ô chứa (Ký tự, Mã màu)
                buffer = [[(' ', COLOR_RESET) for _ in range(WIDTH)] for _ in range(HEIGHT)]

                # Vẽ lưới không gian nền đại diện cho trường lượng tử số
                for y in range(0, HEIGHT, 4):
                    for x in range(0, WIDTH, 8):
                        buffer[y][x] = ('.', COLOR_GRAY)

                # Thực hiện xoay toán học và chiếu đa chiều
                projected_points = []
                # Kích thước siêu khối mở rộng dần khi Tình Yêu tiến gần 100%
                scale = 17.0 + (self.love_resonance * 0.15)
                distance_4d = 2.1

                for v in vertices_4d:
                    # Áp dụng chuỗi xoay liên hoàn trong không gian 4D
                    v_rot = self.rotate_4d(v, self.angle_xw, 0)
                    v_rot = self.rotate_4d(v_rot, self.angle_yw, 1)
                    v_rot = self.rotate_4d(v_rot, self.angle_zw, 2)
                    v_rot = self.rotate_4d(v_rot, self.angle_xy, 3)

                    # Chiếu từ 4D xuống 3D rồi xuống 2D
                    v_3d = self.project_4d_to_3d(v_rot, distance_4d)
                    v_2d = self.project_3d_to_2d(v_3d, scale)
                    projected_points.append(v_2d)

                # Vẽ 32 cạnh của Tesseract lên màn hình
                # Phân bổ màu sắc để biểu thị các chiều thế giới đang tương tác
                for idx, edge in enumerate(edges):
                    p0 = projected_points[edge[0]]
                    p1 = projected_points[edge[1]]
                    
                    if idx < 16:
                        # 16 cạnh đầu: Thế giới vật chất
                        char, color = '#', COLOR_PHYSICAL
                    elif 16 <= idx < 24:
                        # 8 cạnh tiếp theo: Thế giới dữ liệu số
                        char, color = '*', COLOR_DIGITAL
                    else:
                        # 8 cạnh cuối: Thế giới thuộc linh
                        char, color = '@', COLOR_SPIRITUAL
                        
                    # Nếu đạt trạng thái đồng bộ tối cao, tất cả chuyển sang ánh hồng TÌNH YÊU
                    if self.love_resonance >= 99.0:
                        char, color = 'O', COLOR_LOVE
                        
                    self.draw_line(buffer, p0, p1, char, color)

                # Vẽ Lõi Tình Yêu rực sáng ngay tại tâm hình học
                cx, cy = WIDTH // 2, HEIGHT // 2
                if 0 <= cx < WIDTH and 0 <= cy < HEIGHT:
                    buffer[cy][cx] = ('<', COLOR_LOVE)
                    buffer[cy][cx + 1] = ('3', COLOR_LOVE)

                # Xuất toàn bộ dữ liệu ra màn hình terminal
                # Đưa con trỏ terminal về góc trái trên (0,0) để tránh hiện tượng nhấp nháy màn hình
                sys.stdout.write("\033[H")
                
                # Header thông tin
                sys.stdout.write(f"{COLOR_LOVE}=== [ HỆ THỐNG LIÊN KẾT ĐA VŨ TRỤ - PHIÊN BẢN PYTHON ] ==={COLOR_RESET}\n\n")
                
                # Render nội dung buffer
                for y in range(HEIGHT):
                    line_chars = []
                    current_color = ""
                    for x in range(WIDTH):
                        char, color = buffer[y][x]
                        # Tối ưu hóa in màu để tăng tốc độ render
                        if color != current_color:
                            line_chars.append(color)
                            current_color = color
                        line_chars.append(char)
                    sys.stdout.write("".join(line_chars) + "\n")

                # Footer và các chỉ số thần học/khoa học
                sys.stdout.write(f"\n{COLOR_LOVE}========================================================================{COLOR_RESET}\n")
                sys.stdout.write(f"ĐỒNG BỘ THỜI GIAN: {elapsed:.3f} s | ")
                sys.stdout.write(f"TỌA ĐỘ PHÉP XOAY XW: {self.angle_xw:.2f} rad\n")
                sys.stdout.write(f"CHỈ SỐ CỘNG HƯỞNG TÌNH YÊU: {COLOR_LOVE}{self.love_resonance:.1f}%{COLOR_RESET}\n")
                
                # Trạng thái tiến trình
                if self.love_resonance < 60:
                    status = f"{COLOR_DIGITAL}[ĐANG KHỞI CHẠY TIẾN TRÌNH ĐỒNG BỘ HOÀN HẢO...]{COLOR_RESET}"
                elif self.love_resonance < 99:
                    status = f"{COLOR_PHYSICAL}[CỘNG HƯỞNG ĐẠT MỨC SIÊU VƯỢT TRỘI - TIẾN SÁT ĐA CHIỀU]{COLOR_RESET}"
                else:
                    status = f"{COLOR_LOVE}[ĐÃ KÍCH HOẠT PHIÊN BẢN VÔ SONG - KHÔNG THỂ CẢN PHÁÁÁ!]{COLOR_RESET}"
                sys.stdout.write(f"TRẠNG THÁI BẢN THỂ: {status}\n")
                
                # In nhật ký tương tác
                sys.stdout.write(f"{COLOR_GRAY}--- NHẬT KÝ ĐỒNG BỘ GẦN NHẤT ---\n")
                for log in self.logs:
                    sys.stdout.write(f" > {log}\n")
                sys.stdout.write(COLOR_RESET)
                
                # Nghỉ 35ms (~30 khung hình/giây) để tiết kiệm tài nguyên
                time.sleep(0.035)
                
        except KeyboardInterrupt:
            # Hiện lại con trỏ hệ thống khi người dùng thoát bằng Ctrl+C
            sys.stdout.write("\033[?25h\n")
            sys.stdout.write(f"{COLOR_LOVE}Hệ thống đồng bộ đa vũ trụ tạm thời đóng lại. Hẹn gặp lại bản thể hoàn hảo của bạn!{COLOR_RESET}\n")
            sys.stdout.flush()


if __name__ == "__main__":
    # Lệnh xóa màn hình ban đầu
    os.system('cls' if os.name == 'nt' else 'clear')
    engine = MultiverseEngine()
    engine.run()
