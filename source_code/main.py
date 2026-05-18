import pygame
import sys
import time
import math

from constants import *
from ai_engine import GomokuAI
from ui import font_title, font_medium, ModernButton, draw_game_board, draw_panel

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Caro AI")
    
    ai_engine = GomokuAI()
    state = "MENU"
    board = [[EMPTY]*COLS for _ in range(ROWS)]
    turn = PLAYER
    game_over = False
    game_msg = ""
    last_move = None
    
    algo_name, depth_val = "Compare", 2
    first_turn = PLAYER
    st_time, st_nodes, st_score = 0, 0, 0
    compare_data = None # Biến lưu trữ dữ liệu so sánh 2 AI

    cx = WIDTH // 2
    
    btn_first_p = ModernButton(cx - 220, 150, 200, 45, "PLAYER FIRST")
    btn_first_ai = ModernButton(cx + 20, 150, 200, 45, "AI FIRST")
    btn_first_p.is_active = True

    # Thêm nút Compare Both vào giữa
    btn_mm = ModernButton(cx - 280, 250, 150, 45, "MINIMAX")
    btn_ab = ModernButton(cx - 110, 250, 170, 45, "ALPHA-BETA")
    btn_cmp = ModernButton(cx + 80, 250, 200, 45, "COMPARE BOTH")
    btn_cmp.is_active = True # Mặc định chọn chế độ so sánh
    
    btns_depth = [ModernButton(cx - 220 + i*140, 360, 120, 45, f"DEPTH {i+1}") for i in range(3)]
    btns_depth[1].is_active = True
    
    btn_start = ModernButton(cx - 125, 460, 250, 60, "START GAME", ACCENT_GREEN)

    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        if state == "MENU":
            screen.fill(PANEL_COLOR)
            title_surf = font_title.render("CARO AI", True, TEXT_COLOR)
            title_rect = title_surf.get_rect(centerx=cx, top=50)
            screen.blit(title_surf, title_rect)
            
            screen.blit(font_medium.render("Who Goes First ?:", True, TEXT_MUTED), (cx - 85, 115))
            screen.blit(font_medium.render("Select Search Algorithm:", True, TEXT_MUTED), (cx - 130, 215))
            screen.blit(font_medium.render("Select Search Depth:", True, TEXT_MUTED), (cx - 110, 325))
            
            for btn in [btn_first_p, btn_first_ai, btn_mm, btn_ab, btn_cmp] + btns_depth + [btn_start]:
                btn.draw(screen, mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if btn_first_p.is_clicked(mouse_pos):
                        btn_first_p.is_active, btn_first_ai.is_active = True, False
                        first_turn = PLAYER
                    if btn_first_ai.is_clicked(mouse_pos):
                        btn_first_ai.is_active, btn_first_p.is_active = True, False
                        first_turn = AI
                        
                    # Chọn thuật toán
                    if btn_mm.is_clicked(mouse_pos):
                        btn_mm.is_active, btn_ab.is_active, btn_cmp.is_active = True, False, False
                        algo_name = "Minimax"
                    if btn_ab.is_clicked(mouse_pos):
                        btn_ab.is_active, btn_mm.is_active, btn_cmp.is_active = True, False, False
                        algo_name = "Alpha-Beta"
                    if btn_cmp.is_clicked(mouse_pos):
                        btn_cmp.is_active, btn_mm.is_active, btn_ab.is_active = True, False, False
                        algo_name = "Compare"
                        
                    if btn_start.is_clicked(mouse_pos):
                        state, board, game_over, game_msg, last_move = "GAME", [[EMPTY]*COLS for _ in range(ROWS)], False, "", None
                        turn = first_turn
                        st_time, st_nodes, st_score = 0, 0, 0
                        compare_data = None
                        
                    for i, b in enumerate(btns_depth):
                        if b.is_clicked(mouse_pos):
                            for x in btns_depth: x.is_active = False
                            b.is_active = True
                            depth_val = i + 1

        elif state == "GAME":
            draw_game_board(screen, board, last_move)
            btn_back = draw_panel(screen, algo_name, depth_val, st_time, st_nodes, st_score, turn, game_msg, mouse_pos, False, compare_data)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_back.is_clicked(mouse_pos): state = "MENU"
                    if not game_over and turn == PLAYER:
                        c = (mouse_pos[0] - MARGIN_LEFT) // SQUARE_SIZE
                        r = (mouse_pos[1] - MARGIN_TOP) // SQUARE_SIZE
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == EMPTY:
                            board[r][c] = PLAYER
                            last_move = (r, c)
                            if ai_engine.check_win(board, PLAYER): 
                                game_msg, game_over = "PLAYER WINS!", True
                            elif not ai_engine.get_valid_moves(board): 
                                game_msg, game_over = "DRAW!", True
                            else: 
                                turn = AI

            if not game_over and turn == AI:
                draw_panel(screen, algo_name, depth_val, st_time, st_nodes, st_score, turn, game_msg, mouse_pos, True, compare_data)
                pygame.display.update() 
                
                if algo_name == "Compare":
                    # 1. Chạy ngầm Minimax trước để lấy số liệu (Không áp dụng nước đi)
                    ai_engine.nodes_evaluated = 0
                    start_t = time.time()
                    ai_engine.minimax(board, depth_val, True)
                    mm_time = time.time() - start_t
                    mm_nodes = ai_engine.nodes_evaluated
                    
                    # 2. Chạy Alpha-Beta để lấy nước đi chính thức và số liệu
                    ai_engine.nodes_evaluated = 0
                    start_t = time.time()
                    m, st_score = ai_engine.alphabeta(board, depth_val, -math.inf, math.inf, True)
                    ab_time = time.time() - start_t
                    ab_nodes = ai_engine.nodes_evaluated
                    
                    # Đóng gói dữ liệu để vẽ lên Panel
                    compare_data = {
                        'mm_time': mm_time, 'mm_nodes': mm_nodes,
                        'ab_time': ab_time, 'ab_nodes': ab_nodes
                    }
                else:
                    compare_data = None
                    ai_engine.nodes_evaluated = 0
                    start_t = time.time()
                    if algo_name == "Minimax":
                        m, st_score = ai_engine.minimax(board, depth_val, True)
                    else:
                        m, st_score = ai_engine.alphabeta(board, depth_val, -math.inf, math.inf, True)
                    st_time = time.time() - start_t
                    st_nodes = ai_engine.nodes_evaluated
                
                # Áp dụng nước cờ
                if m:
                    board[m[0]][m[1]] = AI
                    last_move = m
                    if ai_engine.check_win(board, AI): 
                        game_msg, game_over = "ENGINE WINS!", True
                    elif not ai_engine.get_valid_moves(board): 
                        game_msg, game_over = "DRAW!", True
                turn = PLAYER

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
