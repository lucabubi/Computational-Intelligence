# Lab 01

During this laboratory, we conducted experiments on heuristic functions h.

We initially considered a solution based on remaining coverage, which was calculated as the difference between the total number of elements in the set and the number of elements already covered. 

In an attempt to optimize it, we arrived at the same conclusion as heuristic function `h1`, already present in Professor Squillero's repository.

Since heuristic function `h2`, which optimized `h1`, was already present in the professor's repository, we attempted to further optimize `h1` by questioning whether rounding using `ceil` was causing the loss of useful information for PriorityQueue ordering. 

We, therefore, sought information on the implementation of the PriorityQueue and discovered that the priority doesn't necessarily have to be an integer. 

Our hypothesis was that for large values of _PROBLEM_SIZE_ and _NUM_SETS_, rounding was actually making the algorithm worse, as sets with different coverages were being rounded to the same integer and therefore not optimally sorted. However, after running various tests, we realized that the `ceil` operation is indeed functional to the algorithm, and our hypothesis was incorrect because a fractional value wouldn't be suitable as a cost estimate because a fraction of a set in a solution is not valid, since the `ceil` operation represents the minimum number of sets required to cover the missing elements, ensuring that the estimate is optimistic.