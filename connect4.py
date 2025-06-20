import math
import copy
import random

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
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and \
               board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and \
               board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and \
               board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and \
               board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False


import random

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

    # Score center column
    center_array = [board[r][COLS // 2] for r in range(ROWS)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROWS):
        row_array = [board[r][c] for c in range(COLS)]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonals
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
                return (None, 100000000000000)
            elif winning_move(board, 'X'):
                return (None, -10000000000000)
            else:  # Game over, no more valid moves
                return (None, 0)
        else:  # Depth is 0
            return (None, score_position(board, 'O'))  # AI is 'O'

    if maximizingPlayer:
        value = -math.inf
        best_col = None
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, 'O')  # AI move
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Prune branch
        return best_col, value
    else:
        value = math.inf
        best_col = None
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, row, col, 'X')  # Human move
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break  # Prune branch
        return best_col, value

def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 for Player, 1 for AI

    while not game_over:
        print_board(board)
        if turn == 0:
            # Human move
            col = int(input("Player 1 Make your Selection (0-6):"))
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 'X')
                if winning_move(board, 'X'):
                    print("Player wins!")
                    game_over = True
            else:
                print("Invalid move. Try again.")
        else:
            # AI move
            print("AI is thinking...")
            col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 'O')
                if winning_move(board, 'O'):
                    print("AI wins!")
                    game_over = True
        turn = (turn + 1) % 2

if __name__ == "__main__":
    main()

def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 for Player, 1 for AI

    while not game_over:
        print_board(board)
        if turn == 0:
            # Human's turn
            valid_move = False
            while not valid_move:
                try:
                    col = int(input("Your turn - select column (0-6): "))
                    if 0 <= col < COLS and is_valid_location(board, col):
                        valid_move = True
                    else:
                        print("Invalid move. Try again.")
                except:
                    print("Please enter a valid number between 0 and 6.")
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 'X')  # Human is 'X'
            if winning_move(board, 'X'):
                print_board(board)
                print("Congratulations! You win!")
                game_over = True
        else:
            # AI's turn
            print("AI is thinking...")
            col, _ = minimax(board, 4, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 'O')  # AI is 'O'
                if winning_move(board, 'O'):
                    print_board(board)
                    print("AI wins! Better luck next time.")
                    game_over = True

        # Check for draw
        if not game_over and len(get_valid_locations(board)) == 0:
            print_board(board)
            print("It's a draw!")
            break

        turn = (turn + 1) % 2

if __name__ == "__main__":
    main()
