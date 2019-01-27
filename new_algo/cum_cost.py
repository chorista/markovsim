import operation as op
import matplotlib.pyplot as plt
import numpy as np
plt.rc('font', family='serif')
p=0.3
beta = 0.57
time = range(0,20)

src_matrix = [[[0.5,0.5],[0.5,0.5]], [[1-p, p],[p,1-p]]]
src = [op.Source(src_matrix[0]), op.Source(src_matrix[1])]
receiver = op.Receiver(src_matrix)

entropy_a = []
error_a = []
avg_cost_a = []

error_b = []
entropy_b = []
avg_cost_b = []
cum_error_b = []


for t in time:
	
	entropy_a.append(receiver.entropy[0])
	entropy_b.append(receiver.entropy[1])
	
	error_a.append(receiver.error[0])
	error_b.append(receiver.error[1])

	avg_cost_a.append((np.sum(error_a)+beta*receiver.entropy[0])/(t+1))
	avg_cost_b.append((np.sum(error_b)+beta*receiver.entropy[1])/(t+1))

	cum_error_b.append(np.sum(error_b))
	
	print("time: %d"%t)
	print( "err:" + str(receiver.error[1]))
	print( "cum_error:" + str(np.sum(error_b)))
	print( "ent:" + str(beta*receiver.entropy[1]))
	print( "avg_cost:" + str((np.sum(error_b)+beta*receiver.entropy[1])/(t+1)))
	print( "")
	

	receiver.updateReceiver(t+1)


#ax1 = plt.subplot(211)
#plt.plot(np.gradient(error_b), 'g--', label='error')
#plt.plot(np.gradient(entropy_b), 'g',label='entropy')
#ax1.set_ylabel("gradient")
#plt.legend()

ax1 = plt.subplot(131)
plt.plot(time,cum_error_b,'r', label =  'cum. error')
plt.xlabel('t')
plt.ylabel('cost')
ax1.legend( loc = "lower right")

ax3 = plt.subplot(132)
plt.plot(time,beta*np.array(entropy_b),'b', label = '%f*entropy'%beta)
plt.xlabel('t')
plt.ylabel('cost')
ax3.legend( loc = "lower right")


ax2 = plt.subplot(133)
plt.plot(time,avg_cost_b,'g',label = 'avg. cost')
plt.xlabel('t')
plt.ylabel('cost')

ax2.legend( loc = "lower right")
#for a, b in zip(time, error_b): plt.text(a, b, str(round(b,6)))

#for a, b in zip(time, avg_cost_b):
	#plt.text(a,b, str(round(b,3)))


plt.suptitle("p=%f, beta=%f"%(p,beta))
plt.subplots_adjust(hspace = 0.2, wspace = 0.3)
plt.show()



