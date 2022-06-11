def chessboard(dimensions):
    new_board = []
    scale = len(str(dimensions[0] * dimensions[1]))
    empty_cell = '_' * scale
    for i in range(dimensions[0]):
        row = []
        for x in range(dimensions[1]):
            row.append(empty_cell)
        new_board.append(row)
    return new_board

def rotate_board(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]

def print_board(old_board):
    new_board = rotate_board(old_board)
    column_n = len(new_board[0])
    row_n = len(new_board)
    border_len = column_n * (cell_size + 1) + 3

    column_numbers = ''.join([str(i + 1).rjust(cell_size + 1) for i in range(column_n)])
    justify_row = len(str(row_n))
    border = ' ' * justify_row + '-' * border_len
    print(border)
    for i in range(row_n, 0, -1):
        row = f'{str(i).rjust(justify_row)}|'
        for x in range(column_n):
            row += ' ' + str(new_board[-i][x]).rjust(cell_size)
        print(row + ' |')
        # print(i)
    print(border)
    print(' ' * (justify_row + 1) + column_numbers)

def check_input(coords, message='', max_row=100, max_col=100, moves=[[0, 0]], valid_moves=[]):

    if len(coords) != 2:
        print(message)
        return False

    for n, i in enumerate(coords):
        try:
            coords[n] = int(i)
        except ValueError:
            print(message)
            return False

    for i in coords:
        if i < 1:
            print(message)
            return False

    if coords[0] > max_row:
        print(message)
        return False
    if coords[1] > max_col:
        print(message)
        return False

    if coords in moves:
        return False

    if valid_moves:
        if coords not in valid_moves:
            return False

    return True

def place_piece(board, coords, symbol='X'):
    x = coords[0] - 1
    y = coords[1] - 1
    board[x][y] = symbol.rjust(cell_size)
    return board

def place_moves(board, moves):
    for move in moves:
        x = move[0] - 1
        y = move[1] - 1
        z = move[-1]
        board[x][y] = str(z).rjust(cell_size)

    return board


def possible_moves(board, coords):
    knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (1, -2), (-1, -2))
    can_move = []
    boundaries = len(board), len(board[0])
    for move in knight_moves:
        x = coords[0] + move[0]
        y = coords[1] + move[1]
        if 0 < x <= boundaries[0] and 0 < y <= boundaries[1] and board[x - 1][y - 1] == ('_' * cell_size):
            can_move.append([x, y])
    return can_move


def play_KTP(board, piece):
    # piece = fix_coords(piece_co)
    board = place_piece(board, piece)
    piece_moves = possible_moves(board, piece)
    next_possible_moves = []
    for move in piece_moves:
        moves = possible_moves(board, move)
        next_possible_moves.append([move[0], move[1], len(moves)])

    board = place_moves(board, next_possible_moves)
    print_board(board)
    board = place_piece(board, piece, symbol="*")  # update with star
    old_moves = [piece]  # where have we been

    while next_possible_moves:
        piece = input("Enter your next move:").split()
        # print(next_possible_moves)
        while not check_input(piece, message='Invalid move!', max_row=coords[0], max_col=coords[1], moves=old_moves,
                              valid_moves=piece_moves):
            piece = input("Invalid move! Enter your next move:").split()
        board = chessboard(coords)
        for old_piece in old_moves:
            board = place_piece(board, old_piece, symbol="*")

        board = place_piece(board, piece)

        piece_moves = possible_moves(board, piece)
        next_possible_moves = []
        for move in piece_moves:
            if move not in old_moves:
                moves = possible_moves(board, move)
                next_possible_moves.append([move[0], move[1], len(moves)])
        board = place_moves(board, next_possible_moves)

        print_board(board)
        board = place_piece(board, piece, symbol="*")
        old_moves.append(piece)
        # print(old_moves)
        # print(next_possible_moves)

    if len(old_moves) == (coords[0] * coords[1]):
        print('What a great tour! Congratulations!')
    else:
        print('No more possible moves!')
        print(f'Your knight visited {len(old_moves)} squares!')

def solve_ktp_wdorff(solution_board, coords):
    x = coords[0] - 1
    y = coords[1] - 1

    solution_board[x][y] = 1

    # print_board(board)

    pos_counter = 2

    next_move = piece_start
    while next_move and pos_counter <= squares:
        moves = possible_moves(solution_board, next_move)
        min_moves = 8
        for move in moves:
            access = len(possible_moves(solution_board, move))
            if access < min_moves and solution_board[move[0] - 1][move[1] - 1] == ('_' * cell_size):
                next_move = move
                min_moves = access

        if solution_board[next_move[0] - 1][next_move[1] - 1] == ('_' * cell_size):
            solution_board[next_move[0] - 1][next_move[1] - 1] = pos_counter
        # elif pos_counter == squares:
        #     solution_board[next_move[0] - 1][next_move[1] - 1] = pos_counter
        else:
            return False
        pos_counter += 1
        # print(access)
        # print_board(solution_board)
        # print(pos_counter)
        # print(next_move)

    return solution_board

coords = input("Enter your board dimensions:").split()
while not check_input(coords, message='Invalid dimensions!'):
    coords = input("Enter your board dimensions:").split()
piece_start = input("Enter the knight's starting position:").split()
while not check_input(piece_start, message='Invalid position!', max_row=coords[0], max_col=coords[1]):
    piece_start = input("Enter the knight's starting position:").split()

# print(piece_start)
# print(coords)
board = chessboard(coords)
solve_board = chessboard(coords)
cell_size = len(str(len(board[0]) * len(board)))

board_size = len(board), len(board[0])

squares = board_size[0] * board_size[1]

try_puzzle = input("Do you want to try the puzzle? (y/n)")
while try_puzzle.lower() not in ['y', 'n']:
    print('Invalid input! ')
    try_puzzle = input("Do you want to try the puzzle? (y/n)")

solution = solve_ktp_wdorff(solve_board, piece_start)

if try_puzzle == 'n':
    if solution:
        print("Here's the solution!")
        print_board(solution)
    else:
        print("No solution exists!")
elif try_puzzle == 'y':
    if solution:
        play_KTP(board, piece_start)
    else:
        print("No solution exists!")
