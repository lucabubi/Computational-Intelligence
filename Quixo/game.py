from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
import os
import numpy as np
from rich import box, print
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

class Move(Enum):
    '''
    Selects where you want to place the taken piece. The rest of the pieces are shifted
    '''
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

class Player(ABC):
    def __init__(self) -> None:
        '''You can change this for your player if you need to handle state/have memory'''
        pass

    @abstractmethod
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        '''
        The game accepts coordinates of the type (X, Y). X goes from left to right, while Y goes from top to bottom, as in 2D graphics.
        Thus, the coordinates that this method returns shall be in the (X, Y) format.

        game: the Quixo game. You can use it to override the current game with yours, but everything is evaluated by the main game
        return values: this method shall return a tuple of X,Y positions and a move among TOP, BOTTOM, LEFT and RIGHT
        '''
        pass

class Game(object):
    def __init__(self) -> None:
        self._board = np.ones((5, 5), dtype=np.uint8) * -1
        self.current_player_idx = 1

    def get_board(self) -> np.ndarray:
        '''
        Returns the board
        '''
        return deepcopy(self._board)

    def get_current_player(self) -> int:
        '''
        Returns the current player
        '''
        return deepcopy(self.current_player_idx)

    def print(self):
        '''Prints the board. -1 are neutral pieces, 0 are pieces of player 0, 1 pieces of player 1'''
        print(self._board)

    def check_winner(self) -> int:
        '''Check the winner. Returns the player ID of the winner if any, otherwise returns -1'''
        # for each row
        for x in range(self._board.shape[0]):
            # if a player has completed an entire row
            if self._board[x, 0] != -1 and all(self._board[x, :] == self._board[x, 0]):
                # return the relative id
                return self._board[x, 0]
        # for each column
        for y in range(self._board.shape[1]):
            # if a player has completed an entire column
            if self._board[0, y] != -1 and all(self._board[:, y] == self._board[0, y]):
                # return the relative id
                return self._board[0, y]
        # if a player has completed the principal diagonal
        if self._board[0, 0] != -1 and all(
            [self._board[x, x]
                for x in range(self._board.shape[0])] == self._board[0, 0]
        ):
            # return the relative id
            return self._board[0, 0]
        # if a player has completed the secondary diagonal
        if self._board[0, -1] != -1 and all(
            [self._board[x, -(x + 1)]
            for x in range(self._board.shape[0])] == self._board[0, -1]
        ):
            # return the relative id
            return self._board[0, -1]
        return -1

    def play(self, player1: Player, player2: Player, interactive: bool = False) -> int:
        '''Play the game. Returns the winning player, if any. For draws return value is 10'''
        players = [player1, player2]
        winner = -1
        move_history = []
        while winner < 0:
            self.current_player_idx += 1
            self.current_player_idx %= len(players)
            ok = False
            self.print_dashboard(player1, player2,
                                " | ".join([" ".join(map(str, move[1])) for move in move_history if move[0] == player1]),
                                " | ".join([" ".join(map(str, move[1])) for move in move_history if move[0] == player2])
                                ) if interactive else None
            while not ok:
                from_pos, slide = players[self.current_player_idx].make_move(self)
                ok = self.move(from_pos, slide, self.current_player_idx)
            move_history.append((players[self.current_player_idx],(from_pos, slide)))
            winner = self.check_winner()
            if winner == -1: # if no winner is found
                winner = self.check_draw([move[1] for move in move_history]) # Exclude the information regarding who made that move. If draw found return 10 else still -1
            if winner >= 0 and interactive:
                self.print_dashboard(player1, player2,
                                    " | ".join([" ".join(map(str, move[1])) for move in move_history if move[0] == player1]),
                                    " | ".join([" ".join(map(str, move[1])) for move in move_history if move[0] == player2])
                                    ) if interactive else None
                self.print_winner(winner, player1 if winner == 0 else player2)
        return winner

    def move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        '''Perform a move'''
        if player_id > 2:
            return False
        # Oh God, Numpy arrays
        prev_value = deepcopy(self._board[(from_pos[1], from_pos[0])])
        acceptable = self.__take((from_pos[1], from_pos[0]), player_id)
        if acceptable:
            acceptable = self.__slide((from_pos[1], from_pos[0]), slide)
            if not acceptable:
                self._board[(from_pos[1], from_pos[0])] = deepcopy(prev_value)
        return acceptable

    def __take(self, from_pos: tuple[int, int], player_id: int) -> bool:
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (self._board[from_pos] < 0 or self._board[from_pos] == player_id)
        if acceptable:
            self._board[from_pos] = player_id
        return acceptable

    def __slide(self, from_pos: tuple[int, int], slide: Move) -> bool:
        '''Slide the other pieces'''
        # define the corners
        SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
        # if the piece position is not in a corner
        if from_pos not in SIDES:
            # if it is at the TOP, it can be moved down, left or right
            acceptable_top: bool = from_pos[0] == 0 and (
                slide == Move.BOTTOM or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is at the BOTTOM, it can be moved up, left or right
            acceptable_bottom: bool = from_pos[0] == 4 and (
                slide == Move.TOP or slide == Move.LEFT or slide == Move.RIGHT
            )
            # if it is on the LEFT, it can be moved up, down or right
            acceptable_left: bool = from_pos[1] == 0 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.RIGHT
            )
            # if it is on the RIGHT, it can be moved up, down or left
            acceptable_right: bool = from_pos[1] == 4 and (
                slide == Move.BOTTOM or slide == Move.TOP or slide == Move.LEFT
            )
        # if the piece position is in a corner
        else:
            # if it is in the upper left corner, it can be moved to the right and down
            acceptable_top: bool = from_pos == (0, 0) and (
                slide == Move.BOTTOM or slide == Move.RIGHT)
            # if it is in the lower left corner, it can be moved to the right and up
            acceptable_left: bool = from_pos == (4, 0) and (
                slide == Move.TOP or slide == Move.RIGHT)
            # if it is in the upper right corner, it can be moved to the left and down
            acceptable_right: bool = from_pos == (0, 4) and (
                slide == Move.BOTTOM or slide == Move.LEFT)
            # if it is in the lower right corner, it can be moved to the left and up
            acceptable_bottom: bool = from_pos == (4, 4) and (
                slide == Move.TOP or slide == Move.LEFT)
        # check if the move is acceptable
        acceptable: bool = acceptable_top or acceptable_bottom or acceptable_left or acceptable_right
        # if it is
        if acceptable:
            # take the piece
            piece = self._board[from_pos]
            # if the player wants to slide it to the left
            if slide == Move.LEFT:
                # for each column starting from the column of the piece and moving to the left
                for i in range(from_pos[1], 0, -1):
                    # copy the value contained in the same row and the previous column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i - 1)]
                # move the piece to the left
                self._board[(from_pos[0], 0)] = piece
            # if the player wants to slide it to the right
            elif slide == Move.RIGHT:
                # for each column starting from the column of the piece and moving to the right
                for i in range(from_pos[1], self._board.shape[1] - 1, 1):
                    # copy the value contained in the same row and the following column
                    self._board[(from_pos[0], i)] = self._board[(
                        from_pos[0], i + 1)]
                # move the piece to the right
                self._board[(from_pos[0], self._board.shape[1] - 1)] = piece
            # if the player wants to slide it upward
            elif slide == Move.TOP:
                # for each row starting from the row of the piece and going upward
                for i in range(from_pos[0], 0, -1):
                    # copy the value contained in the same column and the previous row
                    self._board[(i, from_pos[1])] = self._board[(
                        i - 1, from_pos[1])]
                # move the piece up
                self._board[(0, from_pos[1])] = piece
            # if the player wants to slide it downward
            elif slide == Move.BOTTOM:
                # for each row starting from the row of the piece and going downward
                for i in range(from_pos[0], self._board.shape[0] - 1, 1):
                    # copy the value contained in the same column and the following row
                    self._board[(i, from_pos[1])] = self._board[(
                        i + 1, from_pos[1])]
                # move the piece down
                self._board[(self._board.shape[0] - 1, from_pos[1])] = piece
        return acceptable

    def get_possible_moves(self, player: int) -> list[tuple[tuple[int, int], Move]]:
        """Returns a list of possible moves for the specified player"""
        moves = []
        for x in range(0,5):
            for y in range(0,5):
                # if cube is different from the other player.
                if self.get_board()[(y, x)] != ((player+1)%2):
                    match (x, y):
                        case (0, 0):
                            moves.append(((x, y), Move.BOTTOM))
                            moves.append(((x, y), Move.RIGHT))
                        case (0, 4):
                            moves.append(((x, y), Move.TOP))
                            moves.append(((x, y), Move.RIGHT))
                        case (4, 0):
                            moves.append(((x, y), Move.BOTTOM))
                            moves.append(((x, y), Move.LEFT))
                        case (4, 4):
                            moves.append(((x, y), Move.TOP))
                            moves.append(((x, y), Move.LEFT))
                        case _:
                            if y == 0:
                                moves.append(((x, y), Move.BOTTOM))
                                moves.append(((x, y), Move.LEFT))
                                moves.append(((x, y), Move.RIGHT))
                            elif x == 0:
                                moves.append(((x, y), Move.TOP))
                                moves.append(((x, y), Move.BOTTOM))
                                moves.append(((x, y), Move.RIGHT))
                            elif y == 4:
                                moves.append(((x, y), Move.TOP))
                                moves.append(((x, y), Move.LEFT))
                                moves.append(((x, y), Move.RIGHT))
                            elif x == 4:
                                moves.append(((x, y), Move.TOP))
                                moves.append(((x, y), Move.BOTTOM))
                                moves.append(((x, y), Move.LEFT))
        return moves

    def check_draw(self, move_history: list) -> int:
        '''Check if the game is a draw. Returns 10 otherwise still -1'''
        if self.check_repeated_pattern(move_history) or len(move_history) > 60:
            return 10
        return -1

    def check_repeated_pattern(self, move_history: list, pattern_length: int = 10) -> bool:
        '''Check if the game is a draw due to a repeated pattern of moves. Returns True if a (pattern_length) pattern is found, False otherwise'''
        if len(move_history) < 2 * pattern_length:
            return False
        last_sequence = move_history[-pattern_length:] # extract the last pattern_length sequence of moves
        for i in range(len(move_history) - 2 * pattern_length):
            if move_history[i:i + pattern_length] == last_sequence:
                return True
        return False

    def print_dashboard(self, player1: Player, player2: Player, move_history_p1: str, move_history_p2: str):
        '''Prints the board and move history'''
        fixed_console = Console(height=20)
        main_layout = Layout()
        main_layout.split_column(Layout(name="first_row", size=4), Layout(name="second_row"))
        main_layout["second_row"].split_row(Layout(name="left_column",ratio=2), Layout(name="right_column",ratio=5))
        main_layout["right_column"].split_column(Layout(name="right_column_top"), Layout(name="right_column_bottom"))
        os.system('cls' if os.name == 'nt' else 'clear')
        table = Table(show_header=False, box=box.ROUNDED, border_style="bold white", show_lines=True, title="Game Board", title_style="bold white")
        # Add columns for each column in the board
        for _ in range(self._board.shape[1]):
            table.add_column(width=2)
        # Fill the table with values from the board
        for row in self._board:
            row_data = ["🔴" if cell == 0 else "🟣" if cell == 1 else "" for cell in row]
            table.add_row(*row_data)
        main_layout["first_row"].update(Align.center(Panel(f"You're playing as {'[red]🔴 first[/red]' if player1.name == 'Human' else '[violet]🟣 second[/violet]'} against {player1.name if player1.name != 'Human' else player2.name}", title="Game Recap", style="bold white")))
        main_layout["left_column"].update(table)
        main_layout["right_column_top"].update(Panel(move_history_p1, style="bold white", title="Player 1 Move History"))
        main_layout["right_column_bottom"].update(Panel(move_history_p2, style="bold white", title="Player 2 Move History"))
        fixed_console.print(main_layout)
        print("")

    def print_winner(self, winner: int, winner_player: Player):
        console = Console()
        if winner == 10:
            message = "It's a draw!"
            style = "bold yellow"
        elif winner == 0 and winner_player.name == "Human":
            message = "You won! Congratulations! 🎉"
            style = "bold green"
        else:
            message = "Unfortunately you lost!"
            style = "bold red"
        styled_message = Text(message, style=style, justify="center")
        console.print(Panel(styled_message, title="GAME ENDED!", style=style, expand=True))
        console.print("")