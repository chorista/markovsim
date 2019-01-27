import operation as op
import numpy as np

def main(p, beta):
	src_matrix = [[[0.5,0.5],[0.5,0.5]], [[1-p, p],[p,1-p]]]

	src = [op.Source(src_matrix[0]), op.Source(src_matrix[1])]

	receiver = op.Receiver(src_matrix)

	error_cost = 0
	comm_cost = 0

	update_count = [0,0,0]

	for i in range(1,1000):
		src[0].updateSource()
		src[1].updateSource()
		receiver.updateReceiver(i)

		#expected error sum of not observed source
		error_else = (np.array(receiver.error).sum() - np.array(receiver.error)).tolist()
		
		#expected total cost, sqrt is starvation function

		update_idx = dict()

		print receiver.error,
		print (beta*np.array(receiver.entropy)).tolist(),
		#print max_cost
		for idx, (ent, err, er_else) in enumerate(zip(receiver.entropy, receiver.error, error_else)):
			if beta*ent <= err: #we need to update
				update_idx[beta*ent+er_else] = idx

		if bool(update_idx): #if update_idx is not empty
			#max() gets maximum key(cost) value.
			max_update_cost =update_idx[max(update_idx)] 

			comm_cost += receiver.entropy[max_update_cost]
			receiver.doObserve(src[max_update_cost], max_update_cost, i)
			update_count[max_update_cost] += 1
			print max_update_cost
		else:
			update_count[2] += 1
			print "update nothing" 

		state_real= [src[0].state, src[1].state]
		state_estimation =[receiver.estimation[0], receiver.estimation[1]]
		
		error_cost += op.calculateError(state_real, state_estimation)
	
	print '\n'

	return [error_cost, comm_cost, update_count]
