# EvoDev

Evolutionary computing draws inspiration from the natural process of evolution to solve complex optimization problems in various domains. Genetic algorithms (GAs) are a subfeild of evolutionary computing, where a population of candidate solutions to a given problem are evolved under the repeated process of selection, mutation, and crossover. Over many generations, GAs are especially useful for finding global optima in complex fitness landscapes. This Jupyter notebook transforms the development of GAs into an intuitive, interactive, process, by enabling the user to configure and run a GA from a predefined library of selection, mutation, and crossover techniques, visualize the results in real time, and update certain parameters to acheive better results.

# Acknowledgments

This project was completed in fulfillment of the course CISC 499 - Advanced Undergraduate Project at the Queen's School of Computing. Thank you to our supervisor, Professor Ting Hu for her supervision on this project.

# Getting Started

## Google Colab

## Jupyter Lab/Notebook

### MacOS

### Windows

# Library

In this section, we discuss the library of predefined problem instances, and custom problem types, solution encodings, as well as selection, crossover, and mutation techniques implimented in this project.

## Predefined problem instances

### Traveling Salesperson Problem (TSP)

Given n points and their (x, y) locations, the goal of the TSP is to find the shortest route, starting and ending at the first point, and visiting each other point exactly once. The TSP uses a permutation encoding to represent the order in which the points are visited. In our predefedined TSP instance, we include a map of the [29 cities in the Western Sahara](http://www.math.uwaterloo.ca/tsp/world/wipoints.html).

### Knapsack

Given n items and their weights and values, the goal of this modified version of the knapsack problem is to select the items that maximize the value of the selection, while simultaneously maximizing the weights. This implementation of the knapsack problem uses a binary encoding, where a 1 in the ith position means that the ith item was selected, where a 0 represents that it was not.

### n-Queens

Given an (n x n) chessboard, the goal of the n-queens problem is to place n-queens in such a way that minimizes the checks on the board. Recall that queens can move horizontally, vertically, and diagnolly. The n-queens problem uses the permutation encoding, where a value in the ith position indicates the row in which the ith queen is placed.

### Sudoku

Given an (n x n) grid, the goal of sudoku is to arrange values in the range (0, n - 1) in each row and column in such a way that minimizes the number of times each value occurs in the same row or column. This implementation of the sudoku problem uses a (1 x n x n) permutation to encode solutions, where the result of (value % 10) indicates the value placed in that position.

## Problem types

### Single-objective

Single-obective problems are defined by a single goal, to minimize or maximize the sole fitness value of solutions. Selection techniques are dependent on problem type, and for single-objective problems, we implement the following selection techniques:

#### Rank-based

Solutions are ranked and the fittest are selected to produce offspring and/or survive into the next generation.

#### Tournament

Solutions are randomly selected to compete in a tournament, and compete 1-on-1. The winner of each tournament proceeds to crossover or into the next generation.

#### Note

Rank-based selection automatically selects the fittest solutions, while in tournament selection, low fitness solutions can win if the draw is especially weak. By increasing the tournament size, it becomes more likely that high fitness solutions win each tournament.

### Multi-Objective

Multi-objective problems are defined by multiple goals, to minimize or maximize mutliple fitness values. For this problem type, we implement the following technique:

#### NSGA-II

Solutions are divided into fronts based on the dominance relation, where a solution is said to dominate another individual if all of its fitness values are better in terms of the problem objectives. The first front (sometimes referred to as the Pareto front) is defined as the set of solutions that are not dominated by any other individual, the second front the set that are not dominated by any other solution not in the first front, and so on.

## Encodings

### Binary

The binary encoding is defined as a binary string of a given length. The binary string is used in the Knapsack problem, where a 0 in the ith position means that the ith object is not selected. A 1 in the ith position, however, means that the ith object is selected.

### Permutation

The permutation encoding is defined in this implementation as an ordering of integers between a minimum and maximum value. A valid permutation for the range 0 to 3 (inclusive), for example, would be the list \[3, 2, 1, 0\]. The permutation encoding is used in the TSP instance, where the permutation represents the order at which the nodes are visited in the circuit.

### Integer and Real-valued

The integer and real-valued representations are defined as a random sample (usually uniform) of a given length from a given distribution of either integer or floating point values. Although this encoding is not used in any of the predefined problem instances, it can be used in instances where you would like to select a non-binary amount of something.

## Techniques

The remaining crossover and mutation techniques are dependent on the encoding of solutions.

### Binary

#### Crossover

##### n-point

n crossover points are randomly generated, and the resulting offspring inherits the sequence of alleles between each crossover point from the first and second parent alternatively.

##### Uniform

For each allele in the resulting offspring, the value is inherited from either parent with equal probability.

#### Mutation

##### Bit-flip

For each allele in the offspring, the bit is flipped with probability specified by the bit-wise mutation rate.

### Permutation

#### Crossover

##### Order

Two crossover points are randomly generated, and in the resulting offspring, the alleles between them are inherited from the first parent. The remaining alleles are inherited from the second parent, treating the sequence as toroidal.

##### Partially-Mapped (PMX)

Two crossover points are randomly generated, and in the resulting offspring, the alleles between them are inherited from the first parent. In the same region, for each value (i) in the second parent that has not already been inherited, look in the corresponding index in the first parent, and place this value (j) in the index where j occurs in the second parent. In the remaining indices, the offspring inherits the value from the second parent.

#### Mutation

##### Swap

For each allele in the offspring, the value is swapped with a value at another allele with probability specified by the bit-wise mutation rate.

##### Scramble

Two crossover points are randomly generated, and the sequence of values between them are randomly shuffled.

### Integer

#### Crossover

##### N-point

(see binary crossover)

##### Uniform

(see binary crossover)

#### Mutation

##### Random-resetting

For each allele in the offspring, the value is randomly replaced with probability specified by the value-wise mutation rate.

##### Creep

For each allele in the offspring, the value is incremented or decremented by a value drawn from a Gaussian distribution. This occurs with probability specified by the value-wise mutation rate, and the standard deviation of the distribution is specified by the parameter theta.

### Real-valued

#### Crossover

##### Whole-arithmetic

The resulting offspring is the arithmetic average of the two parents, with the first parent's values weighted by a parameter alpha, and the second's weighted by 1 less the parameter alpha.

##### Simple-arithmetic

A single crossover point is randomly generated. The alleles before this point are inherited from the first parent, and whole-arithmetic crossover is performed on the remaining region.

#### Mutation

##### Uniform

(see integer crossover - random-resetting)

##### Non-uniform

(see integer crossover - creep)

## Visualizations

We provide two predefined visualizations in order to inform the user on the progress of a run.

### Fitness distribution convergence

The first visualzation indicates the convergence of the population fitness distribution, where the top line of each color indicates the maximum fitness value in the population, the bottom line, the minimum, and the middle line the average. This visualization is scalable to 3 objectives, and the width of the shaded area corresponds to the width of the fitness distribution, and is often a good indicator of population diversity.

### Population heatmap

The second visualization leverages a heatmap to show the values in each allele for each individual in the population. Each row represents the encoding for an individual solution, and each column represents a single allele. Thus, a heatmap that looks like television static means that there is lots of diversity in the population of solutions. On the other hand, a heatmap that contains uniform vertical columns of the same color indicates that the population has converged to a single solution. This is usually a good time to stop the algorithm.

# FAQ

##### Can I change any parameters I defined in the setup applet once I get to the main applet?

If you would like to reconfigure the problem type or representation, or select a new predefined problem instance, you must re-run the setup applet cell, select your desired configuration or problem instance, and re-run the main applet.

# References

[Introduction to Evolutionary Computing](https://link.springer.com/book/10.1007/978-3-662-44874-8)
