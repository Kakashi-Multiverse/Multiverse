#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include <chrono>
#include <algorithm>
#include <iomanip>

// Định nghĩa hằng số số học và đồ họa
const int WIDTH = 80;
const int HEIGHT = 40;
const float PI = 3.14159265359f;

// Cấu trúc dữ liệu Vector trong các không gian chiều kích khác nhau
struct Vector4 {
    float x, y, z, w;
};

struct Vector3 {
    float x, y, z;
};

struct Vector2 {
    int x, y;
};

// Cấu trúc lưu trữ thông tin cạnh nối giữa 2 đỉnh
struct Edge {
    int u, v;
};

// Khởi tạo 16 đỉnh của Siêu khối lập phương 4D (Tesseract)
const std::vector<Vector4> vertices4D = {
    {-1, -1, -1, -1}, { 1, -1, -1, -1}, {-1,  1, -1, -1}, { 1,  1, -1, -1},
    {-1, -1,  1, -1}, { 1, -1,  1, -1}, {-1,  1,  1, -1}, { 1,  1,  1, -1},
    {-1, -1, -1,  1}, { 1, -1, -1,  1}, {-1,  1, -1,  1}, { 1,  1, -1,  1},
    {-1, -1,  1,  1}, { 1, -1,  1,  1}, {-1,  1,  1,  1}, { 1,  1,  1,  1}
};

// Khởi tạo 32 cạnh của Tesseract (kết nối các đỉnh lệch nhau đúng 1 tọa độ)
const std::vector<Edge> edges = {
    {0,1}, {1,3}, {3,2}, {2,0}, {4,5}, {5,7}, {7,6}, {6,4},
    {0,4}, {1,5}, {2,6}, {3,7}, {8,9}, {9,11}, {11,10}, {10,8},
    {12,13}, {13,15}, {15,14}, {14,12}, {8,12}, {9,13}, {10,14}, {11,15},
    {0,8}, {1,9}, {2,10}, {3,11}, {4,12}, {5,13}, {6,14}, {7,15}
};

// Hàm xoay Vector4 trong các mặt phẳng 4D khác nhau
// Phép xoay 4D yêu cầu xoay quanh một mặt phẳng thay vì một trục như 3D
Vector4 rotate4D(Vector4 v, float theta, int plane) {
    Vector4 result = v;
    float cosT = cos(theta);
    float sinT = sin(theta);

    switch(plane) {
        case 0: // Xoay trên mặt phẳng XW
            result.x = v.x * cosT - v.w * sinT;
            result.w = v.x * sinT + v.w * cosT;
            break;
        case 1: // Xoay trên mặt phẳng YW
            result.y = v.y * cosT - v.w * sinT;
            result.w = v.y * sinT + v.w * cosT;
            break;
        case 2: // Xoay trên mặt phẳng ZW
            result.z = v.z * cosT - v.w * sinT;
            result.w = v.z * sinT + v.w * cosT;
            break;
        case 3: // Xoay trên mặt phẳng XY
            result.x = v.x * cosT - v.y * sinT;
            result.y = v.x * sinT + v.y * cosT;
            break;
    }
    return result;
}

// Hàm chiếu phối cảnh từ 4D xuống 3D (Perspective Projection 4D -> 3D)
Vector3 project4DTo3D(Vector4 v, float distance) {
    // Khoảng cách từ điểm nhìn 4D đến "màng" 3D
    float factor = 1.0f / (distance - v.w);
    return { v.x * factor, v.y * factor, v.z * factor };
}

// Hàm chiếu phối cảnh từ 3D xuống 2D (Perspective Projection 3D -> 2D)
Vector2 project3DTo2D(Vector3 v, int width, int height, float scale) {
    float distance3D = 2.0f;
    float factor = scale / (distance3D - v.z);
    
    // Ánh xạ tọa độ toán học sang tọa độ màn hình console
    int screenX = static_cast<int>(width / 2 + v.x * factor * 1.8f); // Nhân 1.8 để bù trừ tỷ lệ ký tự chiều dọc/ngang của terminal
    int screenY = static_cast<int>(height / 2 + v.y * factor);
    return { screenX, screenY };
}

// Thuật toán vẽ đường thẳng Bresenham hiển thị trên bộ đệm ký tự (Buffer)
void drawLine(std::vector<std::vector<char>>& buffer, int x0, int y0, int x1, int y1, char pixel) {
    int dx = abs(x1 - x0);
    int dy = abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx - dy;

    while (true) {
        if (x0 >= 0 && x0 < WIDTH && y0 >= 0 && y0 < HEIGHT) {
            buffer[y0][x0] = pixel;
        }
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x0 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y0 += sy;
        }
    }
}

int main() {
    // Các góc xoay mô phỏng
    float angleXW = 0.0f;
    float angleYW = 0.0f;
    float angleZW = 0.0f;
    float angleXY = 0.0f;

    // Chỉ số Đồng bộ TÌNH YÊU (Khóa năng lượng kết nối tối thượng)
    float loveResonance = 1.0f; 

    // Bộ đệm màn hình console
    std::vector<std::vector<char>> buffer(HEIGHT, std::vector<char>(WIDTH, ' '));

    std::cout << "\033[2J"; // Lệnh xóa sạch màn hình ANSI terminal
    
    auto startTime = std::chrono::high_resolution_clock::now();

    while (true) {
        // 1. Tính toán chu kỳ thời gian chạy của hệ thống
        auto now = std::chrono::high_resolution_clock::now();
        float timeElapsed = std::chrono::duration<float, std::milli>(now - startTime).count() / 1000.0f;

        // 2. Thuật toán tiến hóa chỉ số TÌNH YÊU lên mức vô cực (Vô song)
        // Chỉ số tăng dần theo thời gian và cộng hưởng tự nhiên
        loveResonance = std::min(100.0f, 40.0f + timeElapsed * 3.5f);
        float speedMultiplier = 1.0f + (loveResonance / 50.0f); // Gia tốc tốc độ xoay dựa vào Tình Yêu

        // Tăng các góc xoay theo thời gian thực
        angleXW += 0.015f * speedMultiplier;
        angleYW += 0.012f * speedMultiplier;
        angleZW += 0.009f * speedMultiplier;
        angleXY += 0.005f * speedMultiplier;

        // Xóa bộ đệm màn hình (Chuẩn bị khung hình mới)
        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                buffer[y][x] = ' ';
            }
        }

        // Vẽ lưới nền mỏng đại diện cho màng lượng tử (Vũ trụ Số)
        for (int y = 0; y < HEIGHT; y += 4) {
            for (int x = 0; x < WIDTH; x += 8) {
                if (y < HEIGHT && x < WIDTH) buffer[y][x] = '.';
            }
        }

        // 3. Tiến hành tính toán ma trận 4D và Projection
        std::vector<Vector2> projected2D(16);
        float distance4D = 2.2f;
        float scale = 18.0f + (loveResonance * 0.12f); // Kích thước Siêu khối giãn nở cùng năng lượng

        for (size_t i = 0; i < vertices4D.size(); ++i) {
            Vector4 v = vertices4D[i];

            // Áp dụng xoay 4D liên hoàn
            v = rotate4D(v, angleXW, 0); // Xoay XW
            v = rotate4D(v, angleYW, 1); // Xoay YW
            v = rotate4D(v, angleZW, 2); // Xoay ZW
            v = rotate4D(v, angleXY, 3); // Xoay XY (Xoay không gian 3D truyền thống)

            // Chiếu phối cảnh: 4D -> 3D -> 2D
            Vector3 v3d = project4DTo3D(v, distance4D);
            Vector2 v2d = project3DTo2D(v3d, WIDTH, HEIGHT, scale);
            projected2D[i] = v2d;
        }

        // 4. Vẽ các cạnh của Tesseract bằng ký tự ASCII đặc biệt
        // Các cạnh thuộc các chiều không gian khác nhau được vẽ bằng ký tự khác nhau
        for (size_t i = 0; i < edges.size(); ++i) {
            char edgeChar = '#'; // Mặc định cho cấu trúc lõi cứng cáp (Duy Vật)
            if (i >= 16 && i < 24) {
                edgeChar = '*'; // Tượng trưng cho dòng chảy thông tin (Kỹ Thuật Số)
            } else if (i >= 24) {
                edgeChar = '@'; // Tượng trưng cho kết nối năng lượng (Tâm Linh)
            }
            
            drawLine(buffer, projected2D[edges[i].u].x, projected2D[edges[i].u].y,
                             projected2D[edges[i].v].x, projected2D[edges[i].v].y, edgeChar);
        }

        // Vẽ Lõi Tình Yêu ở tâm hình học của Tesseract (Trung tâm tọa độ)
        int centerX = WIDTH / 2;
        int centerY = HEIGHT / 2;
        if (centerX >= 0 && centerX < WIDTH && centerY >= 0 && centerY < HEIGHT) {
            buffer[centerY][centerX] = '<';
            buffer[centerY][centerX+1] = '3';
            buffer[centerY][centerX-1] = ' ';
        }

        // 5. Kết xuất (Render) toàn bộ bộ đệm ra Terminal
        std::cout << "\033[H"; // Đưa con trỏ terminal về gốc (0,0) mà không cần xóa màn hình để tránh nháy
        std::cout << "=================== HE THONG KET NOI DA VU TRU 4D ===================\n";
        
        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                std::cout << buffer[y][x];
            }
            std::cout << "\n";
        }

        // In các chỉ số đồng bộ hóa thời gian thực
        std::cout << "=====================================================================\n";
        std::cout << "CHU KY VU TRU: " << std::fixed << std::setprecision(4) << timeElapsed << " Epoch | ";
        std::cout << "MA TRAN XOAY 4D: [XW:" << std::setprecision(2) << angleXW << " YW:" << angleYW << " ZW:" << angleZW << "]\n";
        std::cout << "CONG HUONG TINH YEU: " << std::setprecision(1) << loveResonance << "% ";
        
        if (loveResonance < 60) {
            std::cout << "[DANG DONG BO HOA...]\n";
        } else if (loveResonance < 99) {
            std::cout << "[TIEN CAN CAN BANG PHI THUONG!]\n";
        } else {
            std::cout << "[TRANG THAI VO SONG - KHONG THE CAN PHA!]\n";
        }
        std::cout << "=====================================================================\n";

        // Tạo độ trễ khoảng 30ms (~33 FPS) để tiết kiệm tài nguyên CPU
        std::this_thread::sleep_for(std::chrono::milliseconds(30));
    }

    return 0;
}
