import chess
import chess.engine
import pygame

# Initialize pygame
pygame.init()

# Load sounds
move_sound = pygame.mixer.Sound('assets/move-self.mp3')
capture_sound = pygame.mixer.Sound('assets/capture.mp3')

# Define dimensions
SQUARE_SIZE = 60
DIM_X = DIM_Y = 8  # 8x8 squares

# Window size
width = SQUARE_SIZE * DIM_X
height = SQUARE_SIZE * DIM_Y
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Game')

# Colors
BEIGE = (255, 218, 153)
BROWN = (138, 86, 39)
GREEN = (0, 255, 0)

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
def draw_chessboard(selected_square=None):
    for i in range(DIM_X):
        for j in range(DIM_Y):
            color = BEIGE if (i + j) % 2 == 0 else BROWN
            if selected_square is not None and selected_square == chess.square(i, 7 - j):
                color = GREEN  # Highlight the selected square
            pygame.draw.rect(screen, color, pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# Display pieces
def draw_pieces(board):
    for i in range(DIM_X):
        for j in range(DIM_Y):
            piece = board.piece_at(chess.square(i, 7 - j))
            if piece:
                screen.blit(pieces_images[piece.symbol()], (i * SQUARE_SIZE, j * SQUARE_SIZE))


# Function to make the AI (Stockfish) play
def play_ai(board, engine_path="stockfish/stockfish-windows-x86-64-avx2.exe"):
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        result = engine.play(board, chess.engine.Limit(time=1.0))
        move = result.move
        if board.is_capture(move):
            capture_sound.play()
        else:
            move_sound.play()
        board.push(move)


# Main function
def main():
    board = chess.Board()
    running = True
    selected_square = None

    while running:
        draw_chessboard(selected_square)
        draw_pieces(board)
        pygame.display.flip()

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
                        if not board.is_game_over():
                            play_ai(board)
                    selected_square = None

    pygame.quit()


if __name__ == "__main__":
    main()
