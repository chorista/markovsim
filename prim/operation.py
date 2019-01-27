###Python 1st order markov source simulator###
import numpy as np

np.random.seed(8)

#number of source
num_source = 2

#number of source states
num_state = 2

#simulation time
sim_time = 10

#probability
theta = 0.4

def getTransitionMatrix(Sources, Receiver, i, time):
	matrix_trans = np.array(Sources[i])
	matrix_ret = matrix_trans
	prev_time = Receiver[i][1]

	for i in range(1, time-prev_time):
		matrix_ret = np.dot(matrix_ret, matrix_trans)
	return matrix_ret

#Do observation. It returns observed value,
#calculated transition matrix.
def doObserve(matrix, Receiver, i):
	matrix_res = matrix
	val_state = -1;
	prev_state = Receiver[i][0]

	#generate random variable
	val_rand = np.random.rand(1)
	
	#get observation result
	for i in range (0, num_state):
		if val_rand[0]<=matrix_res[prev_state,:i+1].sum():
			val_state = i
			break;

	return [matrix_res, val_state]	


#Update cost is related to current value - previous value.
def calculateCost(prev, curr):
	delta = min([abs(num_state+curr-prev), abs(prev-curr), abs(num_state+prev-curr)])
	a = 1
	b = 0
	#1st-order linear cost function.
	cost = a*delta+b
	return cost

#calculate Error with estimated value - observed value
def calculateError(prev, M, curr):
	if (M[prev].tolist().index(max(M[prev])) - curr) == 0:
		return 0
	return 1
	

#Entropy is determined by previous state and time.
def calculateEntropy(prev, M):
	b = M[prev]
	log_b = []
	for v in M[prev]:
		if v==0:
			log_b.append(0)
		else:
			log_b.append(np.log2(v))
	
	log_b = np.array(log_b)

	return -(b*log_b).sum()

#for basic markov matrix for source type a 
def generateMatrix_a(num, p):
	matrix = [[1-p,p],[1-p,p]]
	return np.array(matrix)

#for source type b
def generateMatrix_half(num):
	matrix = [[0.5,0.5],[0.5,0.5]]
	return np.array(matrix)

