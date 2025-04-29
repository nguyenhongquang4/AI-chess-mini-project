import chess
from pieces import material_value, center_squares, PIECE_VALUES, KING_ENDGAME_VALUES
def surrounding_squares(square):
    rank = chess.square_rank(square)
    file = chess.square_file(square)

    neighbors = []
    for dr in [-1, 0, 1]:
        for df in [-1, 0, 1]:
            if dr == 0 and df == 0:
                continue
            r, f = rank + dr, file + df
            if 0 <= r < 8 and 0 <= f < 8:
                neighbors.append(chess.square(f, r))
    return neighbors


def get_positional_value(piece_type, color, square):
    table = PIECE_VALUES.get(piece_type)
    if table and len(table) == 64:
        index = square if color == chess.WHITE else chess.square_mirror(square)
        return table[index]
    return 0


def evaluate_material(board):
    score = 0
    game_phase = evaluate_game_phase(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece.piece_type
            value = material_value.get(piece_type, 0)
            position_value = get_positional_value(piece_type, piece.color, square)

            if piece_type == chess.KING:
                mg_value = position_value
                eg_value = KING_ENDGAME_VALUES[square] if 0 <= square < 64 else 0
                position_value = mg_value * game_phase + eg_value * (1 - game_phase)

            score += (value + position_value) if piece.color == chess.WHITE else -(value + position_value)

    return score


def evaluate_pawn_advances(board):
    score = 0

    # Reward central pawn advances
    central_files = [3, 4]  # d and e files (0-indexed)

    for color in [chess.WHITE, chess.BLACK]:
        for file in central_files:
            initial_rank = 1 if color == chess.WHITE else 6

            # Check if the pawn has moved from its initial position
            initial_square = chess.square(file, initial_rank)
            initial_piece = board.piece_at(initial_square)

            if not (initial_piece and initial_piece.piece_type == chess.PAWN and initial_piece.color == color):
                # The pawn has moved, give a bonus
                score += 30 if color == chess.WHITE else -30

                # Additional bonus if moved to control the center
                target_ranks = [3, 4] if color == chess.WHITE else [3, 4]
                for rank in target_ranks:
                    target_square = chess.square(file, rank)
                    target_piece = board.piece_at(target_square)
                    if target_piece and target_piece.piece_type == chess.PAWN and target_piece.color == color:
                        score += 50 if color == chess.WHITE else -50

    # Smaller reward for flank pawn advances to discourage excessive flank play
    flank_files = [0, 1, 2, 5, 6, 7]  # a, b, c, f, g, h files

    for color in [chess.WHITE, chess.BLACK]:
        for file in flank_files:
            initial_rank = 1 if color == chess.WHITE else 6
            initial_square = chess.square(file, initial_rank)
            initial_piece = board.piece_at(initial_square)

            if not (initial_piece and initial_piece.piece_type == chess.PAWN and initial_piece.color == color):
                # The pawn has moved, give a smaller bonus
                score += 10 if color == chess.WHITE else -10

    return score


def evaluate_key_squares_control(board):
    score = 0

    # Define key squares beyond just the center
    key_squares = [
        chess.D4, chess.E4, chess.D5, chess.E5,  # Center
        chess.C3, chess.F3, chess.C6, chess.F6,  # Extended center
        chess.D3, chess.E3, chess.D6, chess.E6  # Important development squares
    ]

    # Evaluate control of these squares
    for square in key_squares:
        # A square is controlled if it's attacked and not occupied by opponent
        if board.is_attacked_by(chess.WHITE, square):
            score += 15
            # Extra points if we actually occupy the square with our piece
            piece = board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                score += 25

        if board.is_attacked_by(chess.BLACK, square):
            score -= 15
            # Extra points if opponent occupies the square
            piece = board.piece_at(square)
            if piece and piece.color == chess.BLACK:
                score -= 25

    return score


def evaluate_piece_mobility(board):
    score = 0
    original_turn = board.turn

    mobility_weights = {
        chess.PAWN: 10,
        chess.KNIGHT: 25,  # Reduced from previous weight
        chess.BISHOP: 30,  # Increased
        chess.ROOK: 40,  # Increased
        chess.QUEEN: 50  # Increased
    }

    for color in [chess.WHITE, chess.BLACK]:
        mobility = 0
        board.turn = color
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if piece:
                # Apply weighted mobility based on piece type
                mobility += mobility_weights.get(piece.piece_type, 0)

                # Additional points for central moves
                to_file = chess.square_file(move.to_square)
                to_rank = chess.square_rank(move.to_square)
                if 2 <= to_file <= 5 and 2 <= to_rank <= 5:
                    mobility += 10

                # Additional points for attacking moves
                if board.piece_at(move.to_square):
                    if piece.piece_type != chess.KNIGHT:  # Lower incentive for knight captures
                        mobility += 20
                    else:
                        mobility += 10

        score += mobility if color == chess.WHITE else -mobility

    board.turn = original_turn
    return score


def evaluate_king_safety(board):
    score = 0
    phase = evaluate_game_phase(board)

    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square is None:
            continue

        file = chess.square_file(king_square)
        open_file_penalty = 0
        shield_bonus = 0

        for f in (file - 1, file, file + 1):
            if 0 <= f < 8:
                if all(board.piece_at(chess.square(f, r)) != chess.Piece(chess.PAWN, color) for r in range(8)):
                    open_file_penalty += 500

        shield_rank = chess.square_rank(king_square) + (1 if color == chess.WHITE else -1)
        if 0 <= shield_rank < 8:
            for df in [-1, 0, 1]:
                shield_file = file + df
                if 0 <= shield_file < 8:
                    piece = board.piece_at(chess.square(shield_file, shield_rank))
                    if piece and piece.piece_type == chess.PAWN and piece.color == color:
                        shield_bonus += 300

        safety_score = shield_bonus - open_file_penalty
        score += safety_score if color == chess.WHITE else -safety_score

    return score


def static_exchange_evaluation(board, move):
    if not board.is_capture(move):
        return 0

    to_square = move.to_square
    from_square = move.from_square

    target_piece = board.piece_at(to_square)
    gain = material_value.get(target_piece.piece_type, 0) if target_piece else (
        material_value[chess.PAWN] if board.is_en_passant(move) else 0)

    board.push(move)
    attackers = board.attackers(not board.turn, to_square)

    if not attackers:
        board.pop()
        return gain

    min_attacker_square = min(attackers, key=lambda s: material_value.get(board.piece_at(s).piece_type, float('inf')))
    recapture_move = chess.Move(min_attacker_square, to_square)
    recapture_value = -static_exchange_evaluation(board, recapture_move)

    board.pop()
    return max(0, gain - recapture_value)


def evaluate_pawn_structure(board):
    score = 0
    phase = evaluate_game_phase(board)

    for color in [chess.WHITE, chess.BLACK]:
        pawns = list(board.pieces(chess.PAWN, color))
        files = [chess.square_file(p) for p in pawns]
        file_count = {f: files.count(f) for f in set(files)}

        doubled_penalty = sum(30 for count in file_count.values() if count > 1)
        isolated_penalty = sum(25 * file_count[f] for f in range(8) if
                               file_count.get(f, 0) and file_count.get(f - 1, 0) + file_count.get(f + 1, 0) == 0)

        passed_bonus = 0
        for pawn_sq in pawns:
            file = chess.square_file(pawn_sq)
            rank = chess.square_rank(pawn_sq)
            is_passed = True

            if color == chess.WHITE:
                for r in range(rank + 1, 8):
                    if any(board.piece_at(chess.square(f, r)) and board.piece_at(
                            chess.square(f, r)).piece_type == chess.PAWN and board.piece_at(
                            chess.square(f, r)).color != color for f in (file - 1, file, file + 1) if 0 <= f < 8):
                        is_passed = False
                        break
            else:
                for r in range(rank):
                    if any(board.piece_at(chess.square(f, r)) and board.piece_at(
                            chess.square(f, r)).piece_type == chess.PAWN and board.piece_at(
                            chess.square(f, r)).color != color for f in (file - 1, file, file + 1) if 0 <= f < 8):
                        is_passed = False
                        break

            if is_passed:
                passed_bonus += (50 + rank * 10) * phase

        pawn_score = passed_bonus - (doubled_penalty + isolated_penalty)
        score += pawn_score if color == chess.WHITE else -pawn_score

    return score


def evaluate_piece_activation(board):
    score = 0

    # Initial positions of pieces
    initial_positions = {
        chess.WHITE: {
            chess.PAWN: [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2],
            chess.KNIGHT: [chess.B1, chess.G1],
            chess.BISHOP: [chess.C1, chess.F1],
            chess.ROOK: [chess.A1, chess.H1],
            chess.QUEEN: [chess.D1],
            chess.KING: [chess.E1]
        },
        chess.BLACK: {
            chess.PAWN: [chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7],
            chess.KNIGHT: [chess.B8, chess.G8],
            chess.BISHOP: [chess.C8, chess.F8],
            chess.ROOK: [chess.A8, chess.H8],
            chess.QUEEN: [chess.D8],
            chess.KING: [chess.E8]
        }
    }

    # Check for moved pieces and reward accordingly
    for color in [chess.WHITE, chess.BLACK]:
        # Check bishops - high reward for movement
        for init_square in initial_positions[color][chess.BISHOP]:
            piece = board.piece_at(init_square)
            if not (piece and piece.piece_type == chess.BISHOP and piece.color == color):
                score += 50 if color == chess.WHITE else -50

        # Check queen - good reward
        queen_square = initial_positions[color][chess.QUEEN][0]
        piece = board.piece_at(queen_square)
        if not (piece and piece.piece_type == chess.QUEEN and piece.color == color):
            score += 35 if color == chess.WHITE else -35

        # Check rooks - moderate reward
        for init_square in initial_positions[color][chess.ROOK]:
            piece = board.piece_at(init_square)
            if not (piece and piece.piece_type == chess.ROOK and piece.color == color):
                score += 40 if color == chess.WHITE else -40

        # Check knights - reduced reward compared to other pieces to balance development
        for init_square in initial_positions[color][chess.KNIGHT]:
            piece = board.piece_at(init_square)
            if not (piece and piece.piece_type == chess.KNIGHT and piece.color == color):
                score += 45 if color == chess.WHITE else -45

    return score


def evaluate_passed_pawns(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        pawns = list(board.pieces(chess.PAWN, color))
        for pawn_sq in pawns:
            file = chess.square_file(pawn_sq)
            rank = chess.square_rank(pawn_sq)

            # Kiểm tra tốt thông hành
            is_passed = True
            if color == chess.WHITE:
                blocker_ranks = range(rank + 1, 8)
                promotion_distance = 7 - rank
            else:
                blocker_ranks = range(0, rank)
                promotion_distance = rank

            # Kiểm tra các quân chặn
            for r in blocker_ranks:
                for f in [file - 1, file, file + 1]:
                    if 0 <= f < 8:
                        blocker_sq = chess.square(f, r)
                        blocker = board.piece_at(blocker_sq)
                        if blocker and blocker.piece_type == chess.PAWN and blocker.color != color:
                            is_passed = False
                            break
                if not is_passed:
                    break

            if is_passed:
                # Tính điểm dựa trên hàng của quân tốt
                if color == chess.WHITE:
                    base_value = 20 * (rank + 1)  # Điểm tăng theo hàng
                else:
                    base_value = 20 * (8 - rank)

                # Bonus lớn cho các quân tốt đã tiến xa
                if (color == chess.WHITE and rank >= 5) or (color == chess.BLACK and rank <= 2):
                    base_value *= 2

                # Kiểm tra vua hỗ trợ tốt thông hành
                king_sq = board.king(color)
                if king_sq:
                    king_distance = manhattan_distance(king_sq, pawn_sq)
                    # Vua gần tốt thông hành sẽ được thưởng
                    base_value += (7 - king_distance) * 10

                # Kiểm tra vua đối phương có thể chặn tốt
                opponent_king_sq = board.king(not color)
                if opponent_king_sq:
                    # Tính khoảng cách từ vua đối phương đến ô thăng cấp
                    promotion_sq = chess.square(file, 7 if color == chess.WHITE else 0)
                    opponent_king_distance = manhattan_distance(opponent_king_sq, promotion_sq)

                    # Nếu vua đối phương không thể bắt kịp tốt
                    if opponent_king_distance > promotion_distance + (0 if board.turn == color else 1):
                        base_value *= 3  # Bonus rất lớn cho tốt không thể chặn

                score += base_value if color == chess.WHITE else -base_value

    return score


def evaluate_key_squares_control(board):
    score = 0

    # Define key squares beyond just the center
    key_squares = [
        chess.D4, chess.E4, chess.D5, chess.E5,  # Center
        chess.C3, chess.F3, chess.C6, chess.F6,  # Extended center
        chess.D3, chess.E3, chess.D6, chess.E6  # Important development squares
    ]

    # Evaluate control of these squares
    for square in key_squares:
        # A square is controlled if it's attacked and not occupied by opponent
        if board.is_attacked_by(chess.WHITE, square):
            score += 15
            # Extra points if we actually occupy the square with our piece
            piece = board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                score += 25

        if board.is_attacked_by(chess.BLACK, square):
            score -= 15
            # Extra points if opponent occupies the square
            piece = board.piece_at(square)
            if piece and piece.color == chess.BLACK:
                score -= 25

    return score


def evaluate_development(board):
    score = 0

    # Only apply this evaluation in the opening phase
    if board.fullmove_number <= 15:
        # Count undeveloped minor pieces
        white_undeveloped = 0
        black_undeveloped = 0

        # Check white's development
        initial_positions = {
            chess.WHITE: {
                chess.KNIGHT: [chess.B1, chess.G1],
                chess.BISHOP: [chess.C1, chess.F1],
                chess.QUEEN: [chess.D1],
                # Don't check rooks since they develop later
            },
            chess.BLACK: {
                chess.KNIGHT: [chess.B8, chess.G8],
                chess.BISHOP: [chess.C8, chess.F8],
                chess.QUEEN: [chess.D8],
            }
        }

        # Count undeveloped pieces with different penalties
        for color, positions in initial_positions.items():
            for piece_type, squares in positions.items():
                for square in squares:
                    piece = board.piece_at(square)
                    if piece and piece.piece_type == piece_type and piece.color == color:
                        if color == chess.WHITE:
                            # Penalty based on piece type - more harsh for bishops than knights
                            if piece_type == chess.BISHOP:
                                white_undeveloped += 45
                            elif piece_type == chess.KNIGHT:
                                white_undeveloped += 30
                            elif piece_type == chess.QUEEN and board.fullmove_number > 8:
                                white_undeveloped += 20
                        else:
                            if piece_type == chess.BISHOP:
                                black_undeveloped += 45
                            elif piece_type == chess.KNIGHT:
                                black_undeveloped += 30
                            elif piece_type == chess.QUEEN and board.fullmove_number > 5:
                                black_undeveloped += 20

        # Apply penalties for undeveloped pieces
        score -= white_undeveloped
        score += black_undeveloped

        # Bonus for controlling center with pawns
        central_pawn_bonus = 0
        for square in [chess.D4, chess.E4, chess.D5, chess.E5]:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    central_pawn_bonus += 35
                else:
                    central_pawn_bonus -= 35
        score += central_pawn_bonus

    return score


def boost_aggressive_tactics(board, losing=False):
    score = 0
    for move in board.legal_moves:
        if board.is_capture(move):
            score += 200
        if board.gives_check(move):
            score += 500 if losing else 20
        if move.promotion:
            score += 1000
    return score


def detect_pawn_breaks(board):
    score = 0
    for move in board.legal_moves:
        piece = board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            if board.is_capture(move) or board.is_en_passant(move):
                score += 400
            elif chess.square_file(move.from_square) == chess.square_file(move.to_square):
                score += 100
    return score


def evaluate_castling(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square is None:
            continue

        if color == chess.WHITE:
            if king_square in [chess.G1, chess.C1]:
                score += 1000
            elif board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
                if king_square == chess.E1:
                    score -= 3000
        else:
            if king_square in [chess.G8, chess.C8]:
                score -= 1000
            elif board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
                if king_square == chess.E8:
                    score += 3000

    return score


def evaluate_king_shield(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square is None:
            continue
        file = chess.square_file(king_square)
        rank = chess.square_rank(king_square)

        shield_squares = []
        if color == chess.WHITE:
            if rank + 1 < 8:
                shield_squares = [chess.square(f, rank + 1) for f in (file - 1, file, file + 1) if 0 <= f < 8]
        else:
            if rank - 1 >= 0:
                shield_squares = [chess.square(f, rank - 1) for f in (file - 1, file, file + 1) if 0 <= f < 8]

        shield_pawns = sum(1 for sq in shield_squares if
                           board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(
                               sq).color == color)

        if shield_pawns < 2:
            if color == chess.WHITE:
                score -= 100
            else:
                score += 100
    return score


def evaluate_tactical_threats(board):
    score = 0

    for move in board.legal_moves:
        from_sq = move.from_square
        to_sq = move.to_square
        piece = board.piece_at(from_sq)
        target = board.piece_at(to_sq)

        # === Prioritize capturing high-value pieces with low-value pieces ===
        if target and piece:
            gain = material_value.get(target.piece_type, 0)
            cost = material_value.get(piece.piece_type, 0)
            if gain > cost:
                score += (gain - cost)  # Tactical profit

        # === Fork detection (attacking multiple pieces at once) ===
        try:
            board.push(move)
            # Only proceed if the move was valid
            if piece:
                attacked = []
                try:
                    attacked = list(board.attacks(to_sq))
                except Exception:
                    pass

                high_value_targets = [
                    sq for sq in attacked if board.piece_at(sq) and
                                             board.piece_at(sq).color != piece.color and
                                             material_value.get(board.piece_at(sq).piece_type, 0) >= 300
                ]
                if len(high_value_targets) >= 2:
                    score += 1500  # fork bonus

            # === Check detection ===
            if board.is_check():
                score += 200

            # === Pin detection: if a piece is pinned to its king ===
            if piece and piece.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                for pinned_sq in board.attacked_by(piece.color, to_sq):
                    pinned_piece = board.piece_at(pinned_sq)
                    if pinned_piece and pinned_piece.color != piece.color:
                        try:
                            if board.is_pinned(pinned_piece.color, pinned_sq):
                                score += 1000  # pin bonus
                                break
                        except Exception:
                            pass
            board.pop()
        except Exception:
            # If any error occurs (like invalid move), skip this move
            if board.move_stack and move == board.peek():
                board.pop()
            continue

        # === Promotion (no need to push) ===
        if move.promotion:
            score += 1000

    return score


def manhattan_distance(sq1, sq2):
    x1, y1 = chess.square_file(sq1), chess.square_rank(sq1)
    x2, y2 = chess.square_file(sq2), chess.square_rank(sq2)
    return abs(x1 - x2) + abs(y1 - y2)


def evaluate_game_phase(board):
    total_phase = 24

    phase = total_phase
    phase -= 4 - len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK))
    phase -= (4 - len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK))) * 0.5
    phase -= (4 - len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK))) * 0.33
    phase -= (4 - len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK))) * 0.33
    return max(0, min(1, phase / total_phase))


def evaluate_center_control(board):
    score = 0

    control_white = 0
    control_black = 0

    for sq in center_squares:
        if board.is_attacked_by(chess.WHITE, sq):
            control_white += 1
        if board.is_attacked_by(chess.BLACK, sq):
            control_black += 1

        piece = board.piece_at(sq)
        if piece:
            if piece.color == chess.WHITE:
                score += 1000
            else:
                score -= 1000

    score += (control_white - control_black) * 20

    if control_white < 2:
        score -= 100
    if control_black < 2:
        score += 100

    return score


def detect_tactical_patterns(board):
    score = 0
    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        is_capture = board.is_capture(move)
        gives_check = board.gives_check(move)

        if is_capture:
            attacker = board.piece_at(move.from_square)
            victim = board.piece_at(move.to_square)
            if attacker and victim:
                attacker_value = material_value.get(attacker.piece_type, 0)
                victim_value = material_value.get(victim.piece_type, 0)
                if victim_value > attacker_value:
                    score += 50

        if gives_check:
            score += 50

        try:
            board.push(move)
            if not board.is_game_over():
                attacked_squares = list(board.attacks(move.to_square))
                if len(attacked_squares) >= 2:
                    score += 20
            board.pop()
        except Exception as e:
            if board.move_stack:
                board.pop()
            continue

    return score


def detect_endgame_advantage(board):
    score = 0
    white_pawns = list(board.pieces(chess.PAWN, chess.WHITE))
    black_pawns = list(board.pieces(chess.PAWN, chess.BLACK))

    if len(white_pawns) == 1 and len(board.piece_map()) <= 4:
        score += 100
    if len(black_pawns) == 1 and len(board.piece_map()) <= 4:
        score -= 100

    return score


def evaluate_king_endgame_activity(board):
    score = 0
    phase = evaluate_game_phase(board)
    if phase < 0.3:
        white_king = board.king(chess.WHITE)
        black_king = board.king(chess.BLACK)

        if white_king is not None:
            white_center_distance = min(manhattan_distance(white_king, center_sq) for center_sq in center_squares)
            score += (7 - white_center_distance) * 20  # càng gần trung tâm càng tốt

        if black_king is not None:
            black_center_distance = min(manhattan_distance(black_king, center_sq) for center_sq in center_squares)
            score -= (7 - black_center_distance) * 20

        if white_king is not None:
            white_rank = chess.square_rank(white_king)
            if white_rank <= 1:  # stuck ở hàng 1 hoặc 2
                score -= 100

        if black_king is not None:
            black_rank = chess.square_rank(black_king)
            if black_rank >= 6:  # stuck ở hàng 7 hoặc 8
                score += 100

    return score


def encourage_rook_on_open_file(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        rooks = board.pieces(chess.ROOK, color)
        for rook_sq in rooks:  # Iterate through rook squares
            file = chess.square_file(rook_sq)
            is_open = True
            is_semi_open = True

            # Check for pawns on the same file
            for rank in range(8):
                sq = chess.square(file, rank)
                piece = board.piece_at(sq)
                if piece and piece.piece_type == chess.PAWN:
                    is_open = False
                    if piece.color == color:  # Own pawn
                        is_semi_open = False

            if is_open:
                score += 100 if color == chess.WHITE else -100  # Increased bonus for open file
            elif is_semi_open:
                score += 50 if color == chess.WHITE else -50  # Bonus for semi-open file

            # Bonus for rooks on the 7th rank (for white) or 2nd rank (for black) - increased
            rook_rank = chess.square_rank(rook_sq)
            if (color == chess.WHITE and rook_rank == 6) or (color == chess.BLACK and rook_rank == 1):
                score += 100 if color == chess.WHITE else -100

    return score


def queen_trade(board):
    score = 0
    white_queen = list(board.pieces(chess.QUEEN, chess.WHITE))
    black_queen = list(board.pieces(chess.QUEEN, chess.BLACK))
    # Only encourage queen trade if we are ahead in material or have a significant advantage
    if white_queen and black_queen:
        material_diff = evaluate_material(board)  # Use material evaluation to assess advantage
        if (board.turn == chess.WHITE and material_diff > 200) or (board.turn == chess.BLACK and material_diff < -200):
            score += 500
    return score


def attack_strength(board):
    attack_score = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            if piece.piece_type == chess.QUEEN:
                attack_score += 5000
            elif piece.piece_type == chess.ROOK:
                attack_score += 4000
            elif piece.piece_type == chess.BISHOP:
                attack_score += 3500
            elif piece.piece_type == chess.KNIGHT:
                attack_score += 3000
            else:
                attack_score += 2000

    opponent_color = not board.turn
    for sq in chess.SQUARES:
        piece_on_sq = board.piece_at(sq)
        if piece_on_sq and piece_on_sq.color == opponent_color:
            if board.is_attacked_by(board.turn, sq):
                attack_score += material_value.get(piece_on_sq.piece_type, 0) // 5  # Example bonus

    return attack_score


def defense_strength(board):
    defense_score = 0

    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            if piece.piece_type == chess.PAWN:
                defense_score += 1000
            elif piece.piece_type == chess.KING:
                defense_score += 3000
            elif piece.piece_type == chess.ROOK:
                defense_score += 2000
            elif piece.piece_type == chess.KNIGHT:
                defense_score += 1500
            elif piece.piece_type == chess.QUEEN:
                defense_score += 2500
            else:
                defense_score += 1750

    king_square = board.king(chess.WHITE)
    if king_square:
        distance_to_center = abs(chess.square_file(king_square) - 3) + abs(chess.square_rank(king_square) - 3)
        defense_score -= distance_to_center

    return defense_score


def evaluate_board(board):
    # Các trường hợp kết thúc ván đấu
    if board.is_checkmate():
        return -999999 if board.turn == chess.WHITE else 999999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Xác định giai đoạn ván đấu chính xác hơn
    phase = evaluate_game_phase(board)

    # Tính toán trọng số dựa vào giai đoạn ván đấu
    material = evaluate_material(board) * 1.0

    # Giai đoạn khai cuộc - ưu tiên phát triển và kiểm soát trung tâm
    if phase > 0.7:  # Khai cuộc
        return material + \
            evaluate_piece_mobility(board) * 0.8 + \
            evaluate_development(board) * 2.5 + \
            evaluate_king_safety(board) * 2.0 + \
            evaluate_center_control(board) * 2.0 + \
            evaluate_pawn_structure(board) * 0.7 + \
            evaluate_castling(board) * 2.0 + \
            evaluate_piece_activation(board) * 2.5 + \
            evaluate_pawn_advances(board) * 1.5 + \
            evaluate_key_squares_control(board) * 1.8 + \
            queen_trade(board) * 0.1 + \
            attack_strength(board) * 0.7 + \
            defense_strength(board) * 1.2

    # Giai đoạn trung cuộc - cân bằng giữa an toàn và tấn công
    elif phase > 0.3:  # Trung cuộc
        return material + \
            evaluate_piece_mobility(board) * 2 + \
            evaluate_tactical_threats(board) * 1.8 + \
            evaluate_king_safety(board) * 2 + \
            evaluate_pawn_structure(board) * 1.2 + \
            evaluate_center_control(board) * 1.5 + \
            detect_tactical_patterns(board) * 1.5 + \
            evaluate_key_squares_control(board) * 1.2 + \
            encourage_rook_on_open_file(board) * 1.5 + \
            attack_strength(board) * 1 + \
            defense_strength(board) * 1.3 + \
            queen_trade(board) * 0.5

    else:  # Tàn cuộc
        return material + \
            evaluate_piece_mobility(board) * 1.8 + \
            evaluate_king_endgame_activity(board) * 3.0 + \
            evaluate_pawn_structure(board) * 2.5 + \
            encourage_rook_on_open_file(board) * 1.8 + \
            detect_endgame_advantage(board) * 2.0 + \
            evaluate_passed_pawns(board) * 3.0 + \
            attack_strength(board) * 0.8 + \
            defense_strength(board) * 1.3 + \
            evaluate_pawn_advances(board) * 0.5

