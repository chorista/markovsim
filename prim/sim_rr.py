###Python 1st order markov source simulator###
import numpy as np
import operation as op


num_source= op.num_source
num_state = op.num_state
sim_time = op.sim_time


#Counting fail estimation
num_error = 0

print ("source,state,Cost,Error,Entropy,source="+str(num_source)+" state="+str(num_state))
#receiver (value, time)
receiver = [[0,0] for i in range(0,num_source)]

## Type a With round ro
source = [op.generateMatrix_a(num_state) for i in range(0,num_source)]
for time in range(1,sim_time):
	idx = time%num_source
	prev = receiver[idx][0]
	matrix = op.getTransitionMatrix(source, receiver, idx, time)
	res = op.doObserve( matrix, receiver, idx)
	cost = op.calculateCost(prev, res[1])
	error = op.calculateError(prev, res[0], res[1])
	entropy = op.calculateEntropy(prev,res[0])
	num_error+=error
	print str(idx)+","+str(res[1])+","+str(cost)+","+str(error)+","+str(entropy)
	receiver[idx][0] = res[1]
	receiver[idx][1] = time
print "ERROR RATE: " + str(float(num_error)/sim_time)
