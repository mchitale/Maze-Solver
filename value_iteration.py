import sys
import numpy as np
import time


class Environment:

#*****************************************************************#
	
	"""Environment class takes filename in constructor
	   which is the path to the maze file.
	   
	   It has a method "step" that simulates a step 
	   based on action and outputs the next state, the
	   reward and is_terminal.
	   
	   It has a state reset that does not take any arguments
	   and sets the agent back to the initial state"""

#*****************************************************************#

	
	def __init__(self, filename_maze, filename_a = None, file_op = None):
		

		self.filename_maze = filename_maze
		self.filename_a = filename_a
		self.opfile = file_op
		self.is_terminal = 0
		

		if self.opfile != None:
			self.op = open(file_op, 'w')
		
		
		if self.filename_a != None:
			self.actions = np.genfromtxt(filename_a, dtype = int,delimiter = ' ')		


		with open(filename_maze,'r') as f:
			self.l = f.read()
			self.maze = self.l.splitlines()
			
		
		self.a = np.empty([len(self.maze),len(self.maze[0])], dtype = object)

		for i,word in enumerate(self.maze):
			for j,char in enumerate(word):
				self.a[i][j] = char


		
		
		self.state = [len(self.maze)-1, 0]
		self.num_states = np.shape(self.a)



#*****************************************************************#


	def step(self, action):
		
		state = self.state
		#Action - West : <--
		if action == 0:
			if self.state[1]-1 >=0:
				y_c = self.state[1]-1
				if self.a[self.state[0]][y_c] == '*':
					state = [self.state[0],self.state[1]]
				else:
					state = [self.state[0],y_c]

				
		#Action - North : ^
		elif action == 1:
			if self.state[0]-1 >=0:
				x_c = self.state[0]-1
				if self.a[x_c][self.state[1]] == '*':
					state = [self.state[0],self.state[1]]
				else:
					state = [x_c,self.state[1]]


		#Action - East : -->
		elif action == 2:
			sh = np.shape(self.a)
			if self.state[1]+1 >=0 and self.state[1]+1 < sh[1]:
				y_c = self.state[1]+1
				if self.a[self.state[0]][y_c] == '*':
					state = [self.state[0],self.state[1]]
				else:
					state = [self.state[0],y_c]

		
		#Action - South : v
		elif action == 3:
			if self.state[0]+1 >=0  and self.state[0]+1 < len(self.maze):
				x_c = self.state[0]+1
				if self.a[x_c][self.state[1]] == '*':
					state = [self.state[0],self.state[1]]
				else:
					state = [x_c,self.state[1]]

		

		#If the state reached is terminal, set is_terminal to 1.
		if self.a[self.state[0]][self.state[1]] == 'G':
			self.is_terminal = 1

		return state, self.is_terminal

#*****************************************************************#

		
	def reset(self):

		#Resets the state to the Initial State.
		
		self.state = [len(self.maze)-1, 0]


#*****************************************************************#

def largest(Q):

	larg = Q[0]
	index = 0

	for i in xrange(0, len(Q)):
		if Q[i] > larg:
			larg = Q[i]
			index = i

	return larg,index

#*****************************************************************#

def main():

	maze_ip = str(sys.argv[1])
	value_op = str(sys.argv[2])
	qv_op = str(sys.argv[3])
	policy_op = str(sys.argv[4])
	num_epoch = int(sys.argv[5])
	gamma = float(sys.argv[6])

	qv = open(qv_op, 'w')
	vl = open(value_op, 'w')
	pol = open(policy_op,'w')

	#Creates an object of type env, and initialises
	#agent to Initial State


	env = Environment(maze_ip)

	actions = [0, 1, 2, 3]

	V = np.zeros([env.num_states[0],env.num_states[1]])
	temp_V = np.zeros([env.num_states[0],env.num_states[1]])
	V_actions = np.zeros([env.num_states[0],env.num_states[1]])
	shv = np.shape(V)
	

	for e in xrange(0, num_epoch+1):

		print "iteration = ", e
		
		for i in xrange(0, shv[0]):
			for j in xrange(0, shv[1]):
				
				Q = []

				env.state = [i,j]
				
				if env.a[env.state[0]][env.state[1]]=='G':
					temp_V[i][j] = 0
					if e == num_epoch:
						for m in xrange(0,4):
							qv.write(str(i))
							qv.write(" ")
							qv.write(str(j))
							qv.write(" ")
							qv.write(str(m))
							qv.write(" ")
							qv.write(str(0.0)) 
							qv.write("\n")

					pass
				
				elif env.a[env.state[0]][env.state[1]]=='*':
					temp_V[i][j] = 0
					pass
					
				
				else:
					for action in actions:
						
						st, is_terminal = env.step(action)

						val = -1 + (gamma * V[st[0]][st[1]])
						Q.append(val)

						if e == num_epoch:
							qv.write(str(i))
							qv.write(" ")
							qv.write(str(j))
							qv.write(" ")
							qv.write(str(action))
							qv.write(" ")
							qv.write(str(val))
							qv.write("\n")


				
					temp_V[i][j] = max(Q)
					V_actions[i][j] = Q.index(max(Q))

		if e != num_epoch:
			V = 1*temp_V



	print V


	for i in xrange(0, shv[0]):
		for j in xrange(0, shv[1]):

			env.state = [i,j]
				
			if env.a[env.state[0]][env.state[1]]=='G':
				vl.write(str(i))
				vl.write(" ")
				vl.write(str(j))
				vl.write(" ")
				pol.write(str(i))
				pol.write(" ")
				pol.write(str(j))
				pol.write(" ")
				pol.write("0.0")
				pol.write("\n")
				vl.write(str(0.0))
				vl.write("\n")

			elif env.a[env.state[0]][env.state[1]] != '*':
				vl.write(str(i))
				vl.write(" ")
				vl.write(str(j))
				vl.write(" ")
				vl.write(str(V[i][j]))
				vl.write("\n")
				pol.write(str(i))
				pol.write(" ")
				pol.write(str(j))
				pol.write(" ")
				pol.write(str(V_actions[i][j]))
				pol.write("\n")



#*****************************************************************#


if __name__ == "__main__":
	main()


