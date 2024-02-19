import random
from game import Game, Move, Player

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Random"

    # Includes invalid moves... for a legal random move use random.choice(game.get_possible_moves(game.get_current_player()))
    def random_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        return self.random_move(game)