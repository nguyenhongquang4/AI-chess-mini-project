import numpy as np
import chess
from chess import Board

import random

from stockfish import Stockfish
class StockfishEngine:
    def __init__(self, path, parameters):
        self.engine = Stockfish(path=path)
        self.elo = 1000
        self.parameters = parameters

    def predict_move(self, board):
        self.engine.set_fen_position(board.fen())
        move_uci = self.engine.get_best_move()
        move = chess.Move.from_uci(move_uci)
        return move

    def calculate_elo(self, opponent, result, K=64):
        E1 = 1 / (1 + 10 ** ((opponent.elo - self.elo) / 400))
        S1 = result
        S2 = 1 - result
        E2 = 1 - E1
        self.elo += K * (S1 - E1)
        opponent.elo += K * (S2 - E2)
        return self.elo, opponent.elo

    def play_game(self, opponent, result):
        self.elo, opponent.elo = self.calculate_elo(opponent, result)
        self.elo = int(self.elo)
        opponent.elo = int(opponent.elo)
