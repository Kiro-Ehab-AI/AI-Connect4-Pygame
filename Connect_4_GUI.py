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

def create_board():
    return np.zeros((ROWS, COLS))

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col): 
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def print_pretty_board(board):
    print("\n   0    1    2    3    4    5    6") 
    print("-------------------------------------")
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            if board[r][c] == 1:
                row_str += " ⚪ |" 
            elif board[r][c] == 2:
                row_str += " 🔴 |"  
            else:
                row_str += "    |"  
        print(row_str)
        print("-------------------------------------")


def draw_board(board, screen):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BOARD_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BG_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLS):
        for r in range(ROWS):       
            if board[r][c] == 1: 
                pygame.draw.circle(screen, PLAYER_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, AI_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def draw_text_with_shadow(text, color): 
 
    pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE))
    
    
    shadow = myfont.render(text, 1, (50, 50, 50)) 

    shadow_rect = shadow.get_rect(center=(board_width//2 + 2, SQUARESIZE//2 + 2))
    screen.blit(shadow, shadow_rect)
    
    
    label = myfont.render(text, 1, color)
    
    label_rect = label.get_rect(center=(board_width//2, SQUARESIZE//2))
    screen.blit(label, label_rect)
    
    pygame.display.update()


def draw_stats_panel(ai_col, score, nodes, time_ms):
    
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


def draw_game_summary(moves, depth): 
    
    pygame.draw.line(screen, BOARD_COLOR, (board_width + 40, 480), (board_width + 310, 480), 2)
    
    
    title = title_font.render("SUMMARY", 1, AI_COLOR)
    screen.blit(title, (board_width + 90, 500))
    
    
    screen.blit(panel_font.render("Total Moves:", 1, PLAYER_COLOR), (board_width + 15, 570))
    screen.blit(panel_font.render(str(moves), 1, AI_COLOR), (board_width + 220, 570))
    
    screen.blit(panel_font.render("Final Depth:", 1, PLAYER_COLOR), (board_width + 15, 630))
    screen.blit(panel_font.render(str(depth), 1, AI_COLOR), (board_width + 220, 630))
    
    pygame.display.update()


def draw_start_screen():
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

def is_terminal(board):
     return Check_Draw(board) or Check_Win(board, 1) or Check_Win(board, 2)

def evaluation_function(window,player,opponent):
    score = 0
    player_pieces = window.count(player)
    opponent_pieces = window.count(opponent)
    empty = window.count(0)

    
    if player_pieces == 4:
        score += 100
    elif opponent_pieces == 4:
        score -= 100

    
    elif player_pieces == 3 and empty == 1:
        score += 5 
    elif opponent_pieces == 3 and empty == 1:
        score -= 4   #

    
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

         
            if row + 3 < 6:
                window = []
                for i in range(4):
                    window.append(board[row + i][col])
                score += evaluation_function(window,piece,opponent)

            if row + 3 < 6 and col + 3 < 7:
                window = []
                for i in range(4):
                    window.append(board[row + i][col + i])
                score += evaluation_function(window,piece,opponent)

            if row - 3 >= 0 and col + 3 < 7:
                window = []
                for i in range(4):
                    window.append(board[row - i][col + i])
                score += evaluation_function(window,piece,opponent)


    center_col = 3
    center_pieces = sum(1 for row in range(6) if board[row][center_col] == piece)
    score += center_pieces * 3

    return score

nodes_counter=0 

def get_valid_moves(board):
    valid_moves = []
    for col in range(COLS):
        if board[0][col] == 0:  
            valid_moves.append(col)
    return valid_moves

def minimax(board,depth,maximizing):    
    global nodes_counter    
    nodes_counter+=1   


    if Check_Win(board, AI_PIECE):
       return 10**7      
    elif Check_Win(board, PLAYER_PIECE):
       return -10**7         
    elif Check_Draw(board) or depth == 0:
       return heuristic_Score(board, AI_PIECE)

    
    valid_moves=get_valid_moves(board)
  
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
pygame.display.set_caption("Connect Four") 

myfont = pygame.font.SysFont("monospace", 45)
title_font = pygame.font.SysFont("monospace", 45, bold=True)
panel_font = pygame.font.SysFont("monospace", 25, bold=True)


chosen_depth = 0
draw_start_screen()

while chosen_depth == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos

            for i in range(1, 7):
                cx = (width // 2) - 350 + (i * 100)
                cy = height // 2 + 50
           
                if math.hypot(posx - cx, posy - cy) <= RADIUS:
                    chosen_depth = i


screen.fill(BG_COLOR)
print_pretty_board(board)
draw_board(board, screen)
draw_stats_panel("-", "-", "-", "-")

game_over = False
turn = 1 
total_moves = 0 



while not game_over:
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
           
            pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE))
            posx = event.pos[0]
          
            if posx > board_width - RADIUS:
                posx = board_width - RADIUS
                
            if turn == 1: 
                pygame.draw.circle(screen, PLAYER_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
       
            pygame.display.update(0, 0, board_width, SQUARESIZE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0] 
      
            if posx < board_width and turn == 1:
  
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
                


    if turn == 2 and not game_over:
        draw_text_with_shadow("AI is thinking...", AI_COLOR)
        print("\n--- AI (🔴) is thinking... ---")
        
  
        start_time = time.time()

        col, score = get_AI_move(board, depth=chosen_depth)

      
        pygame.draw.rect(screen, BG_COLOR, (0,0, board_width, SQUARESIZE)) 
        end_time = time.time()
        
        time_taken_ms = (end_time - start_time) * 1000 

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



    if game_over:
        print("\n=== FINAL GAME SUMMARY ===")
        print(f"Total Moves Played: {total_moves}")
        print(f"Final Depth Used: {chosen_depth}")
        print("==========================")
        
  
        draw_game_summary(total_moves, chosen_depth)
        
        pygame.time.wait(7000)
  