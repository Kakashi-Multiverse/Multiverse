```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multiverse Optimization Engine (MOE) - Bản Thể Ý Chí Thực Tế Bất Biến
Tác giả: Gemini Cosmic Developer
Mô tả: Chương trình giả lập toán học và vật lý lượng tử mô tả quá trình 
       tự sửa lỗi và tối ưu hóa toàn cục của Đa Vũ Trụ trước các nhiễu loạn cục bộ.
"""

import os
import sys
import math
import time
import random

# Định nghĩa mã màu ANSI cho Terminal thêm phần trực quan và thẩm mỹ
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BG_DARK = '\033[48;5;232m'

class SpaceTimeParticle:
    """Đại diện cho một hạt tọa độ không-thời gian trong Đa vũ trụ."""
    def __init__(self, pid, tx, ty):
        self.id = pid
        # Tọa độ mục tiêu tối ưu (Ý chí Thực tế định sẵn)
        self.tx = tx
        self.ty = ty
        # Tọa độ thực tế hiện tại (Có thể bị hỗn loạn sai lệch)
        self.x = tx + random.uniform(-15, 15)
        self.y = ty + random.uniform(-15, 15)
        # Vận tốc dao động
        self.vx = 0.0
        self.vy = 0.0
        # Mức độ sai lệch hiện tại so với trạng thái tối ưu
        self.deviation = 0.0

    def update(self, will_power, chaos_seeds):
        """Áp dụng Lực phục hồi của Ý chí Thực tế và sức hút từ các hạt Hỗn loạn."""
        # 1. Lực Phục Hồi (Ý chí Thực tế): Phương trình lò xo giảm chấn phục hồi trạng thái
        dx = self.tx - self.x
        dy = self.ty - self.y
        
        # Hệ số đàn hồi của ý chí thực tế
        spring_force = 0.05 * will_power
        damping = 0.82 # Lực cản môi trường lượng tử để tránh dao động vô hạn
        
        self.vx += dx * spring_force
        self.vy += dy * spring_force

        # 2. Lực Nhiễu Loạn Cục Bộ (Chaos Seeds)
        for seed in chaos_seeds:
            sdx = seed['x'] - self.x
            sdy = seed['y'] - self.y
            dist = math.sqrt(sdx*sdx + sdy*sdy) or 1.0
            
            if dist < seed['radius']:
                # Lực tác động tỷ lệ nghịch với khoảng cách
                force_ratio = (seed['radius'] - dist) / seed['radius']
                if seed['type'] == 'gravity': # Hố đen hút vào
                    self.vx += (sdx / dist) * force_ratio * 2.5
                    self.vy += (sdy / dist) * force_ratio * 2.5
                elif seed['type'] == 'explosion': # Big Bang đẩy ra
                    self.vx -= (sdx / dist) * force_ratio * 4.0
                    self.vy -= (sdy / dist) * force_ratio * 4.0

        # Cập nhật tọa độ thực tế
        self.vx *= damping
        self.vy *= damping
        self.x += self.vx
        self.y += self.vy

        # Tính toán sai số lệch chuẩn
        self.deviation = math.sqrt((self.tx - self.x)**2 + (self.ty - self.y)**2)


class MultiverseEngine:
    """Bộ khung quản lý và thực thi quá trình Tối ưu hóa Toàn cục Đa vũ trụ."""
    def __init__(self, width=60, height=22):
        self.width = width
        self.height = height
        self.particles = []
        self.chaos_seeds = []
        self.will_power = 0.8  # Từ 0.1 đến 1.0 (Đại diện cho cường độ thực thi)
        self.active_law = 'spiral' # 'spiral' (vòng xoáy) hoặc 'grid' (ma trận ổn định)
        self.step_count = 0
        self.logs = []
        
        self.initialize_universe()

    def add_log(self, text, color=Colors.CYAN):
        """Ghi nhận nhật ký hoạt động hệ thống."""
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"{Colors.BLUE}[{timestamp}]{color} {text}{Colors.ENDC}")
        if len(self.logs) > 6:
            self.logs.pop(0)

    def initialize_universe(self):
        """Thiết lập các hạt về trạng thái hình học tối ưu ban đầu."""
        self.particles = []
        self.chaos_seeds = []
        num_particles = 120
        cx, cy = self.width / 2.0, self.height / 2.0

        if self.active_law == 'spiral':
            # Thiết lập tọa độ mục tiêu theo đường xoắn ốc Fibonacci
            for i in range(num_particles):
                theta = i * 0.35
                r = Math_Map(math.sqrt(i), 0, math.sqrt(num_particles), 1.0, min(cx, cy) * 0.9)
                tx = cx + math.cos(theta) * r * 2.0  # Nhân 2 để bù trừ tỷ lệ ký tự terminal
                ty = cy + math.sin(theta) * r
                self.particles.append(SpaceTimeParticle(i, tx, ty))
                
        elif self.active_law == 'grid':
            # Thiết lập tọa độ mục tiêu theo cấu trúc mạng lưới Hypercube 2D phẳng
            rows = 8
            cols = 15
            spacing_x = self.width / (cols + 1)
            spacing_y = self.height / (rows + 1)
            pid = 0
            for r in range(rows):
                for c in range(cols):
                    tx = (c + 1) * spacing_x
                    ty = (r + 1) * spacing_y
                    self.particles.append(SpaceTimeParticle(pid, tx, ty))
                    pid += 1

        self.add_log(f"Khởi tạo mạng lưới lượng tử thành công dạng [{self.active_law.upper()}]", Colors.GREEN)

    def inject_chaos(self, ctype='explosion'):
        """Tạo ra một hạt nhân hỗn loạn lớn ngay giữa hệ thống."""
        cx = self.width / 2.0 + random.uniform(-5, 5)
        cy = self.height / 2.0 + random.uniform(-2, 2)
        seed = {
            'x': cx,
            'y': cy,
            'type': ctype,
            'radius': 12.0,
            'lifespan': 15 # Tự biến mất sau 15 chu kỳ do Ý chí phục hồi áp chế
        }
        self.chaos_seeds.append(seed)
        
        msg = "BƠM HỖN LOẠN: Vụ nổ Big Bang cục bộ phá vỡ chiều không gian!" if ctype == 'explosion' else "HỐ ĐEN: Siêu trọng lực xé rách màng thời gian!"
        self.add_log(msg, Colors.RED)

    def update(self):
        """Tiến trình cập nhật vật lý lượng tử cho từng hạt."""
        self.step_count += 1
        
        # Cập nhật và lọc các hạt nhân hỗn loạn đã hết hạn
        for seed in self.chaos_seeds[:]:
            seed['lifespan'] -= 1
            if seed['lifespan'] <= 0:
                self.chaos_seeds.remove(seed)
                self.add_log("Ý chí Thực tế đã hấp thụ và triệt tiêu một dị điểm nhiễu loạn.", Colors.YELLOW)

        # Cập nhật từng hạt một
        for p in self.particles:
            p.update(self.will_power, self.chaos_seeds)

    def get_metrics(self):
        """Tính toán các chỉ số hiện trạng của Đa vũ trụ."""
        if not self.particles:
            return 100.0, 0.0
            
        total_dev = sum(p.deviation for p in self.particles)
        avg_dev = total_dev / len(self.particles)
        
        # Chỉ số đồng điệu toàn cục (Alignment)
        alignment = max(0.0, 100.0 - (avg_dev * 8.0))
        entropy = 100.0 - alignment
        return alignment, entropy

    def render(self):
        """Vẽ bản đồ Đa Vũ Trụ bằng ký tự ASCII trực tiếp lên màn hình Console."""
        # Khởi tạo buffer trống
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Vẽ các hạt nhân hỗn loạn nếu có
        for seed in self.chaos_seeds:
            sx, sy = int(seed['x']), int(seed['y'])
            if 0 <= sx < self.width and 0 <= sy < self.height:
                grid[sy][sx] = f"{Colors.RED}X{Colors.ENDC}"

        # Vẽ các hạt lượng tử dựa trên mức độ lệch (Deviation)
        for p in self.particles:
            x, y = int(round(p.x)), int(round(p.y))
            if 0 <= x < self.width and 0 <= y < self.height:
                # Nếu hạt lệch quá xa so với quỹ đạo Ý chí định sẵn
                if p.deviation > 3.0:
                    grid[y][x] = f"{Colors.RED}#{Colors.ENDC}" # Màu đỏ: Đang bị hỗn loạn
                elif p.deviation > 1.0:
                    grid[y][x] = f"{Colors.YELLOW}o{Colors.ENDC}" # Màu vàng: Đang hiệu chỉnh
                else:
                    grid[y][x] = f"{Colors.CYAN}*{Colors.ENDC}" # Màu xanh: Đã tối ưu hoàn mỹ

        # Xuất chuỗi hiển thị
        out = []
        out.append(f"{Colors.BOLD}{Colors.HEADER}=== TRÌNH MÔ PHỎNG Ý CHÍ THỰC TẾ ĐA VŨ TRỤ ==={Colors.ENDC}")
        
        # Vẽ biên trên
        out.append("+" + "-" * self.width + "+")
        for row in grid:
            out.append("|" + "".join(row) + "|")
        # Vẽ biên dưới
        out.append("+" + "-" * self.width + "+")
        
        # Xuất thông số
        alignment, entropy = self.get_metrics()
        out.append(f"{Colors.BOLD}Chu Kỳ: {Colors.YELLOW}{self.step_count:04d}{Colors.ENDC} | "
                   f"Cường độ phục hồi: {Colors.CYAN}{self.will_power*100:.0f}%{Colors.ENDC}")
        out.append(f"Độ Đồng Điệu Toàn Cục: {Colors.GREEN}{alignment:.2f}%{Colors.ENDC} | "
                   f"Entropy Tức Thời: {Colors.RED}{entropy:.2f}%{Colors.ENDC}")
        
        # In bảng nhật ký vận hành vũ trụ
        out.append(f"\n{Colors.UNDERLINE}HỆ THỐNG NHẬT KÝ THỜI GIAN THỰC:{Colors.ENDC}")
        out.extend(self.logs)
        
        return "\n".join(out)


def Math_Map(val, in_min, in_max, out_min, out_max):
    """Hàm phụ trợ chuyển đổi thang đo toán học."""
    if in_max == in_min:
        return out_min
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def Clear_Screen():
    """Làm sạch màn hình Console trên mọi hệ điều hành."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    engine = MultiverseEngine()
    
    try:
        while True:
            Clear_Screen()
            engine.update()
            print(engine.render())
            
            # Khung menu tương tác dưới dạng non-blocking hoặc mô phỏng vòng lặp tự động nhanh
            print(f"\n{Colors.BOLD}Tùy chọn điều khiển (Bấm Ctrl+C để thoát):{Colors.ENDC}")
            print(f"[{Colors.RED}1{Colors.ENDC}] Bơm Vụ Nổ Lượng Tử (Hỗn Loạn)  "
                  f"[{Colors.RED}2{Colors.ENDC}] Tạo Hố Đen Lực Hút")
            print(f"[{Colors.GREEN}3{Colors.ENDC}] Chuyển sang Dạng hình học Spiral  "
                  f"[{Colors.GREEN}4{Colors.ENDC}] Chuyển sang Dạng hình học Grid")
            print(f"[{Colors.YELLOW}5{Colors.ENDC}] Tăng Sức Mạnh Phục Hồi          "
                  f"[{Colors.YELLOW}6{Colors.ENDC}] Giảm Sức Mạnh Phục Hồi")
            print(f"Bất kỳ phím nào khác để tiếp tục bước thời gian kế tiếp...")
            
            # Chờ người dùng nhập liệu trong 0.8 giây, nếu không nhập tự động chạy tiếp bước thời gian
            # Để đơn giản và chạy được trên mọi OS mà không cần thư viện bên ngoài (như msvcrt hay select):
            try:
                import select
                # Kiểm tra xem có ký tự nào được nhập vào stdin không (Chỉ dùng được trên Unix)
                if sys.platform != "win32":
                    i, o, e = select.select([sys.stdin], [], [], 0.8)
                    if i:
                        choice = sys.stdin.readline().strip()
                    else:
                        choice = ""
                else:
                    # Trên Windows, sử dụng cơ chế thủ công tạm dừng nhẹ
                    time.sleep(0.6)
                    choice = ""
            except ImportError:
                # Fallback nếu thiết bị không hỗ trợ thư viện nâng cao
                time.sleep(0.7)
                choice = ""

            # Xử lý lựa chọn của người dùng nếu có
            if choice == '1':
                engine.inject_chaos('explosion')
            elif choice == '2':
                engine.inject_chaos('gravity')
            elif choice == '3':
                engine.active_law = 'spiral'
                engine.initialize_universe()
            elif choice == '4':
                engine.active_law = 'grid'
                engine.initialize_universe()
            elif choice == '5':
                engine.will_power = min(1.0, engine.will_power + 0.1)
                engine.add_log(f"Cường độ ý chí tăng lên: {engine.will_power*100:.0f}%", Colors.YELLOW)
            elif choice == '6':
                engine.will_power = max(0.1, engine.will_power - 0.1)
                engine.add_log(f"Cường độ ý chí giảm xuống: {engine.will_power*100:.0f}%", Colors.YELLOW)
                
    except KeyboardInterrupt:
        Clear_Screen()
        print(f"\n{Colors.GREEN}Hệ thống đóng lại an toàn. Ý chí thực tế tối ưu vẫn tiếp tục vận hành vĩnh hằng.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()

```
