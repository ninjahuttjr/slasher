class TicTacToeAI:
    def __init__(self, board, my_symbol):
        self.board = board
        self.my_symbol = my_symbol
        self.opponent_symbol = -my_symbol

    def minimax(self, board, depth, maximizing):
        if self.check_winner(board) == self.my_symbol:
            return 10 - depth
        if self.check_winner(board) == self.opponent_symbol:
            return depth - 10

        if all(cell != 0 for row in board for cell in row):
            return 0

        if maximizing:
            max_eval = float('-inf')
            for x in range(3):
                for y in range(3):
                    if board[y][x] == 0:
                        board[y][x] = self.my_symbol
                        eval = self.minimax(board, depth + 1, False)
                        board[y][x] = 0
                        max_eval = max(eval, max_eval)
            return max_eval

        else:
            min_eval = float('inf')
            for x in range(3):
                for y in range(3):
                    if board[y][x] == 0:
                        board[y][x] = self.opponent_symbol
                        eval = self.minimax(board, depth + 1, True)
                        board[y][x] = 0
                        min_eval = min(eval, min_eval)
            return min_eval

    def make_move(self):
        best_val = float('-inf')
        best_move = None

        for x in range(3):
            for y in range(3):
                if self.board[y][x] == 0:
                    self.board[y][x] = self.my_symbol
                    move_val = self.minimax(self.board, 0, False)
                    self.board[y][x] = 0
                    if move_val > best_val:
                        best_move = (x, y)
                        best_val = move_val

        return best_move

    def check_winner(self, board):
        for row in board:
            if row[0] == row[1] == row[2] != 0:
                return row[0]
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != 0:
                return board[0][col]
        if board[0][0] == board[1][1] == board[2][2] != 0:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            return board[0][2]
        return None
