from rich.console import Console
from rich.prompt import Prompt
from game import Game, Move, Player

class HumanPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Human"
        self.console = Console()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        while True:
            try:
                move_input = Prompt.ask("Enter your move in the format x y move")
                x, y, move_str = move_input.split()
                x, y = int(x), int(y)
                match move_str:
                    case "top":
                        move = Move.TOP
                    case "bottom":
                        move = Move.BOTTOM
                    case "left":
                        move = Move.LEFT
                    case "right":
                        move = Move.RIGHT
                    case _:
                        raise ValueError
                if ((x, y), move) in game.get_possible_moves(game.get_current_player()):
                    return ((x, y), move)
                else:
                    raise ValueError
            except ValueError:
                self.console.print(f"Format and/or move is invalid. Please enter a valid move in the format x y move! (ex. 0 0 bottom)", style="bold red")