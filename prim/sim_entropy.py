###Python 1st order markov source simulator###
import numpy as np
import operation as op
import matplotlib.pyplot as plt

num_source = op.num_source
num_state = op.num_state
sim_time = op.sim_time

#get expected cost and return source matrix, index of minimum value
def maxEntropy(Sources, Receiver, time) :
	matrices = []
	entropy = []
	for i in range(0, num_source) :
		prev_state = Receiver[i][0]
		matrices.append(op.getTransitionMatrix(Sources, Receiver, i, time))
		
		prob = matrices[i][prev_state]

		entropy.append(op.calculateEntropy(prev_state,matrices[i]))

	max_entropy = max(entropy)
	max_idx = entropy.index(max_entropy)

	return [matrices[max_idx], max_idx, max_entropy]
	

#Counting fail estimation
num_error = 0

print ("index,state,Cost,Error,Entropy,source="+str(num_source)+" state="+str(num_state))
#receiver (value, time)
receiver = [[0,0] for i in range(0,num_source)]


##Type a With minimize entropy
source = [op.generateMatrix_a(num_state) for i in range(0, num_source)]

for time in range(1, sim_time):
	min_val = maxEntropy(source, receiver, time)

	matrix = min_val[0]
	idx = min_val[1]
	prev = receiver[idx][0]

	res = op.doObserve( matrix, receiver, idx)
	cost = op.calculateCost(prev, res[1])
	error = op.calculateError(prev, res[0], res[1])
	entropy = min_val[2]
	num_error+=error
	print str(idx)+","+str(res[1])+","+ str(cost)+","+str(error)+","+str(entropy)
	receiver[idx][0] = res[1]
	receiver[idx][1] = time

print "ERROR RATE: " + str(float(num_error)/sim_time)
