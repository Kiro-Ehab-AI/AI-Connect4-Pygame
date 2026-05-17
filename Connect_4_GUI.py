import numpy as np
import pygame
import sys
import math
import time

BOARD_COLOR = (0, 105, 148) 
BG_COLOR = (0, 48, 73)
PLAYER_COLOR = (244, 241, 222)
AI_COLOR = (231, 111, 81)

ROWS = 6

COLS = 7

PLAYER_PIECE = 1
AI_PIECE = 2

def create_board(): # function no1 : creates a 6x7 board filled with zeros #kiro
    return np.zeros((ROWS, COLS))

def is_valid_location(board, col): # function no2 : checks if a column is valid for placing a piece #kiro
    return board[0][col] == 0

def get_next_open_row(board, col): # function no3 : finds the next open row in a given column, starting from the bottom #kiro
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def drop_piece(board, row, col, piece): # function no4 : places a piece in the specified location on the board #kiro
    board[row][col] = piece

def print_pretty_board(board):
    print("\n   0    1    2    3    4    5    6") # أرقام الأعمدة # kiro
    print("-------------------------------------")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            if board[r][c] == 1:
                row_str += " ⚪ |"  # الإنسان
            elif board[r][c] == 2:
                row_str += " 🔴 |"  #  AI ال
            else:
                row_str += "    |"  # فاضي 
        print(row_str)
        print("-------------------------------------")


def draw_board(board, screen): # mina
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BOARD_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BG_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLS):
        for r in range(ROWS):       
            if board[r][c] == 1: # Human
                pygame.draw.circle(screen, PLAYER_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: # AI
                pygame.draw.circle(screen, AI_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def draw_text_with_shadow(text, color): # mina
 
    pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE))
    
    
    shadow = myfont.render(text, 1, (50, 50, 50)) 

    shadow_rect = shadow.get_rect(center=(board_width//2 + 2, SQUARESIZE//2 + 2))
    screen.blit(shadow, shadow_rect)
    
    
    label = myfont.render(text, 1, color)
    
    label_rect = label.get_rect(center=(board_width//2, SQUARESIZE//2))
    screen.blit(label, label_rect)
    
    pygame.display.update()


def draw_stats_panel(ai_col, score, nodes, time_ms): #kiro
    
    pygame.draw.rect(screen, BG_COLOR, (board_width, 0, PANEL_WIDTH, height))
    
    pygame.draw.line(screen, BOARD_COLOR, (board_width, 0), (board_width, height), 6)
    
    
    title = title_font.render("AI STATS", 1, AI_COLOR)
    screen.blit(title, (board_width + 80, 40))
    pygame.draw.line(screen, BOARD_COLOR, (board_width + 50, 90), (board_width + 300, 90), 2)

    
    screen.blit(panel_font.render("Column:", 1, PLAYER_COLOR), (board_width + 20, 150))
    screen.blit(panel_font.render(str(ai_col), 1, AI_COLOR), (board_width + 160, 150))
    
    
    screen.blit(panel_font.render("Score:", 1, PLAYER_COLOR), (board_width + 20, 230))
    screen.blit(panel_font.render(str(score), 1, AI_COLOR), (board_width + 160, 230))
    
    
    screen.blit(panel_font.render("Nodes:", 1, PLAYER_COLOR), (board_width + 20, 310))
    screen.blit(panel_font.render(str(nodes), 1, AI_COLOR), (board_width + 160, 310))
    
    
    screen.blit(panel_font.render("Time:", 1, PLAYER_COLOR), (board_width + 20, 390))
    if isinstance(time_ms, str):
        screen.blit(panel_font.render(time_ms, 1, AI_COLOR), (board_width + 160, 390))
    else:
        screen.blit(panel_font.render(f"{time_ms:.1f} ms", 1, AI_COLOR), (board_width + 160, 390))
    
    pygame.display.update()


def draw_game_summary(moves, depth):  # mina
    
    pygame.draw.line(screen, BOARD_COLOR, (board_width + 40, 480), (board_width + 310, 480), 2)
    
    
    title = title_font.render("SUMMARY", 1, AI_COLOR)
    screen.blit(title, (board_width + 90, 500))
    
    
    screen.blit(panel_font.render("Total Moves:", 1, PLAYER_COLOR), (board_width + 15, 570))
    screen.blit(panel_font.render(str(moves), 1, AI_COLOR), (board_width + 220, 570))
    
    screen.blit(panel_font.render("Final Depth:", 1, PLAYER_COLOR), (board_width + 15, 630))
    screen.blit(panel_font.render(str(depth), 1, AI_COLOR), (board_width + 220, 630))
    
    pygame.display.update()


def draw_start_screen(): # mina
    screen.fill(BG_COLOR) 
    
    
    title = title_font.render("SELECT AI DEPTH (1 - 6)", 1, PLAYER_COLOR)
    screen.blit(title, (width//2 - title.get_width()//2, height//3))

    
    for i in range(1, 7):
        
        cx = (width // 2) - 350 + (i * 100)
        cy = height // 2 + 50
        
        
        pygame.draw.circle(screen, BOARD_COLOR, (cx, cy), RADIUS)
        
        
        num_lbl = title_font.render(str(i), 1, AI_COLOR)
        screen.blit(num_lbl, (cx - num_lbl.get_width()//2, cy - num_lbl.get_height()//2))
        
    pygame.display.update()






def Check_Win(board,piece):
    # Horizontal
    for r in range(ROWS):
          for c in range(COLS-3):
               if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                    return True
    # Vertical
    for c in range(COLS):
         for r in range(ROWS-3):
              if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                   return True
    # Diagonal from up to down and from left to right
    for r in range(ROWS-3):
         for c in range(COLS-3) :
              if board[r][c]==piece and board[r+1][c+1]==piece  and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                     return True
    # Diagonal from down to up and from rigth to left
    for r in range(3,ROWS):
         for c in range (COLS-3):
              if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                   return True
    return False                            


def Check_Draw(board):
    for col in range(COLS):
          if is_valid_location(board,col):
               return False
    return True
 #board state بترجع ال
def is_terminal(board):
     return Check_Draw(board) or Check_Win(board, 1) or Check_Win(board, 2)

def evaluation_function(window,player,opponent):
    score = 0
    player_pieces = window.count(player)
    opponent_pieces = window.count(opponent)
    empty = window.count(0)

    #4 in a Row/Winning move
    if player_pieces == 4:
        score += 100
    elif opponent_pieces == 4:
        score -= 100

    #3 in a Row(open)
    elif player_pieces == 3 and empty == 1:
        score += 5 # فرصة فوز في الخطوة الجاية
    elif opponent_pieces == 3 and empty == 1:
        score -= 4   #Blocking the opponent

    #2 in a Row(open)
    elif player_pieces == 2 and empty == 2:
        score += 2
    elif opponent_pieces == 2 and empty == 2:  
        score -= 2

    return score    

def heuristic_Score(board,piece):
    score = 0
    opponent = 3 - piece

    for row in range(6): 
        for col in range(7): 
            # Horizontal
            if col + 3 < 7:
                window = []
                for i in range(4):
                    window.append(board[row][col + i])
                score += evaluation_function(window,piece,opponent)

            # Vertical
            if row + 3 < 6:
                window = []
                for i in range(4):
                    window.append(board[row + i][col])
                score += evaluation_function(window,piece,opponent)

            # Diagonal from bottomLeft to upRight
            if row + 3 < 6 and col + 3 < 7:
                window = []
                for i in range(4):
                    window.append(board[row + i][col + i])
                score += evaluation_function(window,piece,opponent)
            
            # Diagonal from upleft to bottomRight
            if row - 3 >= 0 and col + 3 < 7:
                window = []
                for i in range(4):
                    window.append(board[row - i][col + i])
                score += evaluation_function(window,piece,opponent)

    #Center Multiplier
    center_col = 3
    center_pieces = sum(1 for row in range(6) if board[row][center_col] == piece)
    score += center_pieces * 3

    return score

nodes_counter=0 
  #بترجع النقلات المتاحة 
def get_valid_moves(board):
    valid_moves = []
    for col in range(COLS):
        if board[0][col] == 0:  
            valid_moves.append(col)
    return valid_moves

def minimax(board,depth,maximizing):    
    global nodes_counter    
    nodes_counter+=1   

    #لو الجيم خلص
    if Check_Win(board, AI_PIECE):
       return 10**7          # فوز مؤكّد للـ AI
    elif Check_Win(board, PLAYER_PIECE):
       return -10**7         # خسارة مؤكّدة
    elif Check_Draw(board) or depth == 0:
       return heuristic_Score(board, AI_PIECE)

    
    valid_moves=get_valid_moves(board)
    #AI هنا دور ال 
    if maximizing:      
        best=float("-inf")   
        for col in valid_moves:
            temp = np.copy(board)  
            row =get_next_open_row(temp,col) 
            drop_piece(temp,row,col,AI_PIECE) 
            score=minimax(temp,depth-1,False)  

            if score>best:
                best=score
        return best
    # (player) هنا العكس         
    else:
        best=float("inf")
        for col in valid_moves:
            temp= np.copy(board)
            row=get_next_open_row(temp,col)
            drop_piece(temp,row,col,1)
            score=minimax(temp,depth-1,True)

            if score<best:
                best=score
        return best      
# minimax returns score but this fuction return the AI move
def get_AI_move(board,depth):
    global nodes_counter
    nodes_counter=0
    best=float("-inf")
    best_col=None

    for col in get_valid_moves(board):
        temp= board.copy()
        row =get_next_open_row(temp,col)
        drop_piece(temp,row,col,AI_PIECE)

        score=minimax(temp,depth-1,False)

        if score>best:
            best=score
            best_col=col
            
    return best_col,best        



# ===== kiro ====={
print("--- Connect Four Started ---")   

board = create_board()


pygame.init()
SQUARESIZE = 100

PANEL_WIDTH = 350
board_width = COLS * SQUARESIZE
width = board_width + PANEL_WIDTH
height = (ROWS+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four - هنقفل انشاء الله 🙂") 

myfont = pygame.font.SysFont("monospace", 45)
title_font = pygame.font.SysFont("monospace", 45, bold=True)
panel_font = pygame.font.SysFont("monospace", 25, bold=True)

# 🔵 تم استبدال لوب الإدخال من الـ Terminal بلوب الشاشة الافتتاحية (Start Screen)
chosen_depth = 0
draw_start_screen()

while chosen_depth == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos
            
            # اليوزر داس علي الدايرة ولا لا
            for i in range(1, 7):
                cx = (width // 2) - 350 + (i * 100)
                cy = height // 2 + 50
                
            #هل الكليك دوا الدايرة ولالا (بنقيس المسافة)
                if math.hypot(posx - cx, posy - cy) <= RADIUS:
                    chosen_depth = i


screen.fill(BG_COLOR)
print_pretty_board(board)
draw_board(board, screen)
draw_stats_panel("-", "-", "-", "-")

# 4. متغيرات التحكم في اللعبة
game_over = False
turn = 1  # 1 for Human, 2 for AI
total_moves = 0 # عشان الملخص


#  Game Loop 

while not game_over:
    
    # 1. Human's turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            #  مسح الجزء الأسود فوق اللوحة الزرقا بس
            pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE))
            posx = event.pos[0]
            
            #  حماية عشان الماوس ميطلعش بره اللوحة الزرقا ويدخل في الإحصائيات
            if posx > board_width - RADIUS:
                posx = board_width - RADIUS
                
            if turn == 1: 
                pygame.draw.circle(screen, PLAYER_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
            #  تحديث الجزء اللي فوق اللوحة الزرقا بس
            pygame.display.update(0, 0, board_width, SQUARESIZE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0] #  أخدنا ال posx هنا عشان نفحصه الأول
            
            #  حماية عشان الكليك يشتغل بس لو اليوزر داس جوه اللوحة الزرقا
            if posx < board_width and turn == 1:
                #  مسح الجزء الأسود فوق اللوحة الزرقا بس
                pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE))
                
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    total_moves += 1

                    print(f"\n--- bor3y  (⚪) Move ---")
                    print(f"Chosen column: {col}")
                    print_pretty_board(board)
                    
                    draw_board(board, screen)

                    if Check_Win(board, 1):
                        draw_text_with_shadow("bor3y wins!!", PLAYER_COLOR)
                        print("\n*******************\n bor3y (⚪) WINS! \n*******************")
                        game_over = True
                    elif Check_Draw(board):
                        draw_text_with_shadow("IT'S A DRAW!!", BOARD_COLOR)
                        print("\nIt's a draw!")
                        game_over = True

                    turn = 2
                    # ===== kiro =====}

    # 2. AI's turn
    if turn == 2 and not game_over:
        draw_text_with_shadow("AI is thinking...", AI_COLOR)
        print("\n--- AI (🔴) is thinking... ---")
        
        # حساب الوقت والـ nodes
        start_time = time.time()

        col, score = get_AI_move(board, depth=chosen_depth)

        #  مسح الجزء اللي فوق اللوحة الزرقا بس
        pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE)) 
        end_time = time.time()
        
        time_taken_ms = (end_time - start_time) * 1000 # تحويل لمللي ثانية

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            total_moves += 1

            print(f"1) Board State:")
            print_pretty_board(board)
            print(f"2) AI Chosen Column: {col}")
            print(f"3) Heuristic Score: {score}")
            print(f"4) Total Nodes Evaluated (Depth {chosen_depth}): {nodes_counter}")
            print(f"5) Time Taken: {time_taken_ms:.2f} ms")
            print("------------------------------")
            
            draw_board(board, screen)
            
            #   تحديث الإحصائيات في اللوحة الجانبية
            draw_stats_panel(col, score, nodes_counter, time_taken_ms)

            if Check_Win(board, 2):
                draw_text_with_shadow("AI wins!!", AI_COLOR)
                print("\n*******************\n AI (🔴) WINS! \n*******************")
                game_over = True
            elif Check_Draw(board):
                draw_text_with_shadow("IT'S A DRAW!!", BOARD_COLOR)
                print("\nIt's a draw!")
                game_over = True

            turn = 1


     # ===== kiro ====={
    # 3(Game Summary)
    if game_over:
        print("\n=== FINAL GAME SUMMARY ===")
        print(f"Total Moves Played: {total_moves}")
        print(f"Final Depth Used: {chosen_depth}")
        print("==========================")
        
        # عرض الملخص في اللوحة الجانبية
        draw_game_summary(total_moves, chosen_depth)
        
        pygame.time.wait(7000)
    # ===== kiro =====}