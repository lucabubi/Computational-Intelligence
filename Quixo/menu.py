import os
import sys
import time
from rich.align import Align
from rich.console import Console
from rich_menu import Menu
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from tqdm import tqdm
from aiplayer import AIPlayer
from game import Game
from human import HumanPlayer
from randomplayer import RandomPlayer

class QuixoMenu():
    def __init__(self) -> None:
        self.console = Console()
        self.main_content = ["Play against AI", "Evaluate AIs", "Credits", "Exit"]
        self.evaluate_content = ["Random", "Dumb AI", "Weak AI", "Strong AI", "GODLIKE AI", "Back to Main Menu"]
        self.play_against_ai_content = ["First", "Second", "Back to Main Menu"]
        self.counters = {"Player 1 Wins": 0, "Player 2 Wins": 0, "Draws": 0}
        self.PLAYER_1 = None
        self.PLAYER_2 = None
        self.N_GAMES = 0

    def main_menu(self):
        """Main menu of the game"""
        menu = Menu(*self.main_content, rule_title="Welcome to Quixo!", panel_title="MAIN MENU")
        # Handling menu selection
        selection = menu.ask()
        # Play against AI
        if selection == self.main_content[0]:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.play_against_AI()
        # Evaluate AIs
        elif selection == self.main_content[1]:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.PLAYER_1 = self.select_player("first")
            if self.PLAYER_1 is None:
                return self.main_menu()
            self.PLAYER_2 = self.select_player("second")
            if self.PLAYER_2 is None:
                return self.main_menu()
            self.N_GAMES = self.select_n_games()
            self.reset_counters()
            self.evaluation_recap()
            for x in tqdm(range(self.N_GAMES), desc="Evaluating AIs", unit="game"):
                game = Game()
                winner = game.play(self.PLAYER_1, self.PLAYER_2, False) # with interactive=False
                if winner == 0:
                    self.counters["Player 1 Wins"] += 1
                elif winner == 1:
                    self.counters["Player 2 Wins"] += 1
                else: #elif winner == 10
                    self.counters["Draws"] += 1
            self.print_counters()
        # Credits
        elif selection == self.main_content[2]:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.credits()
        # Exit
        elif selection == self.main_content[3]:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.print("Goodbye!", style="bold red")
            sys.exit()
        # Just in case
        else:
            sys.exit()

    def select_player(self, turn: str):
        """Select the player strategy for the play against AI section"""
        menu = Menu(*self.evaluate_content,
                    panel_title="Choose first player strategy:" if turn == "first" else "Choose second player strategy:",
                    rule_title=self.main_content[1])
        # Handling menu selection
        selection = menu.ask()
        # Random
        if selection == self.evaluate_content[0]:
            return RandomPlayer()
        # Dumb AI
        elif selection == self.evaluate_content[1]:
            return AIPlayer(max_depth=1)
        # Weak AI
        elif selection == self.evaluate_content[2]:
            return AIPlayer(max_depth=2)
        # Strong AI
        elif selection == self.evaluate_content[3]:
            return AIPlayer(max_depth=3)
        # GODLIKE AI
        elif selection == self.evaluate_content[4]:
            return AIPlayer(max_depth=4)
        # Back to Main Menu
        elif selection == self.evaluate_content[5]:
            return None
        # Just in case
        else:
            return None

    def select_n_games(self):
        """Select the number of games to evaluate the AIs"""
        while True:
            try:
                n_games = int(Prompt.ask("How many games do you want to evaluate?"))
                if n_games <= 0:
                    raise ValueError
                return n_games
            except ValueError:
                self.console.print("Please enter a valid number greater than 0!", style="bold red")

    def evaluation_recap(self):
        """Print the recap of the evaluation section"""
        os.system('cls' if os.name == 'nt' else 'clear')
        # All of this only for printing text centered with some italics? yes. Is it worth it? maybe not.
        panel_content = Text(justify="center")
        panel_content.append("Number of games: ")
        panel_content.append(f"{self.N_GAMES}\n", style="italic")
        panel_content.append("Player 1: ")
        panel_content.append(f"{self.PLAYER_1.name}", style="italic")
        panel_content.append("  vs  Player 2: ")
        panel_content.append(f"{self.PLAYER_2.name}", style="italic")
        panel = Align.center(Panel(panel_content, title="Evaluation Recap", style="bold green"))
        self.console.print(panel)
        self.console.print("")

    def credits(self):
        """Credits section"""
        os.system('cls' if os.name == 'nt' else 'clear')
        panel_content = "Developed by Luca Barbato.\nLABs have been made in collaboration with [italic]Lorenzo Greco[/italic] and [italic]Giuseppe Roberto Allegra[/italic].\nQUIXO has not been developed together but strategy has been discussed."
        panel = Align.center(Panel(panel_content, title="Credits", style="bold green"))
        self.console.print(panel)

    def reset_counters(self):
        self.counters = {"Player 1 Wins": 0, "Player 2 Wins": 0, "Draws": 0}

    def print_counters(self):
        """Print the counters for the evaluation section"""
        table = Table(title="Game Results", title_style="green")
        table.add_column("Player", justify="center", style="white")
        table.add_column("Wins", justify="center", style="bold green")
        table.add_column("Losses", justify="center", style="red")
        table.add_column("Draws", justify="center", style="yellow")
        table.add_column("Total Games", justify="center", style="bright_blue")
        table.add_column("Win Percentage", justify="center", style="bold green")
        table.add_row(
            self.PLAYER_1.name,
            str(self.counters['Player 1 Wins']),
            str(self.N_GAMES - self.counters['Player 1 Wins'] - self.counters['Draws']),
            str(self.counters['Draws']),
            str(self.N_GAMES),
            f"{self.counters['Player 1 Wins']/self.N_GAMES*100:.1f}%",
        )
        table.add_row(
            self.PLAYER_2.name,
            str(self.counters['Player 2 Wins']),
            str(self.N_GAMES - self.counters['Player 2 Wins'] - self.counters['Draws']),
            str(self.counters['Draws']),
            str(self.N_GAMES),
            f"{self.counters['Player 2 Wins']/self.N_GAMES*100:.1f}%",
        )
        self.console.print("")
        self.console.print(Align.center(table))
        self.console.print("")

    def play_against_AI(self):
        """Play against AI section"""
        # Choose if you want to play as first or second
        human_turn = self.choose_human_turn()
        if human_turn is None:
            return self.main_menu()
        # First
        elif human_turn == self.play_against_ai_content[0]:
            self.PLAYER_1 = HumanPlayer()
            self.PLAYER_2 = self.select_player("second")
            if self.PLAYER_2 is None:
                return self.main_menu()
        # Second
        else:
            self.PLAYER_1 = self.select_player("first")
            if self.PLAYER_1 is None:
                return self.main_menu()
            self.PLAYER_2 = HumanPlayer()
        self.display_message_with_timer(4)
        game = Game()
        game.play(self.PLAYER_1, self.PLAYER_2, True) # with interactive=True

    def choose_human_turn(self):
        """Choose if you want to play as first or second in the play against AI section"""
        menu = Menu(*self.play_against_ai_content,
                    panel_title="Do you want to play as First or Second?",
                    rule_title=self.main_content[0])
        # Handling menu selection
        selection = menu.ask()
        # First
        if selection == self.play_against_ai_content[0]:
            return self.play_against_ai_content[0]
        # Second
        elif selection == self.play_against_ai_content[1]:
            return self.play_against_ai_content[1]
        # Back to Main Menu
        elif selection == self.play_against_ai_content[2]:
            return None
        # just in case
        else:
            return None

    def display_message_with_timer(self, countdown_seconds):
        """Display a message with a countdown timer before the game starts"""
        console = Console()
        console.clear()
        with console.status("SPINNER") as status:
            while countdown_seconds > 0:
                status.update(f"[bold green]Please enlarge the screen for a better use experience.\n\nGET READY\n\nStarting in: {countdown_seconds} seconds...")
                time.sleep(1)
                countdown_seconds -= 1
        console.clear()