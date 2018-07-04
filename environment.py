import sys
import numpy as np


class Environment:
	
	"""Environment class takes filename in constructor
	   which is the path to the maze file.
	   
	   It has a method "step" that simulates a step 
	   based on action and outputs the next state, the
	   reward and is_terminal.
	   
	   It has a state reset that does not take any arguments
	   and sets the agent back to the initial state"""
	
	def __init__(self, filename_maze, filename_a, file_op):
		
		#Input maze -
		self.filename_maze = filename_maze
		#File containing sequence of actions - 
		self.filename_a = filename_a
		#File to write output policy to -
		self.opfile = file_op

		self.op = open(file_op, 'w')
		
		"""The flag 'is_terminal' informs the agent whether it has reached
		goal state or not. 1 means that the agent has moved into the goal state."""
		self.is_terminal = 0
		
		self.actions = np.genfromtxt(filename_a, dtype = int,delimiter = ' ')		


		with open(filename_maze,'r') as f:
			self.l = f.read()
			self.maze = self.l.splitlines()
			
		
		self.a = np.empty([len(self.maze),len(self.maze[0])], dtype = object)

		for i,word in enumerate(self.maze):
			for j,char in enumerate(word):
				self.a[i][j] = char


		
		
		self.state = [len(self.maze)-1, 0]


	"""
	step(action) returns the next state of the agent once it has taken an 'action'.
	It returns the same state if the action taken by the agent leads it to an obstacle
	or outside the maze boundaries.
	"""
	def step(self, action):
		
		if action == 0:
			if self.state[1]-1 >=0:
				y_c = self.state[1]-1
				if self.a[self.state[0]][y_c] == '*':
					self.state = [self.state[0],self.state[1]]
				else:
					self.state = [self.state[0],y_c]

				
		
		elif action == 1:
			if self.state[0]-1 >=0:
				x_c = self.state[0]-1
				if self.a[x_c][self.state[1]] == '*':
					self.state = [self.state[0],self.state[1]]
				else:
					self.state = [x_c,self.state[1]]



		elif action == 2:
			sh = np.shape(self.a)
			if self.state[1]+1 >=0 and self.state[1]+1 < sh[1]:
				y_c = self.state[1]+1
				if self.a[self.state[0]][y_c] == '*':
					self.state = [self.state[0],self.state[1]]
				else:
					self.state = [self.state[0],y_c]

		
		elif action == 3:
			if self.state[0]+1 >=0  and self.state[0]+1 < len(self.maze):
				x_c = self.state[0]+1
				if self.a[x_c][self.state[1]] == '*':
					self.state = [self.state[0],self.state[1]]
				else:
					self.state = [x_c,self.state[1]]

		

		if self.a[self.state[0]][self.state[1]] == 'G':
			self.is_terminal = 1

		
		#Writing to the output file - 
		self.op.write(str(self.state[0]))
		self.op.write(" ")
		self.op.write(str(self.state[1]))
		self.op.write(" ")
		self.op.write('-1')
		self.op.write(" ")
		self.op.write(str(self.is_terminal))
		self.op.write("\n")



	"""Resets the agent's state to the Initial State"""
	def reset(self):

		self.state = [len(self.maze)-1, 0]





def main():

	#maze ip -
	filename = sys.argv[1]

	#output file - 2
	opfile = sys.argv[2]

	#action file - 3
	actionfile = sys.argv[3]

	
	#Initialise an object of class Environment
	ev1 = Environment(filename, actionfile, opfile)

	
	for action in ev1.actions:
		
		ev1.step(action)

	ev1.reset()



if __name__ == "__main__":
	main()
