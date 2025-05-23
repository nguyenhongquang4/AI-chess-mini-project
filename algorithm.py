import time
import math
import random
import chess
from pieces import opening_book, transposition_table, material_value
from evaluation import evaluate_board
killer_moves = {}
history_heuristic = {}


def order_moves(board, depth, prev_best_move=None):
    moves = list(board.legal_moves)
    move_scores = {}

    piece_moved = {}

    for move in moves:
        score = 0
        from_square = move.from_square
        piece = board.piece_at(from_square)

        if prev_best_move and move == prev_best_move:
            score += 100000

        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            aggressor = board.piece_at(move.from_square)
            if victim and aggressor:
                victim_value = material_value.get(victim.piece_type, 0)
                aggressor_value = material_value.get(aggressor.piece_type, 0)
                score += 10 * victim_value - aggressor_value + 5000

        if move.promotion:
            score += 10000

        if board.gives_check(move):
            score += 3000

        if depth in killer_moves and move in killer_moves[depth]:
            score += 4500

        history_value = history_heuristic.get((from_square, move.to_square), 0)
        score += history_value

        if piece:
            piece_type = piece.piece_type
            piece_key = (piece_type, from_square)

            if piece_key not in piece_moved:
                if piece_type == chess.BISHOP:
                    score += 3500
                elif piece_type == chess.QUEEN:
                    score += 3000
                elif piece_type == chess.ROOK:
                    score += 2500
                elif piece_type == chess.PAWN:
                    file = chess.square_file(from_square)
                    if 2 <= file <= 5 and board.fullmove_number <= 10:
                        score += 2000
                    else:
                        score += 1500
                elif piece_type == chess.KNIGHT:
                    score += 1000

                piece_moved[piece_key] = True

        to_file = chess.square_file(move.to_square)
        to_rank = chess.square_rank(move.to_square)
        if 2 <= to_file <= 5 and 2 <= to_rank <= 5:
            score += 1500

        if board.fullmove_number <= 10:
            if piece and piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                piece_color = piece.color
                is_starting_position = False

                if piece_color == chess.WHITE:
                    if piece.piece_type == chess.BISHOP and from_square in [chess.C1, chess.F1]:
                        is_starting_position = True
                    elif piece.piece_type == chess.KNIGHT and from_square in [chess.B1, chess.G1]:
                        is_starting_position = True
                else:
                    if piece.piece_type == chess.BISHOP and from_square in [chess.C8, chess.F8]:
                        is_starting_position = True
                    elif piece.piece_type == chess.KNIGHT and from_square in [chess.B8, chess.G8]:
                        is_starting_position = True

                if is_starting_position:
                    score += 3000

        move_scores[move] = score

    return sorted(moves, key=lambda move: move_scores.get(move, 0), reverse=True)


def use_opening_book(board):
    try:
        fen = board.fen()
        fen_parts = fen.split(' ')
        position_fen = ' '.join(fen_parts[:4])

        for book_fen, move_uci in opening_book.items():
            book_fen_parts = book_fen.split(' ')
            book_position_fen = ' '.join(book_fen_parts[:4])

            if book_position_fen == position_fen:
                try:
                    book_move = chess.Move.from_uci(move_uci)
                    if book_move in board.legal_moves:
                        return book_move
                except ValueError:
                    try:
                        book_move = board.parse_san(move_uci)
                        if book_move in board.legal_moves:
                            return book_move
                    except ValueError:
                        pass
    except Exception:
        pass

    return None


def quiescence_search(board, alpha, beta, color, depth=0, max_depth=8):
    if depth >= max_depth:
        return color * evaluate_board(board)

    stand_pat = color * evaluate_board(board)

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat


    moves = [move for move in board.legal_moves if board.is_capture(move) or move.promotion or board.gives_check(move)]

    moves.sort(key=lambda move: score_capture(board, move), reverse=True)

    for move in moves:
        board.push(move)
        score = -quiescence_search(board, -beta, -alpha, -color, depth + 1, max_depth)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


def score_capture(board, move):
    if not board.is_capture(move):
        return 0

    victim = board.piece_at(move.to_square)
    aggressor = board.piece_at(move.from_square)

    if not victim or not aggressor:
        return 0

    victim_value = material_value.get(victim.piece_type, 0)
    aggressor_value = material_value.get(aggressor.piece_type, 0)

    return victim_value - (aggressor_value / 10)


def negamax_with_quiescence(board, depth, alpha, beta, color):
    if board.is_repetition(2):
        return 0

    if depth == 0 or board.is_game_over():
        return quiescence_search(board, alpha, beta, color)

    key = board.fen()

    # Transposition table lookup
    if key in transposition_table:
        stored_score, stored_depth, stored_flag, prev_move = transposition_table[key]
        if stored_depth >= depth:
            if stored_flag == 'EXACT':
                return stored_score
            elif stored_flag == 'LOWERBOUND' and stored_score > alpha:
                alpha = max(alpha, stored_score)
            elif stored_flag == 'UPPERBOUND' and stored_score < beta:
                beta = min(beta, stored_score)
            if alpha >= beta:
                return stored_score

    if board.is_check():
        depth += 1

    if depth >= 3 and not board.is_check() and has_non_pawn_material(board, board.turn):
        R = 2 if depth >= 4 else 1

        board.push(chess.Move.null())
        null_move_score = -negamax_with_quiescence(board, depth - 1 - R, -beta, -beta + 1, -color)
        board.pop()

        if null_move_score >= beta:
            return beta

    prev_best_move = None
    if key in transposition_table:
        stored_score, stored_depth, stored_flag, prev_move = transposition_table.get(key, (None, None, None, None))
        prev_best_move = prev_move

    moves = order_moves(board, depth, prev_best_move)
    best_score = -float('inf')
    best_move = None
    moves_searched = 0

    if depth <= 6 and board.fullmove_number <= 10:
        book_move = use_opening_book(board)
        if book_move and book_move in moves:
            moves.remove(book_move)
            moves.insert(0, book_move)

    for move in moves:
        moves_searched += 1
        board.push(move)

        if moves_searched > 1 and depth >= 3 and not board.is_check() and not board.is_capture(
                move) and not move.promotion:
            reduction = 1 if moves_searched > 4 else 0
            score = -negamax_with_quiescence(board, depth - 1 - reduction, -beta, -alpha, -color)

            if score > alpha:
                score = -negamax_with_quiescence(board, depth - 1, -beta, -alpha, -color)
        else:
            score = -negamax_with_quiescence(board, depth - 1, -beta, -alpha, -color)

        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)
        if alpha >= beta:
            if not board.is_capture(move) and not move.promotion:
                killer_moves.setdefault(depth, []).append(move)
                history_key = (move.from_square, move.to_square)
                history_heuristic[history_key] = history_heuristic.get(history_key, 0) + depth * depth

            transposition_table[key] = (beta, depth, 'LOWERBOUND', move)
            return beta

    flag = 'EXACT'
    if best_score <= alpha:
        flag = 'UPPERBOUND'
    elif best_score >= beta:
        flag = 'LOWERBOUND'

    transposition_table[key] = (best_score, depth, flag, best_move if best_move else None)
    return best_score


def has_non_pawn_material(board, color):
    for piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        if any(board.pieces(piece_type, color)):
            return True
    return False

import multiprocessing

def evaluate_move(move, board_fen, depth, alpha, beta):
    board = chess.Board(board_fen)
    board.push(move)
    score = -negamax_with_quiescence(board, depth, -beta, -alpha, -1)
    return move, score

def iterative_deepening(board, max_depth=10, time_limit=5.0):
    start_time = time.time()
    best_move = None
    prev_best_move = None
    prev_score = 0
    killer_moves.clear()
    history_heuristic.clear()

    for current_depth in range(1, max_depth + 1):
        if time.time() - start_time > time_limit * 0.9:
            break

        aspiration_window = 50
        alpha = prev_score - aspiration_window
        beta = prev_score + aspiration_window
        best_score = -float('inf')
        best_move_at_depth = None

        while True:
            moves = order_moves(board, current_depth, prev_best_move)
            current_best_score = -float('inf')
            current_best_move = None
            search_timed_out = False
            for move in moves:
                board.push(move)
                score = -negamax_with_quiescence(board, current_depth - 1, -beta, -alpha, -1)
                board.pop()

                if time.time() - start_time > time_limit:
                    search_timed_out = True
                    break

                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move

                if current_best_score > alpha:
                    alpha = current_best_score

                if alpha >= beta:
                    break

            if search_timed_out:
                break
            if current_best_move is not None and (current_best_score > beta or current_best_score < alpha):
                aspiration_window += 50
                alpha = prev_score - aspiration_window
                beta = prev_score + aspiration_window
                alpha = max(alpha, -999999)
                beta = min(beta, 999999)
            else:
                best_score = current_best_score
                best_move_at_depth = current_best_move
                prev_score = best_score
                break

        if search_timed_out and best_move is not None:
            break

        if best_move_at_depth:
        #     print(f"Best move at depth {current_depth}: {best_move_at_depth}")
            best_move = best_move_at_depth

    return best_move