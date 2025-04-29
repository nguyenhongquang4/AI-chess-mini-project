import chess
import pygame
from chessAI import ChessEngine
from stockfish_AI import StockfishEngine

# GUI constants
WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
DIMENSION = 8
pieces_img = {}

def load_images():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        pieces_img[piece] = pygame.transform.scale((pygame.image.load("chess/" + piece + ".png")), (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board, screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                piece_str = piece.symbol()
                piece_name = ('w' if piece_str.isupper() else 'b') + piece_str.lower()
                screen.blit(pieces_img[piece_name], pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI vs Stockfish")
    load_images()
    clock = pygame.time.Clock()

    ai_white = ChessEngine()
    stockfish_path = "stockfish-windows-x86-64-avx2.exe"
    ai_black = StockfishEngine(path=stockfish_path, parameters={"Skill Level": 5, "Threads": 0, "Minimum Thinking Time": 5})

    num_games = 1
    results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}

    for game_num in range(num_games):
        board = chess.Board()
        print(f"\n=== Starting game {game_num + 1} ===\n")

        while not board.is_game_over():
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if board.turn == chess.WHITE:
                move = ai_white.predict_move(board)
            else:
                move = ai_black.predict_move(board)


            board.push(move)

            draw_board(screen)
            draw_pieces(board, screen)
            pygame.display.flip()
            pygame.time.wait(300)



        result = board.result()
        results[result] += 1
        print(f"Game {game_num + 1} finished: {result}")

        if result == "1-0":
            ai_white.play_game(ai_black, 1)
            ai_black.play_game(ai_white, 0)
        elif result == "0-1":
            ai_white.play_game(ai_black, 0)
            ai_black.play_game(ai_white, 1)
        else:
            ai_white.play_game(ai_black, 0.5)
            ai_black.play_game(ai_white, 0.5)

        print(f"White Elo: {ai_white.elo:.1f}, Black Elo: {ai_black.elo:.1f}")
    pygame.time.wait(10000)
    print(results)
    pygame.quit()

if __name__ == "__main__":
    main()
