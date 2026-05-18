# 🎮 Caro AI – Gomoku Artificial Intelligence Project

Dự án xây dựng Trí tuệ nhân tạo (AI) cho game Cờ Caro luật 4 quân liên tiếp thắng bằng ngôn ngữ Python và thư viện Pygame.  
Chương trình sử dụng các thuật toán tìm kiếm đối kháng như Minimax và Alpha-Beta Pruning để mô phỏng khả năng ra quyết định của AI trong môi trường game đối kháng.

---

# ✨ Features

- Giao diện đồ họa Dark Theme hiện đại bằng Pygame
- Hỗ trợ 2 thuật toán:
  - Minimax
  - Alpha-Beta Pruning
- Tùy chỉnh độ sâu tìm kiếm (Depth)
- Dashboard hiển thị:
  - Thời gian suy nghĩ
  - Số node đã duyệt
  - Điểm heuristic
- Chế độ so sánh hiệu năng giữa Minimax và Alpha-Beta
- AI có khả năng:
  - Tấn công
  - Phòng thủ
  - Chặn nước thắng của đối thủ

---

# 📂 Project Structure

```text
source_code/
├── main.py
├── ai_engine.py
├── ui.py
└── constants.py
main.py: Điều khiển game loop và xử lý sự kiện
ai_engine.py: Chứa thuật toán AI và heuristic
ui.py: Xử lý giao diện đồ họa
constants.py: Chứa cấu hình và hằng số
⚙️ Requirements
Python 3.x
Pygame

Cài đặt thư viện bằng lệnh:

pip install -r requirements.txt
🚀 How to Run

Mở terminal tại thư mục project và chạy:

python source_code/main.py
🕹️ How to Play
Người chơi sử dụng chuột để đánh quân X
AI sẽ đánh quân O
Bên nào tạo được 4 quân liên tiếp theo:
hàng ngang
hàng dọc
đường chéo

sẽ giành chiến thắng.

🧠 AI Techniques

Dự án sử dụng các kỹ thuật AI:

Minimax Search
Alpha-Beta Pruning
Move Ordering
Pattern Matching Heuristic
Ray-Casting Win Check
📊 Performance

Alpha-Beta Pruning giúp giảm mạnh số trạng thái cần duyệt so với Minimax truyền thống, từ đó tăng tốc độ phản hồi của AI và cải thiện trải nghiệm thời gian thực.

👨‍💻 Authors
Nguyễn Khắc Cường-23020249
Lê Văn Chiến-23020251
Nguyễn Mạnh Dũng 23020252
