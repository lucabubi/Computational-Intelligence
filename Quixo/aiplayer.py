import random
from copy import deepcopy
from game import Game, Move, Player

class AIPlayer(Player):
    def __init__(self, max_depth: int) -> None:
        super().__init__()
        self.max_depth = max_depth
        match max_depth:
            case 1:
                self.name = "Dumb AI"
            case 2:
                self.name = "Weak AI"
            case 3:
                self.name = "Strong AI"
            case 4:
                self.name = "GODLIKE AI"
            case _:
                self.name = "Undefined AI"

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        """Wrapper that returns the best move for the AI player using the minimax algorithm"""
        moves = game.get_possible_moves(game.get_current_player())
        best_score = float("-inf")
        best_move = None
        alpha = float("-inf")
        beta = float("inf")
        for move in moves:
            virtual_game = deepcopy(game)
            # ignoring acceptable return value supposing that get_possible_moves always returns the FULL list of valid moves
            virtual_game.move(move[0], move[1], game.get_current_player())
            score = self.minimax(virtual_game, self.max_depth-1, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = move
        if best_move:
            return best_move
        # if every move is a win/loss, return a random move
        else:
            return random.choice(moves)

    def minimax(self, game: 'Game', depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or game.check_winner() != -1:
            return self.evaluate(game)
        if maximizing:
            max_eval = float("-inf")
            for from_pos, slide in game.get_possible_moves(game.get_current_player()):
                new_game = deepcopy(game)
                # ignoring acceptable return value supposing that get_possible_moves always returns the FULL list of valid moves
                new_game.move(from_pos, slide, game.get_current_player())
                eval = self.minimax(new_game, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for from_pos, slide in game.get_possible_moves((game.get_current_player()+1)%2):
                new_game = deepcopy(game)
                # ignoring acceptable return value supposing that get_possible_moves always returns the FULL list of valid moves
                new_game.move(from_pos, slide, ((game.get_current_player()+1)%2))
                eval = self.minimax(new_game, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, game: Game) -> float:
        """Evaluation function that returns the difference between the number of pieces of the AI player and the opponent player (if no winner is found)"""
        current_player = game.get_current_player()
        opponent_player = ((current_player + 1) % 2)
        winner = game.check_winner()
        if winner == current_player:
            return float('inf') # AI player wins
        elif winner == opponent_player:
            return float('-inf') # Opponent wins
        current_count = sum([1 for row in game.get_board() for piece in row if piece == current_player])
        opponent_count = sum([1 for row in game.get_board() for piece in row if piece == opponent_player])
        return current_count - opponent_count