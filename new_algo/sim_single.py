import operation as op
import numpy as np
import matplotlib.pyplot as plt

probability = 0.25
beta = 0.4

def plot(time, error, entropy):
	ax1 = plt.subplot()
	plt.plot(time, error[0], 'g', label="error_0")
	plt.plot(time, error[1], 'g--', label="error_1")
	#plt.xlim([0,20])
	ax1.set_xlabel('time')
	ax1.set_ylabel('expected error')

	plt.legend()
	plt.suptitle('beta=%f, prob = %f'%(beta,probability) )
	plt.show()

def main(mode, p, b):
	src_matrix = [[[p, 1-p],[1-p,p]]]

	src = [op.Source(src_matrix[0])]

	receiver = op.Receiver(src_matrix)
	
	error_cost = 0
	comm_cost = 0

	entropy = [[0] for i in range(0,receiver.num_source)]
	error = [[0] for i in range(0,receiver.num_source)]

	entropy_cost=0

	cum_entropy = 0
	cum_error = 0
	
	update_count = [0 for i in range(0,receiver.num_source+1)]

	for t in range(1,1000):
		src[0].updateSource()
		receiver.updateReceiver(t)

		if mode == 'rr':
			comm_cost+= receiver.entropy[0]
			receiver.doObserve(src[0], 0, t)

		elif mode == 'cost_min':
			cum_error += (receiver.error[0])
			cum_entropy += (receiver.entropy[0])
			interval = t-receiver.time_observed[0]

			if cum_error>= b*cum_entropy: 
				comm_cost+= receiver.entropy[0]
				cum_error = 0
				cum_entropy = 0
				update_count[0] += 1
				receiver.doObserve(src[0], 0, t)

		state_real= [src[0].state]
		state_estimation =[receiver.estimation[0]]

		error_cost+=op.calculateError(state_real, state_estimation)


	#plot(range(0,1000), error, entropy)
	#plot(range(0,1000), cum_error, cum_entropy)

	return [error_cost, comm_cost, update_count]

#main('rr', probability, beta)
