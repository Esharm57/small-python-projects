
def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

def two_players():
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    current_player = "X"

    while True:
        for row in board:
            print(' | '.join(row))
            print('- '*5)

        row = int(input(f"Player {current_player}, enter row (0, 1, 2): "))
        col = int(input(f"Player {current_player}, enter column (0, 1, 2): "))

        try:
            if board[row][col] != " ":
                print("Cell already taken. Try again.")
                continue

            board[row][col] = current_player

            if check_winner(board, current_player):
                for row in board:
                    print(' | '.join(row))
                    print('- '*5)
                print(f"Player {current_player} wins!")
                break

            if all(cell != " " for row in board for cell in row):
                for row in board:
                    print(' | '.join(row))
                    print('- '*5)
                print("It's a draw!")
                break

            if current_player == "X":
                current_player = "O" 
            else:
                current_player = "X"
        except (IndexError, ValueError):
            print("Invalid input. Please enter row and column as integers between 0 and 2.")

two_players()
