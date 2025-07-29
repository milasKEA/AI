import math
import copy

ROWS = 6
COLS = 7

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (2 * COLS + 1))
    print(' ' + ' '.join(str(i) for i in range(COLS)))

def is_valid_location(board, col):
    return board[0][col] == ' '

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Horizontal, vertical, and diagonal checks
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = 'X' if piece == 'O' else 'O'
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(' ') == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(' ') == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    center_array = [board[r][COLS // 2] for r in range(ROWS)]
    score += center_array.count(piece) * 3
    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

def is_terminal_node(board):
    return winning_move(board, 'X') or winning_move(board, 'O') or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 'O'):
                return (None, 1e14)
            elif winning_move(board, 'X'):
                return (None, -1e14)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 'O'))
    if maximizingPlayer:
        value = -math.inf
        best_col = None
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, 'O')
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = None
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, 'X')
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def human_move(board, piece):
    valid_move = False
    while not valid_move:
        try:
            col = int(input(f"Spiller {piece} - vælg kolonne (0-6): "))
            if 0 <= col < COLS and is_valid_location(board, col):
                valid_move = True
            else:
                print("Ugyldigt valg, prøv igen.")
        except ValueError:
            print("Skriv et tal mellem 0 og 6.")
    return col

def play_game(two_players=False):
    board = create_board()
    game_over = False
    turn = 0

    print_board(board)
    while not game_over:
        if turn == 0:
            col = human_move(board, 'X')
        else:
            if two_players:
                col = human_move(board, 'O')
            else:
                print("AI tænker...")
                col, _ = minimax(board, 4, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            piece = 'X' if turn == 0 else 'O'
            drop_piece(board, row, col, piece)

            print_board(board)

            if winning_move(board, piece):
                print(f"Spiller {piece} vinder!")
                game_over = True
            elif not get_valid_locations(board):
                print("Uafgjort!")
                game_over = True

            turn = (turn + 1) % 2

if __name__ == "__main__":
    print("Velkommen til Connect Four!")
    mode = input("Vil du spille mod en anden spiller? (ja/nej): ").strip().lower()
    play_game(two_players=(mode == "ja"))
