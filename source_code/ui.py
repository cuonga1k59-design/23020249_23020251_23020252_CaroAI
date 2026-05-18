import pygame
from constants import *

pygame.font.init()

def get_font(size, bold=False):
    return pygame.font.SysFont(['segoe ui', 'helvetica', 'arial'], size, bold=bold)

font_title = get_font(40, bold=True)
font_large = get_font(28, bold=True)
font_medium = get_font(22, bold=True)
font_small = get_font(18)
font_coord = get_font(16, bold=True)

class ModernButton:
    def __init__(self, x, y, w, h, text, active_color=ACCENT_BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.active_color = active_color
        self.is_active = False

    def draw(self, screen, mouse_pos):
        is_hovered = self.rect.collidepoint(mouse_pos)
        color = self.active_color if self.is_active else (HOVER_COLOR if is_hovered else BTN_BG)
        txt_color = BG_COLOR if self.is_active else TEXT_COLOR

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surf = font_medium.render(self.text, True, txt_color)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_game_board(screen, board, last_move):
    screen.fill(BG_COLOR)
    
    for c in range(COLS):
        label = font_coord.render(chr(65 + c), True, TEXT_MUTED)
        screen.blit(label, (MARGIN_LEFT + c*SQUARE_SIZE + SQUARE_SIZE//2 - 5, 10))
    for r in range(ROWS):
        label = font_coord.render(str(r + 1), True, TEXT_MUTED)
        screen.blit(label, (10, MARGIN_TOP + r*SQUARE_SIZE + SQUARE_SIZE//2 - 8))

    for c in range(COLS):
        for r in range(ROWS):
            rect = (MARGIN_LEFT + c*SQUARE_SIZE, MARGIN_TOP + r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
            
            if last_move == (r, c):
                pygame.draw.rect(screen, ACCENT_YELLOW, rect, 3)

            center = (MARGIN_LEFT + int(c*SQUARE_SIZE + SQUARE_SIZE/2), MARGIN_TOP + int(r*SQUARE_SIZE + SQUARE_SIZE/2))
            padding = 16
            
            if board[r][c] == PLAYER:
                pygame.draw.line(screen, ACCENT_BLUE, (center[0]-padding, center[1]-padding), (center[0]+padding, center[1]+padding), 5)
                pygame.draw.line(screen, ACCENT_BLUE, (center[0]-padding, center[1]+padding), (center[0]+padding, center[1]-padding), 5)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, ACCENT_RED, center, int(SQUARE_SIZE/2 - padding + 2), 4)

def draw_panel(screen, algo, depth, time_s, nodes, score, turn, msg, mouse_pos, thinking=False, compare_data=None):
    panel_rect = pygame.Rect(BOARD_WIDTH, 0, PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)
    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH, 0), (BOARD_WIDTH, HEIGHT), 2)
    
    screen.blit(font_large.render("ENGINE STATS", True, TEXT_COLOR), (BOARD_WIDTH + 30, 40))
    screen.blit(font_medium.render("State:", True, TEXT_MUTED), (BOARD_WIDTH + 30, 100))
    
    if thinking:
        state_txt = font_medium.render("AI is computing...", True, ACCENT_YELLOW)
    else:
        turn_str = "PLAYER (X)" if turn == PLAYER else "AI (O)"
        color = ACCENT_BLUE if turn == PLAYER else ACCENT_RED
        state_txt = font_medium.render(turn_str, True, color)
    screen.blit(state_txt, (BOARD_WIDTH + 100, 100))
    
    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH + 30, 150), (WIDTH - 30, 150), 1)
    
    # --- XỬ LÝ HIỂN THỊ CHẾ ĐỘ SO SÁNH HOẶC CHẾ ĐỘ THƯỜNG ---
    if compare_data:
        stats = [
            ("Mode:", "COMPARISON BENCHMARK"),
            ("Search Depth:", str(depth)),
            ("Heuristic Score:", str(score)),
            ("", ""), # Dòng trống
            ("Minimax Time:", f"{compare_data['mm_time']:.4f} s"),
            ("Minimax Nodes:", f"{compare_data['mm_nodes']:,}"),
            ("AlphaBeta Time:", f"{compare_data['ab_time']:.4f} s"),
            ("AlphaBeta Nodes:", f"{compare_data['ab_nodes']:,}")
        ]
    else:
        stats = [
            ("Algorithm:", algo),
            ("Search Depth:", str(depth)),
            ("Time Taken:", f"{time_s:.4f} s"),
            ("Nodes Eval:", f"{nodes:,}"),
            ("Heuristic Score:", str(score))
        ]
    
    for i, (lbl, val) in enumerate(stats):
        # Tô màu nổi bật cho thông số AlphaBeta trong chế độ so sánh để dễ đối chiếu
        val_color = ACCENT_GREEN if "AlphaBeta" in lbl else TEXT_COLOR
        screen.blit(font_small.render(lbl, True, TEXT_MUTED), (BOARD_WIDTH + 30, 180 + i*35))
        screen.blit(font_small.render(val, True, val_color), (BOARD_WIDTH + 180, 180 + i*35))

    if msg:
        m_color = ACCENT_GREEN if "PLAYER" in msg else (ACCENT_RED if "AI" in msg else TEXT_COLOR)
        screen.blit(font_large.render(msg, True, m_color), (BOARD_WIDTH + 50, 480))
    
    btn_back = ModernButton(BOARD_WIDTH + 50, HEIGHT - 80, PANEL_WIDTH - 100, 50, "BACK TO MENU", ACCENT_BLUE)
    btn_back.draw(screen, mouse_pos)
    return btn_back
