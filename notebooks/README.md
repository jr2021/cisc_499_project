# [FIXME]

Evolutionary computing draws inspiration from the natural process of evolution to solve complex optimization problems in various domains. Genetic algorithms (GAs) are a subfeild of evolutionary computing, where a population of candidate solutions to a given problem are evolved under the repeated process of selection, mutation, and crossover. Over many generations, GAs are especially useful for finding global optima in complex fitness landscapes. This Jupyter notebook transforms the development of GAs into an intuitive, interactive, process, by enabling the user to configure and run a GA from a predefined library of selection, mutation, and crossover techniques, visualize the results in real time, and update certain parameters to acheive better results.

# Getting Started

## Google Colab

## Jupyter Lab/Notebook

### MacOS

### Windows

# Library

In this section, we discuss the library of predefined problem instances, and custom problem types, solution encodings, as well as selection, crossover, and mutation techniques implimented in this project.

## Predefined problem instances

### Traveling Salesperson Problem (TSP)

### Knapsack

### 64-Queens

### 10x10 Sudoku

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

#### Mutation

### Permutation

#### Crossover

#### Mutation

### Integer

#### Crossover

#### Mutation

### Real-valued

#### Crossover

#### Mutation

## Visualizations

# FAQ

##### Can I change any parameters I defined in the setup applet once I get to the main applet?
If you would like to reconfigure the problem type or representation, or select a new predefined problem instance, you must re-run the setup applet cell, select your desired configuration or problem instance, and re-run the main applet.



