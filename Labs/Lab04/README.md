# Lab 04
⚠️ We assumed that X always moves first. This information can be useful as a key for interpretation and understanding of some experiments.

- [Objectives](#objectives)
- [Training Phase](#training-phase-for-both-x-and-o)
- [AI using X](#ai-using-x-first-to-move)
- [AI using O](#ai-using-o-second-to-move)
- [AI vs. AI](#ai-using-x-against-ai-using-o)
- [Challenge the AIs](#do-you-want-to-challenge-the-ais)

## Objectives
Starting from the professor's strategy we tried to improve it, testing how artificial intelligence behaved in different scenarios.

## Training Phase (for both X and O)
Two different dictionaries were used, one for AI using x and the other one for the AI using O, as stated here:

```python
# Creation of 2 dictionaries for storing X AI and O AI players training
# Accessible by value_dictionary["x"] and value_dictionary["o"]
value_dictionary = {"x": defaultdict(float), "o": defaultdict(float)}
```

During the training phase our AI plays against an opponent using a random strategy: it means the opponent will choose a random move from the _available_ ones.

We made AI train for 1_000_000 games to be able to have an optimal dictionary capable of suggesting the best move in every situation, covering all possible scenarios that could happen. For a simple game like tic-tac-toe we can assume to have visited all possible states multiple times.

After a huge amount of tests conducted during the development we found that the best results were achived using _epsilon_ = 0.003 and as _Reward Policy_:

| Player  | Win  | Lose | Draw |
|---------|------|------|------|
|  **X**  |  +1  |  -1  |   0  |
|  **O**  |  +3  |  -6  |  +2  |

## AI using X (first to move)
After implementing the training phase, we wondered how good this player actually was.  
On average, when tested in a series of 10_000 games against a player making random moves, performances were excellent:

- Wins: 9908 (99.08%)
- Loses: 0 (0.00%)
- Draws: 92 (0.92%)

But winning doesn't necessarily mean making the best moves.
So, to be sure that it didn't make any mistakes and always chooses the best move, we tested move by move the various states of a lot of games.
The tests performed, showed that every time the AI had the opportunity to win, it closed the game, confirming our hypothesis that it had now reached perfection.

While it might appear obvious, it's not always the case. With a low number of games during training, there's the possibility that not all potential move combinations were explored, leading to the selection of non-optimal moves while still achieving victory. We encountered this issue with a training phase of 100_000 games, prompting us to increase the number to 1_000_000 for a more comprehensive exploration.

## AI using O (second to move)
After achieving this result, we wondered how the AI would behave if it had to use O and move second.

Initially, we adapted the algorithm that selects intelligent moves to find the best moves for O.
Instead of choosing the move that led us to the best state for X, we selected moves that led us to the worst state, therefore more advantageous for O.
Although it played quite decently, it tied and lost a bit too much. Starting second, when X plays well, if you are skilled, you can manage to draw. Therefore, we were not concerned about the number of draws, but there were too many losses for it to be considered a good AI.

In addition, the training phase (for X) stored and updated the state value based on how advantageous it was for X, also considering the difference between the final result of the game and the value of that state up to that point.
Therefore, it didn't fit perfectly to our case.
So we decided to create a training program exclusively for O, with a dictionary that learns the best moves in every situation and that could, at least, draw even against the best opponents.

Initially the training phase (for O) was the same as for X.
The results were not very satisfying. We managed to reduce the losses a bit, but the AI was still far from being a very good player.

The major weakness come out when we tried to make it play against AI using X with optimal moves (the one we just trained before!).
10_000 test games were conducted and they ended all with a lose.
This experiment highlighted how O did not know the strategy to draw against a perfect X. This is because, in the 1,000,000 randomly played training games, the times the computer randomly plays the best moves for X and O's best moves to draw are too few, or not highly valued enough, for O to learn and memorize the optimal defensive strategy in its dictionary.

That's why we decided to change its Reward Policy during the training phase. As stated above, we did a huge amount of tests and we chose the parameters that gave us the best statistics.

As a result, on average, when tested in a series of 10_000 games against a player making random moves, performances were pretty good:

- Wins: 8779 (87.79%)
- Loses: 42 (0.42%)
- Draws: 1179 (11.79%)

We believe that by changing the values assigned by the reward function, it is possible to achieve a perfect gameplay.

## AI using X against AI using O
While we already knew AI using X was making best moves, fights against the two AIs confirmed that the Reward Policy used for AI playing with O during the training phase is very effective.
When AIs were tested in a series of 10_000 games against each other the outcome was as follows:

- AI usign X Wins: 0 (0.00%)
- AI usign O Wins: 0 (0.00%)
- Draws: 10000 (100.00%)

It's important to note that this result doesn't have a random component; it is consistent and seems to remains the same with each execution.

## Do you want to challenge the AIs?
After finishing our experiments, we thought it could be fun having the possibility to challenge the AIs we created.

They are unbeatable...

The few combinations that O fails to block are so rare and suboptimal that any human player would never play them, effectively being unable to beat the AIs (both with X and O) ever!