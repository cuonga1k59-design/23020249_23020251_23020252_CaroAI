# ==========================================
# CẤU HÌNH GIAO DIỆN VÀ MÀU SẮC (THEME)
# ==========================================
BG_COLOR = (30, 30, 46)          # Màu nền chính
PANEL_COLOR = (24, 24, 37)       # Màu nền bảng thống kê
GRID_COLOR = (88, 91, 112)       # Màu đường kẻ lưới bàn cờ
TEXT_COLOR = (205, 214, 244)     # Màu chữ chính
TEXT_MUTED = (166, 173, 200)     # Màu chữ phụ (mờ hơn)
ACCENT_BLUE = (137, 180, 250)    # Màu xanh cho quân X
ACCENT_GREEN = (166, 227, 161)   # Màu xanh lá cho nút Bắt đầu / Thông báo thắng
ACCENT_RED = (243, 139, 168)     # Màu đỏ/hồng cho quân O
ACCENT_YELLOW = (249, 226, 175)  # Màu vàng làm nổi bật nước đi cuối cùng
BTN_BG = (49, 50, 68)            # Màu nền nút bấm mặc định
HOVER_COLOR = (69, 71, 90)       # Màu nền nút bấm khi di chuột vào

# ==========================================
# CẤU HÌNH BÀN CỜ VÀ KÍCH THƯỚC CỬA SỔ
# ==========================================
ROWS = 10                        # Số hàng
COLS = 10                        # Số cột
SQUARE_SIZE = 60                 # Kích thước mỗi ô vuông (pixel)
MARGIN_LEFT = 40                 # Lề trái của bàn cờ
MARGIN_TOP = 40                  # Lề trên của bàn cờ
BOARD_WIDTH = COLS * SQUARE_SIZE + MARGIN_LEFT + 20   # Chiều rộng khu vực bàn cờ
BOARD_HEIGHT = ROWS * SQUARE_SIZE + MARGIN_TOP + 20   # Chiều cao khu vực bàn cờ
PANEL_WIDTH = 350                # Chiều rộng khu vực thống kê bên phải
WIDTH = BOARD_WIDTH + PANEL_WIDTH                     # Tổng chiều rộng cửa sổ
HEIGHT = max(BOARD_HEIGHT, 650)                       # Tổng chiều cao cửa sổ (tối thiểu 650px)

# ==========================================
# ĐỊNH NGHĨA QUÂN CỜ
# ==========================================
PLAYER = 1 # Đại diện cho quân X (Người chơi)
AI = 2     # Đại diện cho quân O (Máy)
EMPTY = 0  # Ô trống
