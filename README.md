# Maze-Solver
A Reinforcement Learning Algorithm that finds the shortest path through rectangular mazes.
The mazes are in the form of a text file that have an initial state represented by 'S', and a goal state represented by 'G'.
It consists of three files:
1. environment.py - This file creates the environment class and the corresponding methods that take as input an action by the agent, and return the updated state of the environment.
2. value_iteration.py - This file attempts to find the shortest path through the maze using the value iteration algorithm.
3. q_learning.py - This file attempts to find the shortest path through the maze using the Q-learning algorithm.

# environment.py
This file creates a class and has the methods 'step' and 'reset'. 
The 'step' method takes an action[up,down,left,right] as input and gives the co-ordinates of the next location of the agent as output. If the input action leads the agent to an obstacle, it keeps the agent in the same state. Once the agent has reached the goal state, the environment class informs the agent of this by setting the flag "is_terminal".
The 'reset' method just resets the agent to its initial state.

