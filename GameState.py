from copy import deepcopy
from meta import GameMeta


class ConnectState:
    def __init__(self):
        self.board = [[0] * GameMeta.COLS for _ in range(GameMeta.ROWS)]
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
        return [col for col in range(GameMeta.COLS) if self.board[0][col] == 0]

    def check_win(self):
        if len(self.last_played) > 0 and self.check_win_from(
            self.last_played[0], self.last_played[1]
        ):
            return self.board[self.last_played[0]][self.last_played[1]]
        else:
            return 0

    def check_win_from(self, row, col):
        player = self.board[row][col]

        return (
            self.check_row(row, col, player)
            or self.check_col(row, col, player)
            or self.check_diagonals(row, col, player)
        )

    def game_over(self):
        return self.check_win() or len(self.get_legal_moves()) == 0

    def get_outcome(self):
        if len(self.get_legal_moves()) == 0 and self.check_win() == 0:
            return GameMeta.OUTCOMES["draw"]

        return (
            GameMeta.OUTCOMES["one"]
            if self.to_play == GameMeta.PLAYERS["two"]
            else GameMeta.PLAYERS["two"]
        )

    def print(self):
        print("=============================")

        for row in range(GameMeta.ROWS):
            for col in range(GameMeta.COLS):
                print(
                    "| {}".format(
                        "X"
                        if self.board[row][col] == 1
                        else "O"
                        if self.board[row][col] == 2
                        else " "
                    ),
                    end=" ",
                )
            print("|")

        print("=============================")

    # Returns True if piece placed at [row][col] ends the game by
    # completing a horizontal 4 in a row, False otherwise
    def check_row(self, row, col, player):
        consecutive = 0
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
    def check_col(self, row, col, player):
        consecutive = 0
        start_index = max(0, row - 3)
        end_index = min(row + 3, GameMeta.ROWS)
        for i in range(start_index, end_index):
            if self.board[i][col] == player:
                consecutive += 1
                if consecutive == 4:
                    return True
            else:
                consecutive = 0
        return False

    # Returns True if piece placed at [row][col] ends the game by
    # completing a diagonal 4 in a row, False otherwise
    def check_diagonals(self, row, col, player):
        # Check diagonals with positive slope (e.g., /)
        consecutive = 0
        for i in range(-3, 4):
            current_row = row + i
            current_col = col + i
            if 0 <= current_row < GameMeta.ROWS and 0 <= current_col < GameMeta.COLS:
                if self.board[current_row][current_col] == player:
                    consecutive += 1
                    if consecutive == 4:
                        return True
                else:
                    consecutive = 0

        # Check diagonals with negative slope (e.g., \)
        consecutive = 0
        for i in range(-3, 4):
            current_row = row - i
            current_col = col + i
            if 0 <= current_row < GameMeta.ROWS and 0 <= current_col < GameMeta.COLS:
                if self.board[current_row][current_col] == player:
                    consecutive += 1
                    if consecutive == 4:
                        return True
                else:
                    consecutive = 0

        return False


def main():
    pass


if __name__ == "__main__":
    main()
