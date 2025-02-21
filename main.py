import chess
import chess.engine
import pygame

ENGINE_PATH = "engine/stockfish/stockfish-windows-x86-64-avx2.exe"  # PATH TO ENGINE EXECUTABLE

# Initialize pygame
pygame.init()

# Load sounds
move_sound = pygame.mixer.Sound('assets/move-self.mp3')
capture_sound = pygame.mixer.Sound('assets/capture.mp3')

# Define dimensions
SQUARE_SIZE = 60
DIM_X = DIM_Y = 8

# Window size
width = SQUARE_SIZE * DIM_X
height = SQUARE_SIZE * DIM_Y
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('BitChess')

# Colors
BEIGE = (255, 218, 153)
BROWN = (138, 86, 39)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
pieces_images = {
    'P': pygame.image.load('assets/white_pawn.png'),
    'R': pygame.image.load('assets/white_rook.png'),
    'N': pygame.image.load('assets/white_knight.png'),
    'B': pygame.image.load('assets/white_bishop.png'),
    'Q': pygame.image.load('assets/white_queen.png'),
    'K': pygame.image.load('assets/white_king.png'),
    'p': pygame.image.load('assets/black_pawn.png'),
    'r': pygame.image.load('assets/black_rook.png'),
    'n': pygame.image.load('assets/black_knight.png'),
    'b': pygame.image.load('assets/black_bishop.png'),
    'q': pygame.image.load('assets/black_queen.png'),
    'k': pygame.image.load('assets/black_king.png')
}

# Resize images
for key in pieces_images:
    pieces_images[key] = pygame.transform.scale(pieces_images[key], (SQUARE_SIZE, SQUARE_SIZE))


# Create the chessboard
def draw_chessboard(selected_square=None, board=None):
    for i in range(DIM_X):
        for j in range(DIM_Y):
            color = BEIGE if (i + j) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    if selected_square is not None and board is not None:
        for move in board.legal_moves:
            if move.from_square == selected_square:
                to_square = move.to_square
                col = chess.square_file(to_square)
                row = 7 - chess.square_rank(to_square)
                if board.piece_at(to_square):
                    pygame.draw.circle(screen, DARK_GRAY,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       SQUARE_SIZE // 2, 3)
                else:
                    pygame.draw.circle(screen, GRAY,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       SQUARE_SIZE // 6)


# Display pieces
def draw_pieces(board):
    for i in range(DIM_X):
        for j in range(DIM_Y):
            piece = board.piece_at(chess.square(i, 7 - j))
            if piece:
                screen.blit(pieces_images[piece.symbol()], (i * SQUARE_SIZE, j * SQUARE_SIZE))


# Function to make the AI (Stockfish) play
def play_ai(board, engine_path=ENGINE_PATH):
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        result = engine.play(board, chess.engine.Limit(time=1.0))
        move = result.move
        if board.is_capture(move):
            capture_sound.play()
        else:
            move_sound.play()
        board.push(move)


# Function to display game over message
def display_game_over(message):
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, BLACK, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)


# Update display function
def update_display(board, selected_square=None):
    draw_chessboard(selected_square, board)
    draw_pieces(board)
    pygame.display.flip()


# Main function
def main():
    board = chess.Board()
    running = True
    selected_square = None

    while running:
        update_display(board, selected_square)

        if board.is_checkmate():
            winner = "You won" if board.turn == chess.BLACK else "Stockfish won"
            display_game_over(f"Shah Mat!, {winner}")
            running = False
            continue
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            display_game_over("Game Over! Draw")
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                square = chess.square(col, 7 - row)

                if selected_square is None:
                    if board.piece_at(square) and board.color_at(square) == chess.WHITE:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        if board.is_capture(move):
                            capture_sound.play()
                        else:
                            move_sound.play()
                        board.push(move)
                        update_display(board)
                        pygame.time.delay(500)
                        if not board.is_game_over():
                            play_ai(board)
                    selected_square = None

    pygame.quit()


if __name__ == "__main__":
    main()
