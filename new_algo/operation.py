import numpy as np

class Source:
	def __init__(self, matrix):
		#source matrix
		self.matrix = np.array(matrix)

		#current state
		self.state = 0
		
	#update real source state
	def updateSource(self):
		val_rand = np.random.rand(1)

		for i in range(0,len(self.matrix[self.state])):
			if val_rand <= self.matrix[self.state,:i+1].sum():
				self.state = i
				break

class Receiver:
	
	def __init__(self, matrices):
		#number of sources
		self.num_source = 0

		#memory[source][time]. It has pre-calculated matrix value.
		self.memory = []

		#previously observed time
		self.time_observed = []

		#previously observed value
		self.state_observed = []
	
		#list of markov transition matrix
		self.matrices = []

		#estimation value of each source
		self.estimation = []

		#entropy of each source
		self.entropy = []

		#expected total cost	
		self.error = []

		for m in matrices:
			self.memory.append([np.array(m)])
			self.state_observed.append(0)
			self.time_observed.append(0)
			self.matrices.append(np.array(m))
			self.estimation.append(0)
			self.entropy.append(-(m[0]*np.log2(m[0])).sum())
			self.error.append(0)
			
			self.num_source+=1

	def updateReceiver(self, time):
		prob_min = 1;
		
		#update transition matrix and estimation value.
		for i in range(0,self.num_source):
			interval = time - self.time_observed[i]
			mem_length = len(self.memory[i])
			idx_prev = self.state_observed[i]
			
			if ( mem_length > interval ):
				self.matrices[i] = self.memory[i][interval-1]
			
			else:
				self.matrices[i] = np.dot(self.matrices[i], self.memory[i][0])
				self.memory[i].append(self.matrices[i])

			self.estimation[i] = np.argmax(self.matrices[i][idx_prev])
			log_2 = np.log2(self.matrices[i][idx_prev])

			#get entropy(expected communication cost when it updates source)
			self.entropy[i] = -(self.matrices[i][idx_prev]*log_2).sum()
		
			#expected error(when it does not update source)
			self.error[i] = 1 - self.matrices[i][idx_prev][self.estimation[i]] 
			#print "interval:"+str(interval)+ ", memlength:" +str(mem_length)

	
	#observe selected source and update estimation value.
	def doObserve(self, source, idx, time):
		result = source.state
		self.time_observed[idx] = time
		self.state_observed[idx] = result
		self.estimation[idx] = result
		self.entropy[idx] = 0
		self.error[idx] = 0

#Estimation error.
def calculateError(real, estimation):
	ret = 0
	for r, e in zip(real, estimation):
		ret += 0 if r==e else 1
	return ret
