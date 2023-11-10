from copy import deepcopy
from meta import GameMeta


class ConnectState:
    def __init__(self):
        self.board = [[0] * GameMeta.COLS for _ in GameMeta.ROWS]
        self.to_play = GameMeta.PLAYERS["one"]
        self.height = [GameMeta.ROWS - 1] * GameMeta.COLS
        self.last_played = []

    def get_board(self):
        return deepcopy(self.board)

    def move(self, col):
        self.board[self.height[col]][col] = self.to_play
        self.last_played = [self.height[col], col]
        self.height[col] -= 1
        self.to_play = (
            GameMeta.PLAYERS["two"]
            if self.to_play == GameMeta.PLAYERS["one"]
            else GameMeta.PLAYERS["one"]
        )

    def get_legal_moves(self):
        return [col for col in GameMeta.COLS if self.board[0][col] == 0]

    def check_win(self):
        if len(self.last_played) > 0 and self.check_win_from(
            self.last_played[0], self.last_played[1]
        ):
            return self.board[self.last_played[0]][self.last_played[1]]
        else:
            return 0

    def check_win_from(self, row, col):
        player = self.board[row][col]

        consecutive = 0

    # Returns True if piece placed at [row][col] ends the game by
    # completing a horizontal 4 in a row, False otherwise
    def check_row(self, row, col):
        consecutive = 0
        player = self.board[row][col]
        start_index = max(0, col - 3)
        end_index = min(col + 3, GameMeta.COLS)
        for i in range(start_index, end_index):
            if self.board[row][i] == player:
                consecutive += 1
                if consecutive == 4:
                    return True
            else:
                consecutive = 0
        return False
    
    # Returns True if piece placed at [row][col] ends the game by
    # completing a vertical 4 in a row, False otherwise
    def check_col(self, row, col):
        consecutive = 0
        player = self.board[row][col]
        start_index = max(0, row - 3)
        end_index = min(row + 3, GameMeta.ROWS)
        for i in range(start_index, end_index):
            if self.board[i][row] == player:
                consecutive += 1
                if consecutive == 4:
                    return True
            else:
                consecutive = 0
        return False
    
    # Returns True if piece placed at [row][col] ends the game by
    # completing a diagonal 4 in a row, False otherwise
    def check_diagonals(self, row, col):
        consecutive = 0
        player = self.board[row][col]
        left_index = max(0, col - 3)
        right_index = min(col + 3, GameMeta.COLS)
        bottom_index = max(0, row - 3)
        top_index = min(row + 3, GameMeta.ROWS)

        for x in range(left_index, right_index):
            if 
            if self.board[i][row] == player:
                consecutive += 1
                if consecutive == 4:
                    return True
            else:
                consecutive = 0
        return False

