# Lab 02

## Genome & Evolutionary Strategy
Regarding the genome, not wanting to rely on the information that the best moves are those with NimSum != 0 (because within the context of evolutionary algorithms, the optimal algorithm is theoretically unknown), we have conceived a genome consisting of three parameters.

The first parameter 'preference' indicates the probability of following or not following the strategy proposed by the genome.  
The second parameter 'use_lower_half' indicates the genome's strategy. We identify the min and max of NimSum for the moves and calculate the average value. Therefore, based on this parameter, we consider as possible moves either the lower or upper half of this set.  
The third parameter represents the 'fitness,' i.e., the proficiency of the individual in the game.

It is certainly not the optimal strategy, but, on the other hand, the optimal strategy already exists. Thus, we wanted to create a strategy that is random but still logical.

## Parent Selection
The parent selection, as with many evolutionary algorithms, occurs through a tournament where the winner is chosen based on the 'fitness' parameter of their genome. The player is rewarded with one point for each won game.

## Crossover
The two parents have a weighted probability in terms of their fitness to transmit or not transmit a specific genomic parameter to their child.

## Mutation
Mutation occurs based on a mutation rate, typically very low. An attempt is made on each parameter of the genome independently. If the mutation occurs, the new parameter is always chosen randomly.

## Simulation
Finally, the simulation is executed. Players are trained against the optimal strategy, and the parameters are configurable.

At the end of the simulation, the best player from the last generation is selected. This best player has the honor of challenging, in a round of 1000 games, other strategies, including a rematch against the optimal strategy.

## Final Considerations
Our strategy is far from being optimal, and being pseudo-random, it has a limited range of improvement.

Conducting numerous tests and varying simulation parameters, both with small and large numbers, we observed that it always starts with a win rate in the first generation of about 35%, evolving to a maximum of around 42%. There is an improvement. It improves very quickly, especially in the first five generations, reaching its maximum value and then stabilizing around that value.

Thinking that it might be a local optimum, we tried increasing the mutation rate to prevent it from settling on a percentage. Unfortunately, it didn't help, rather, increasing the mutation rate emphasizes the random component of the strategy, leading to a loss of evolutionary progress made up to that point.

In the final matches, the elected best player has a positive win rate against Gabriele's strategy, while winning about 46% of the time against the pure random strategy. Against the optimal strategy, the win rate always hovers around 43%.

We attach an example of a simulation where you can see the slight improvement.

### Simulation:
Generation 1:
They won 1801 games in 5000 games  
The percentage of won games of this generation is: 36.02% 

Generation 2:  
They won 1901 games in 5000 games  
The percentage of won games of this generation is: 38.02%  

Generation 3:  
They won 2014 games in 5000 games  
The percentage of won games of this generation is: 40.28%  

Generation 4:  
They won 2044 games in 5000 games  
The percentage of won games of this generation is: 40.88%  

Generation 5:  
They won 1930 games in 5000 games  
The percentage of won games of this generation is: 38.6%  

Generation 6:  
They won 1991 games in 5000 games  
The percentage of won games of this generation is: 39.82%  

Generation 7:  
They won 2032 games in 5000 games  
The percentage of won games of this generation is: 40.64% 

Generation 8:  
They won 2048 games in 5000 games  
The percentage of won games of this generation is: 40.96%  

Generation 9:  
They won 2035 games in 5000 games  
The percentage of won games of this generation is: 40.70%  

Generation 10:  
They won 2056 games in 5000 games  
The percentage of won games of this generation is: 41.12%  

Best Player vs Gabriele Strategy:  
They won 514 games in 1000 games  
The percentage of won games is: 51.4%  

Best Player vs Pure Random Strategy:  
They won 469 games in 1000 games  
The percentage of won games is: 46.9%  

Best Player vs Optimal: The Rematch!  
They won 406 games in 1000 games  
The percentage of won games is: 40.6%

As you can see, it quickly surpassed the 40% winning threshold, only to experience a relapse. Unfortunately, in this simulation, it did not exceed a 41% win rate. However, the best player performed very well against Gabriele's strategy and the random strategy, achieving 'only' a 40.6% win rate in the rematch against the optimal strategy. During some tests, we recorded values even higher than 45%. What a pity, maybe it was tired from all the previous games...




