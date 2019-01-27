import numpy as np
import sim_single as sim
import matplotlib.pyplot as plt

#prob = 0.4
prob = [float(p)/200 for p in range(1,200)]
#beta = range(1,200)
beta = 0.49

y_en = [sim.main('cost_min',p, beta) for p in prob]
y_rr = [sim.main('rr',p, beta) for p in prob]

y_en_error = np.array([y[0] for y in y_en])
y_en_comm = np.array([y[1] for y in y_en])
y_en_count = [y[2] for y in y_en]

y_rr_error = np.array([y[0] for y in y_rr])
y_rr_comm = np.array([y[1] for y in y_rr])


ax1 = plt.subplot(221)
plt.plot(prob, y_rr_error, 'r', label="round robin error")
plt.plot(prob, y_en_error, 'b', label = "cost minimize error")
ax1.set_xlabel('probability')
ax1.set_ylabel('total error')


ax2 = plt.subplot(222)
plt.plot(prob, y_rr_comm, 'r', label="round robin comm.cost")
plt.plot(prob, y_en_comm, 'b', label="cost minimize comm.cost")
ax2.set_xlabel('probability')
ax2.set_ylabel('entropy')



ax3 = plt.subplot(223)
plt.plot(prob, y_rr_comm*beta + y_rr_error, 'r', label="round robin total")
plt.plot(prob, y_en_comm*beta + y_en_error, 'b', label="cost minimize total")
ax3.set_xlabel('probability')
ax3.set_ylabel('total cost')


ax4 = plt.subplot(224)
plt.plot(prob, [y[0] for y in y_en_count], 'b', label='update_count')
ax4.set_xlabel('probability')
plt.legend()


plt.suptitle('beta=%f'%beta)
plt.show()


