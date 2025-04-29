import chess
from stockfish import Stockfish
import random
from chessAI import ChessEngine
from stockfish_AI import StockfishEngine
def main():
    ai_white = ChessEngine()
    stockfish_path = "stockfish-windows-x86-64-avx2.exe"
    ai_black = StockfishEngine(path = stockfish_path)
    #ai_white = StockfishEngine(path = stockfish_path, parameters={"Skill Level": 5, "Threads": 2, "Minimum Thinking Time": 30})
    #ai_black = ChessEngine(search_depth=18)
    num_games = 10
    results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}

    for game_num in range(num_games):
        board = chess.Board()
        print(f"\n=== Starting game {game_num+1} ===\n")

        while not board.is_game_over():
            if board.turn == chess.WHITE:
                move = ai_white.predict_move(board)
            else:
                move = ai_black.predict_move(board)
            board.push(move)
            print(board)
            print("-" * 30)

        result = board.result()
        results[result] += 1
        print(f"Game {game_num+1} finished: {result}")
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

    print(results)

if __name__ == "__main__":
    main()
