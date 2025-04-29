import numpy as np
import chess
from chess import Board

import random
from algorithm import iterative_deepening
class ChessEngine:
    def __init__(self):
        # self.search_depth = search_depth
        self.elo = 1000
        self.transposition_table = {}

    def is_valid_uci(self, move_uci, board):
        try:
            move = chess.Move.from_uci(move_uci)
            return move in board.legal_moves
        except Exception:
            return False

    def predict_move(self, board):
        try:
            # move = select_move(board)
            # if move:
            #     return move
            return iterative_deepening(board)
        except Exception as e:
            print(f"Search error: {e}")
            legal_moves = list(board.legal_moves)
            non_losing_moves = []

            for move in legal_moves:
                board_copy = board.copy()
                board_copy.push(move)
                if not board_copy.is_checkmate():
                    non_losing_moves.append(move)

            if non_losing_moves:
                return random.choice(non_losing_moves)
            elif legal_moves:
                return random.choice(legal_moves)
            else:
                return None

    def calculate_elo(self, opponent, result, K=32):
        """Tính toán Elo với hệ số K điều chỉnh"""
        E1 = 1 / (1 + 10 ** ((opponent.elo - self.elo) / 400))
        S1 = result

        # Điều chỉnh hệ số K dựa trên Elo hiện tại
        if self.elo < 2000:
            K = 32
        elif self.elo < 2400:
            K = 24
        else:
            K = 16

        self.elo += K * (S1 - E1)

        # Cập nhật Elo của đối thủ
        S2 = 1 - result
        E2 = 1 - E1
        opponent.elo += K * (S2 - E2)

        return int(self.elo), int(opponent.elo)

    def play_game(self, opponent, result):
        self.elo, opponent.elo = self.calculate_elo(opponent, result)

        # Reset transposition table sau mỗi trận đấu để tránh tràn bộ nhớ
        self.transposition_table = {}