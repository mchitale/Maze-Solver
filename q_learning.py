import sys
import time
import numpy as np

start_time = time.time()

class Environment:
	
	"""Environment class takes filename in constructor
	   which is the path to the maze file.
	   
	   It has a method "step" that simulates a step 
	   based on action and outputs the next state, the
	   reward and is_terminal.
	   
	   It has a state reset that does not take any arguments
	   and sets the agent back to the initial state"""
	
	def __init__(self, filename_maze, filename_a = None, file_op = None):
		

		self.filename_maze = filename_maze
		self.filename_a = filename_a
		self.opfile = file_op

		if self.opfile != None:
			self.op = open(file_op, 'w')
		
		self.is_terminal = 0
		
		if self.filename_a != None:
			self.actions = np.genfromtxt(filename_a, dtype = int,delimiter = ' ')		


		with open(filename_maze,'r') as f:
			self.l = f.read()
			self.maze = self.l.splitlines()
			
		
		self.a = np.empty([len(self.maze),len(self.maze[0])], dtype = object)

		self.shape_of_A = np.shape(self.a)

		for i,word in enumerate(self.maze):
			for j,char in enumerate(word):
				self.a[i][j] = char


		
		
		self.state = [len(self.maze)-1, 0]



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


		return self.state, self.is_terminal



	def reset(self):

		#Resets the state to the Initial State.

		self.state = [len(self.maze)-1, 0]
		self.is_terminal = 0



def main():
	
	maze_ip = str(sys.argv[1])
	"""val_op = str(sys.argv[2])
	qv_file = str(sys.argv[3])
	policy_op = str(sys.argv[4])
	num_ep = int(sys.argv[5])
	max_ep_len = int(sys.argv[6])
	alpha = float(sys.argv[7])
	gamma = float(sys.argv[8])
	epsilon = float(sys.argv[9])"""


	alpha = 0.1
	gamma = 0.9
	epsilon = 0.8

	"""qv = open(qv_file, 'w')
	pol_c = open(policy_op, 'w')
	valf = open(val_op, 'w')"""

	
	env = Environment(maze_ip)
	actions = [0,1,2,3]

	Q = np.zeros([env.shape_of_A[0],env.shape_of_A[1], len(actions)])
	V =  np.zeros([env.shape_of_A[0],env.shape_of_A[1]])

	stc = np.zeros([2000,1])

	for i in xrange(0,2000):

		env.reset()		# Sets state to 'S'
		count = 0
		
		for j in xrange(0, 100):
			count += 1
			orig_state = env.state 

			action = np.argmax(Q[orig_state[0]][orig_state[1]])


			r = np.random.uniform([0.0,1.0])


			if r[0] <= (1 - epsilon):
				action = action

			else:

				m = np.random.uniform([0.0,1.0])
				if m[0] <= 0.25:
					action = 0
				
				elif m[0] <=0.5:
					action = 1

				elif m[0] <=0.75:
					action = 2

				else:
					action = 3


			temp_state, is_terminal = env.step(action)

			Q[orig_state[0]][orig_state[1]][action] = (((1 - alpha)*Q[orig_state[0]][orig_state[1]][action]) + (alpha*(-1 + gamma*(max(Q[temp_state[0]][temp_state[1]])))))

			if is_terminal == 1:
				break

		stc[i] = count


	step_count = np.mean(stc)

	print "mean steps. = ", step_count


	for i in xrange(0, env.shape_of_A[0]):
		for j in xrange(0,env.shape_of_A[1]):
			
			V[i][j] = max(Q[i][j])

			#print i," ",j," ",np.argmax(Q[i][j])

	print np.round(V,2)	
	
	"""pol = np.empty([env.shape_of_A[0],env.shape_of_A[1]])

	for i in xrange(0, env.shape_of_A[0]):
		for j in xrange(0,env.shape_of_A[1]):

			if env.a[i][j] != '*':
				
				pol[i][j] = np.argmax(Q[i][j])

				pol_c.write(str(i))
				pol_c.write(" ")
				pol_c.write(str(j))
				pol_c.write(" ")
				pol_c.write(str(pol[i][j]))
				pol_c.write("\n")

				valf.write(str(i))
				valf.write(" ")
				valf.write(str(j))
				valf.write(" ")
				valf.write(str(max(Q[i][j])))
				valf.write("\n")

				for m in xrange(0,4):
					qv.write(str(i))
					qv.write(" ")
					qv.write(str(j))
					qv.write(" ")
					qv.write(str(m))
					qv.write(" ")
					qv.write("%0.4f"%Q[i][j][m])
					qv.write("\n")
"""

	print "time = ", time.time() - start_time

if __name__ == "__main__":
	main()
