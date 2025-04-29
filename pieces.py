import chess

PIECE_VALUES = {
    chess.PAWN: [
        0, 5, 5, 5, 5, 5, 5, 0,
        5, 10, 10, 10, 10, 10, 10, 5,
        5, 10, 15, 15, 15, 15, 10, 5,
        10, 15, 20, 20, 20, 20, 15, 10,
        10, 15, 20, 25, 25, 20, 15, 10,
        15, 20, 30, 35, 35, 30, 20, 15,
        20, 30, 35, 40, 40, 35, 30, 20,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],

    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ],
    chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -10,  0,  5,  10,  10,  5,  0, -10,
        -10,   5,  5,  10,  10,  5,   5, -10,
        -10,   0,   10,  10,  10,   10,   0, -10,
        -10,   10,   10,  10,  10,   10,   10, -10,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ],
    chess.ROOK: [
        0,  0,  5,  5,  5,  5,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
       -5,  0,  0,  5,  5,  0,  0, -5,
       -5,  0,  0,  5,  5,  0,  0, -5,
       -5,  0,  0,  5,  5,  0,  0, -5,
       -5,  0,  0,  5,  5,  0,  0, -5,
        5,  0,  0,  5,  5,  0,  0,  5,
        0,  0,  5, 10, 10,  5,  0,  0,
    ],
    chess.QUEEN: [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20,
    ],
    chess.KING: [
        -50, -40, -30, -20, -20, -30, -40, -50,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -20, 20, 30, 30, 20, -20, -30,
        -50, -40, -30, -20, -20, -30, -40, -50,
    ],
}

KING_ENDGAME_VALUES = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -20, 20, 30, 30, 20, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50,
    -50, -40, -30, -20, -20, -30, -40, -50,
]

material_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 350,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 10000
}

center_squares = [
    chess.D4, chess.D5, chess.E4, chess.E5,
]

transposition_table = {}
opening_book = {
    "rnbqkbnr/pppp1ppp/8/4p3/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2": "d5",  # Center opening response
    # King's Pawn Opening
    # Sicilian Defense
    "rnbqkbnr/pppp1ppp/8/4p3/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq - 0 3": "Nf6",  # Development, response to e4
    "rnbqkbnr/pp1ppppp/8/2p5/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 3": "g6",  # King's Indian Defense
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 2": "d5",  # Center opening
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2": "c4",  # English Opening
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2": "g6",  # King's Indian Defense
    "rnbqkb1r/pppp1ppp/4pn2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 3": "Bb4",  # French Defense
    "rnbqkbnr/pp1ppppp/8/2p5/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2": "c6",  # Sicilian Defense: Classical Variation
    # Open Game
    "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1": "c5",  # Closed Game
    # Scandinavian Defense
    "rnbqkbnr/pppp1ppp/8/4p3/2P5/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1": "g3",  # English Opening: Botvinnik System
    # King's Indian Defense
    "rnbqkb1r/pppppppp/5n2/8/4P3/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2": "e5",  # King's Pawn Opening
    "rnbqkbnr/pppp1ppp/8/2p5/2P5/8/PPP1PPPP/RNBQKBNR b KQkq - 0 2": "c5",  # Closed Game
    # King's Pawn Opening
    "rnbqkbnr/pp1ppppp/8/2p5/3P4/8/PPP2PPP/RNBQKBNR b KQkq - 0 2": "e5",  # Scotch Game
    "rnbqkbnr/pppppppp/8/8/2P5/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2": "d4",  # Queen's Pawn Opening
    # Vienna Game
    "rnbqkbnr/pppppppp/8/8/2P5/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1": "d6",  # Pirc Defense
    # Dutch Defense
    "rnbqkbnr/pppp1ppp/8/4p3/3PP3/2N2N2/PPP2PPP/RNBQKBNR b KQkq - 0 3": "Nf6",  # Petrov Defense (Russian Defense)
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1": "c5",  # Symmetrical Variation of the English Opening
    "rnbqkbnr/ppp1pppp/3p4/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2": "d4",  # King's Gambit Declined
    "rnbqkbnr/pppppppp/8/8/2P5/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1": "Nf3",  # Zukertort Opening
}
