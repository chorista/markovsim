import operation as op

def main(p, beta):
	src_matrix= [[[0.5,0.5],[0.5,0.5]], [[1-p, p],[p,1-p]]]

	src_a = op.Source(src_matrix[0])
	src_b = op.Source(src_matrix[1])

	receiver = op.Receiver(src_matrix)

	error_cost = 0
	comm_cost = 0

	for i in range(1,1000):
		src_a.updateSource()
		src_b.updateSource()
		receiver.updateReceiver(i)
		comm_cost += receiver.entropy[i%2]
		if i%2 == 0:
			receiver.doObserve(src_a, 0, i)
		else:
			receiver.doObserve(src_b, 1, i)
		
		state_real= [src_a.state, src_b.state]
		state_estimation =[receiver.estimation[0], receiver.estimation[1]]
		
		error_cost += op.calculateError(state_real, state_estimation)

	return [error_cost,comm_cost]

