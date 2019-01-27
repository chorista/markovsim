import operation as op
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(time, error, entropy):
	ax1 = plt.subplot(211)
	plt.plot(time, error[0], 'g', label="error_0")
	plt.plot(time, error[1], 'g--', label="error_1")
	#plt.xlim([0,20])
	ax1.set_xlabel('time')
	ax1.set_ylabel('expected error')
	plt.legend()

	ax2 = plt.subplot(212)
	plt.plot(time,entropy[0], 'g', label="entropy_0")
	plt.plot(time,entropy[1], 'g--', label="entropy_1")
	#plt.xlim([0,20])
	ax2.set_xlabel('time')
	ax2.set_ylabel('entropy')
	plt.legend()

	plt.suptitle('beta=%f, prob = %f'%(beta,probability) )

	plt.show()

def timeline(receiver, entropy, error, cum_entropy, cum_error):
	for i in range(0, receiver.num_source):
		entropy[i].append(receiver.entropy[i])
		error[i].append(receiver.error[i])
		cum_error[i].append(sum(error[i]))
		cum_entropy[i].append(cum_entropy[i][len(cum_entropy[i])-1])
		if i==receiver.num_source:
			cum_entropy[i][len(cum_entropy[i])-1] += entropy_cost

def calcOptimalUpdate(receiver, b, num_src):
	t=0

	optimal = [False for i in range(0,num_src)]

	cum_error=[0 for i in range(0,num_src)]
	cost = [0 for i in range(0,num_src)]
	min_cost = [b*receiver.entropy[i] for i in range(0,num_src)]
	optimal_time= [0 for i in range(0,num_src)]
	diff_next = [0 for i in range(0,num_src)]
	not_end=True

	while(not_end):
		t = t+1
		receiver.updateReceiver(t)
		end = False
		for i in range(0,num_src):
			cum_error[i] = cum_error[i]+receiver.error[i]

			if(not(optimal[i])):
				cost[i] = ((cum_error[i] + b*receiver.entropy[i])/(t+1))
				if(min_cost[i]>cost[i]):
					min_cost[i]=cost[i]
					if(t>=999):
						optimal[i]=True
						optimal_time[i] = t
				else:
					optimal[i]=True;
					optimal_time[i] = t
					diff_next[i] = cost[i]-min_cost[i]

		for flag in optimal:
			not_end = not_end and flag
		not_end = not(not_end) 

	#return each optimal time and order of differentiation
	return [optimal_time, diff_next.index(max(diff_next))]

def make3Dplot():
	fig = plt.figure()
	
	prob = [float(i)/400 for i in range(1,201)] #probability(0~0.5)
	beta = [float(i)/200 for i in range(1,201)] #beta(0~1)

	ps = []
	bs = []
	zs = []

	for p in prob:
		for b in beta:
			receiver = op.Receiver([[[1-p, p],[p,1-p]]])
			res = calcOptimalUpdate(receiver, b, 1)
			ps.append(p)
			bs.append(b)
			zs.append(res[0][0])	

	ps = np.reshape(ps,(200,200))
	bs = np.reshape(bs,(200,200))
	zs = np.reshape(zs,(200,200))
	colormap = mpl.cm.coolwarm
	norm = mpl.colors.Normalize(vmin=0, vmax=30)
	
	print(len(ps))

	
	surf = ax.plot_surface(ps, bs, zs, cmap=colormap, linewidth=0, antialiased=False)
	ax.set_zlim(-0.01, 30)
	plt.clim(0,30)
	fig.colorbar(surf)
	plt.show()

def make2Dplot():
	prob = [float(i)/400 for i in range(1,201)] #probability(0~0.5)
	beta = [float(i)/200 for i in range(1,201)] #beta(0~1)

	ps = []
	bs = []
	zs = []

	for p in prob:
		for b in beta:
			receiver = op.Receiver([[[1-p, p],[p,1-p]]])
			res = calcOptimalUpdate(receiver, b, 1)
			if(res[0][0] <40):
				ps.append(p)
				bs.append(b)
				zs.append(res[0][0])	
	
	ax = plt.scatter(ps,bs,c=zs, marker=',', s=1, cmap = mpl.cm.coolwarm)
	plt.xlabel('probability')
	plt.ylabel('beta')

	cb = plt.colorbar()
	cb.set_label("optimal update time")

	plt.show()



def main(mode, p, b):
	src_matrix= [[[0.3,0.7],[0.7,0.3]], [[1-p, p],[p,1-p]]]

	src = [op.Source(src_matrix[0]), op.Source(src_matrix[1])]

	receiver = op.Receiver(src_matrix)
	
	error_cost = 0
	comm_cost = 0

	entropy = [[0] for i in range(0,receiver.num_source)]
	error = [[0] for i in range(0,receiver.num_source)]

	entropy_cost=0

	cum_entropy = [[0] for i in range(0,receiver.num_source)]
	cum_error = [[0] for i in range(0,receiver.num_source)]
	
	update_count = [0 for i in range(0,receiver.num_source+1)]

	#pre-calculated optimal update time
	find_optimal = calcOptimalUpdate(receiver, b, 2)
	#if mode == 'cost_min': print(find_optimal)
	is_optimal = [False, False]

	for t in range(1,1000):
		src[0].updateSource()
		src[1].updateSource()
		receiver.updateReceiver(t)
		if mode == 'rr':
			update_source = t%2
			comm_cost+=receiver.entropy[update_source]
			entropy_cost = receiver.entropy[update_source]
			receiver.doObserve(src[update_source], update_source, t)

			update_count[update_source] += 1

		elif mode == 'cost_min':

			if(t-receiver.time_observed[0]>=find_optimal[0][0]):
				is_optimal[0] = True
			if(t-receiver.time_observed[1]>=find_optimal[0][1]):
				is_optimal[1] = True

			if(is_optimal[0] or is_optimal[1]):
				if(not(is_optimal[0]) and is_optimal[1]):
					update_source = 1
					is_optimal[1] = False

				elif(is_optimal[0] and not(is_optimal[1])):
					update_source=0
					is_optimal[0] = False

				elif(is_optimal[0] and is_optimal[1]):
					update_source = find_optimal[1]
					is_optimal[update_source]=False

				comm_cost+=receiver.entropy[update_source]
				receiver.doObserve(src[update_source], update_source, t)

				update_count[update_source] += 1

		state_real= [src[0].state, src[1].state]
		state_estimation =[receiver.estimation[0], receiver.estimation[1]]

		#timeline(receiver, entropy, error, cum_entropy, cum_error)
		
		error_cost+=op.calculateError(state_real, state_estimation)

	#print("probability"+str(p))
	return [error_cost, comm_cost, update_count]


#make2Dplot()