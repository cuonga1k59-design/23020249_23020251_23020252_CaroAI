import math
from constants import *

class GomokuAI:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.nodes_evaluated = 0 # Biến đếm số lượng trạng thái (node) AI đã duyệt qua

    # ---------------------------------------------------------
    # HÀM TỐI ƯU 1: SINH NƯỚC ĐI HỢP LỆ VÀ SẮP XẾP (MOVE ORDERING)
    # ---------------------------------------------------------
    def get_valid_moves(self, board):
        moves = set() # Dùng kiểu Set để tự động loại bỏ các ô bị trùng lặp
        has_piece = False # Cờ kiểm tra xem bàn cờ đã có quân nào chưa
        
        # Quét toàn bộ bàn cờ để tìm các quân cờ ĐÃ ĐƯỢC ĐÁNH
        for r in range(self.rows):
            for c in range(self.cols):
                if board[r][c] != EMPTY:
                    has_piece = True
                    # Nếu thấy 1 quân cờ, tìm các ô trống xung quanh nó (bán kính 1 ô)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue # Bỏ qua chính nó
                            nr, nc = r + dr, c + dc
                            # Nếu ô xung quanh nằm trong bàn cờ và đang trống -> Đưa vào danh sách duyệt
                            if 0 <= nr < self.rows and 0 <= nc < self.cols and board[nr][nc] == EMPTY:
                                moves.add((nr, nc))
        
        # Nếu bàn cờ trống trơn, trả về duy nhất 1 nước đi ở chính giữa bàn cờ (tiết kiệm thời gian)
        if not has_piece: 
            return [(self.rows//2, self.cols//2)]
            
        # [QUAN TRỌNG]: Chuyển Set về List để sắp xếp (Move Ordering)
        moves = list(moves)
        center_r, center_c = self.rows // 2, self.cols // 2
        
        # Sắp xếp các nước đi ưu tiên gần khu vực trung tâm bàn cờ nhất.
        # Điều này giúp Alpha-Beta Pruning tìm thấy nhánh tốt sớm hơn và cắt tỉa nhánh xấu nhanh hơn rấy nhiều.
        moves.sort(key=lambda m: abs(m[0] - center_r) + abs(m[1] - center_c))
        return moves

    # ---------------------------------------------------------
    # HÀM TRÍCH XUẤT CHUỖI ĐỂ TÍNH ĐIỂM
    # ---------------------------------------------------------
    def get_all_lines(self, board):
        lines = []
        # Nối các phần tử trên cùng 1 Hàng ngang thành 1 chuỗi string (vd: "01020")
        for r in range(self.rows):
            lines.append("".join(str(x) for x in board[r]))
        
        # Nối các phần tử trên cùng 1 Cột dọc thành 1 chuỗi string
        for c in range(self.cols):
            lines.append("".join(str(board[r][c]) for r in range(self.rows)))
        
        # Trích xuất các đường Chéo Chính (Từ trên-trái xuống dưới-phải)
        for start_col in range(self.cols - 3):
            lines.append("".join(str(board[i][start_col+i]) for i in range(min(self.rows, self.cols - start_col))))
        for start_row in range(1, self.rows - 3):
            lines.append("".join(str(board[start_row+i][i]) for i in range(min(self.rows - start_row, self.cols))))
            
        # Trích xuất các đường Chéo Phụ (Từ trên-phải xuống dưới-trái)
        for start_col in range(3, self.cols):
            lines.append("".join(str(board[i][start_col-i]) for i in range(min(self.rows, start_col + 1))))
        for start_row in range(1, self.rows - 3):
            lines.append("".join(str(board[start_row+i][self.cols-1-i]) for i in range(min(self.rows - start_row, self.cols))))
            
        return lines

    # ---------------------------------------------------------
    # HÀM TỐI ƯU 2: KIỂM TRA THẮNG BẰNG RAY-CASTING 4 HƯỚNG
    # ---------------------------------------------------------
    def check_win(self, board, piece):
        # Quét bàn cờ, nếu thấy quân cờ của phe đang xét (piece) thì bắt đầu "phóng tia"
        for r in range(self.rows):
            for c in range(self.cols):
                if board[r][c] == piece:
                    # 4 hướng Vector: Ngang (0,1), Dọc (1,0), Chéo Xuống (1,1), Chéo Lên (1,-1)
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        count = 1 # Tính chính nó là 1
                        # Đi tiếp 3 bước nữa theo hướng hiện tại
                        for i in range(1, 4):
                            nr, nc = r + dr * i, c + dc * i
                            # Nếu 3 ô tiếp theo vẫn là quân cờ đó -> tăng biến đếm
                            if 0 <= nr < self.rows and 0 <= nc < self.cols and board[nr][nc] == piece:
                                count += 1
                            else:
                                break # Bị đứt chuỗi thì dừng hướng này
                        # Nếu đủ 4 quân thì xác nhận thắng ngay lập tức
                        if count >= 4:
                            return True
        return False

    # ---------------------------------------------------------
    # HÀM ĐÁNH GIÁ TĨNH (HEURISTIC)
    # ---------------------------------------------------------
    def evaluate_board(self, board, piece):
        score = 0
        opp = PLAYER if piece == AI else AI # Xác định phe địch
        
        p_str = str(piece)
        o_str = str(opp)
        
        # Khai báo các mô hình (pattern) dưới dạng String
        win_p = p_str * 4                          # 4 quân liên tiếp
        open3_p = "0" + p_str * 3 + "0"            # Hở 2 đầu (VD: 02220)
        closed3_p1 = o_str + p_str * 3 + "0"       # Bị chặn đầu trái (VD: 12220)
        closed3_p2 = "0" + p_str * 3 + o_str       # Bị chặn đầu phải (VD: 02221)
        open2_p = "0" + p_str * 2 + "0"            # Hai quân hở 2 đầu (VD: 0220)
        
        # Mô hình của phe địch
        win_o = o_str * 4
        open3_o = "0" + o_str * 3 + "0"
        closed3_o1 = p_str + o_str * 3 + "0"
        closed3_o2 = "0" + o_str * 3 + p_str
        open2_o = "0" + o_str * 2 + "0"

        # Gọi hàm get_all_lines để lấy tất cả các chuỗi có trên bàn cờ
        lines = self.get_all_lines(board)
        
        for line in lines:
            # 1. CỘNG ĐIỂM TẤN CÔNG (Dành cho quân mình)
            if win_p in line: score += 1000000     # Nếu có 4 -> Vô địch
            score += line.count(open3_p) * 50000   # Nếu có Hở 3 -> Rất mạnh
            score += (line.count(closed3_p1) + line.count(closed3_p2)) * 5000 # Nếu chặn 1 đầu -> Tạm ổn
            score += line.count(open2_p) * 1000    # Nếu Hở 2 -> Tiềm năng
            
            # 2. TRỪ ĐIỂM PHÒNG NGỰ (Sợ địch thắng nên phải chặn)
            if win_o in line: score -= 1000000     # Nếu địch có 4 -> Thua chắc
            score -= line.count(open3_o) * 80000   # Trừ cực nặng nếu địch có Hở 3 (Ưu tiên thủ hơn công)
            score -= (line.count(closed3_o1) + line.count(closed3_o2)) * 8000
            score -= line.count(open2_o) * 1500

        return score

    # Hàm kiểm tra xem đã đến trạng thái dừng chưa (Thắng, Thua, hoặc Hết bàn cờ)
    def is_terminal(self, board):
        return self.check_win(board, AI) or self.check_win(board, PLAYER) or not self.get_valid_moves(board)

    # ---------------------------------------------------------
    # THUẬT TOÁN MINIMAX (VÉT CẠN)
    # ---------------------------------------------------------
    def minimax(self, board, depth, maximizingPlayer):
        self.nodes_evaluated += 1
        terminal = self.is_terminal(board)
        
        # ĐIỀU KIỆN DỪNG: Nếu chạm đáy (depth = 0) hoặc kết thúc game
        if depth == 0 or terminal:
            if terminal:
                # [SỬA LỖI LAZY WIN]: Cộng thêm depth để AI hiểu: Thắng nhanh thì tốt hơn, thua chậm thì tốt hơn.
                if self.check_win(board, AI): return (None, 10**8 + depth) 
                if self.check_win(board, PLAYER): return (None, -10**8 - depth)
                return (None, 0) # Hòa
            return (None, self.evaluate_board(board, AI)) # Nếu depth=0, dùng hàm Heuristic để chấm điểm
        
        moves = self.get_valid_moves(board)
        
        if maximizingPlayer: # LƯỢT CỦA AI (Tìm điểm số lớn nhất)
            value = -math.inf
            best_m = moves[0]
            for m in moves:
                board[m[0]][m[1]] = AI # Đi thử
                score = self.minimax(board, depth-1, False)[1] # Đệ quy xuống lượt của người chơi
                board[m[0]][m[1]] = EMPTY # Rút cờ (Backtracking)
                if score > value: 
                    value = score
                    best_m = m
            return best_m, value
            
        else: # LƯỢT CỦA NGƯỜI CHƠI (Tìm điểm số nhỏ nhất để AI chịu thiệt nhất)
            value = math.inf
            best_m = moves[0]
            for m in moves:
                board[m[0]][m[1]] = PLAYER # Người chơi đi thử
                score = self.minimax(board, depth-1, True)[1] # Đệ quy lên lượt AI
                board[m[0]][m[1]] = EMPTY # Rút cờ
                if score < value: 
                    value = score
                    best_m = m
            return best_m, value

    # ---------------------------------------------------------
    # THUẬT TOÁN ALPHA-BETA PRUNING (CẮT TỈA TỐI ƯU NHÁNH)
    # ---------------------------------------------------------
    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        self.nodes_evaluated += 1
        terminal = self.is_terminal(board)
        
        if depth == 0 or terminal:
            if terminal:
                if self.check_win(board, AI): return (None, 10**8 + depth)
                if self.check_win(board, PLAYER): return (None, -10**8 - depth)
                return (None, 0)
            return (None, self.evaluate_board(board, AI))

        moves = self.get_valid_moves(board)
        
        if maximizingPlayer: # Lượt AI
            value = -math.inf
            best_m = moves[0]
            for m in moves:
                board[m[0]][m[1]] = AI
                score = self.alphabeta(board, depth-1, alpha, beta, False)[1]
                board[m[0]][m[1]] = EMPTY
                
                if score > value: 
                    value = score
                    best_m = m
                
                # CẬP NHẬT ALPHA VÀ CẮT NHÁNH
                alpha = max(alpha, value) # Cập nhật mức điểm thấp nhất mà AI chắc chắn nhận được
                if alpha >= beta: # Nếu Alpha >= Beta, nhánh này đã quá tệ với người chơi, người chơi sẽ không bao giờ chọn nhánh này -> CẮT (Dừng vòng lặp)
                    break 
            return best_m, value
            
        else: # Lượt Người chơi
            value = math.inf
            best_m = moves[0]
            for m in moves:
                board[m[0]][m[1]] = PLAYER
                score = self.alphabeta(board, depth-1, alpha, beta, True)[1]
                board[m[0]][m[1]] = EMPTY
                
                if score < value: 
                    value = score
                    best_m = m
                    
                # CẬP NHẬT BETA VÀ CẮT NHÁNH
                beta = min(beta, value) # Cập nhật mức điểm cao nhất mà Người chơi chắc chắn nhận được
                if alpha >= beta: # Cắt tỉa tương tự như trên
                    break 
            return best_m, value
