import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700  # Height increased to add a top row for drop selection
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# Create the board
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_board():
    screen.fill(BLACK)  # Fill background with black
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
    pygame.display.update()

def drop_piece(row, col, piece):
    board[row][col] = piece

def is_valid_location(col):
    return board[0][col] == 0

def get_next_open_row(col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(piece):
    # Check horizontal locations
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

# Main game loop
game_over = False
turn = 0  # 0 for Player 1 (RED), 1 for Player 2 (YELLOW)

draw_board()  # Initial draw

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, SQUARE_SIZE // 2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, SQUARE_SIZE // 2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            # Player 1 Input
            if turn == 0:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if is_valid_location(col):
                    row = get_next_open_row(col)
                    drop_piece(row, col, 1)

                    if winning_move(1):
                        print("Player 1 wins!")
                        game_over = True

            # Player 2 Input
            else:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if is_valid_location(col):
                    row = get_next_open_row(col)
                    drop_piece(row, col, 2)

                    if winning_move(2):
                        print("Player 2 wins!")
                        game_over = True

            draw_board()

            # Switch turn
            turn += 1
            turn %= 2

            if game_over:
                pygame.time.wait(3000)
