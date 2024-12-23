import pygame
import requests

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (173, 216, 230)
FONT_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont('Arial', 35)
BUTTON_COLOR = (0, 122, 204)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Sudoku")

# Fetch a Sudoku puzzle
def fetch_puzzle():
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
    return response.json()["board"]

def draw_grid():
    """Draw the Sudoku grid."""
    for i in range(GRID_SIZE + 1):
        width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), width)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), width)

def draw_numbers(board):
    """Draw the numbers on the Sudoku board."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, FONT_COLOR)
                screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + CELL_SIZE // 5))

def highlight_cell(row, col):
    """Highlight the currently selected cell."""
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def is_valid(board, row, col, num):
    """Check if placing num at (row, col) is valid."""
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_board(board):
    """Solve the Sudoku puzzle using backtracking."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def draw_button():
    """Draw a solve button below the grid."""
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 3, HEIGHT + 10, WIDTH // 3, 40))
    button_text = FONT.render("Solve", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT + 15))

def main() -> object:
    running = True
    board = fetch_puzzle()
    original_board = [[board[i][j] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    selected_cell = None

    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        if selected_cell:
            highlight_cell(*selected_cell)
        draw_numbers(board)
        draw_button()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < HEIGHT:
                    selected_cell = (y // CELL_SIZE, x // CELL_SIZE)
                elif WIDTH // 3 <= x <= 2 * WIDTH // 3 and HEIGHT + 10 <= y <= HEIGHT + 50:
                    solve_board(board)

            if event.type == pygame.KEYDOWN and selected_cell:
                row, col = selected_cell
                if original_board[row][col] == 0:
                    if event.key == pygame.K_1: board[row][col] = 1
                    if event.key == pygame.K_2: board[row][col] = 2
                    if event.key == pygame.K_3: board[row][col] = 3
                    if event.key == pygame.K_4: board[row][col] = 4
                    if event.key == pygame.K_5: board[row][col] = 5
                    if event.key == pygame.K_6: board[row][col] = 6
                    if event.key == pygame.K_7: board[row][col] = 7
                    if event.key == pygame.K_8: board[row][col] = 8
                    if event.key == pygame.K_9: board[row][col] = 9
                    if event.key == pygame.K_BACKSPACE: board[row][col] = 0

    pygame.quit()

if __name__ == "__main__":
    main()
