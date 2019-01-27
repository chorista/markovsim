import numpy as np
import sim
import matplotlib.pyplot as plt

#prob = 0.4
prob = [float(p)/400 for p in range(1,200)]
#beta = range(1,200)
beta = 0.6

y_en = [sim.main('cost_min',p, beta) for p in prob]
y_rr = [sim.main('rr',p, beta) for p in prob]

y_en_error = np.array([y[0] for y in y_en])
y_en_comm = np.array([y[1] for y in y_en])
y_en_count = [y[2] for y in y_en]

y_rr_error = np.array([y[0] for y in y_rr])
y_rr_comm = np.array([y[1] for y in y_rr])


ax1 = plt.subplot(221)
plt.plot(prob, y_rr_error, 'r--', label="rr")
plt.plot(prob, y_en_error, 'b', label = "cm")
ax1.set_xlabel('p_b')
ax1.set_ylabel('expected error')
plt.title("(1)")
plt.legend()

ax2 = plt.subplot(222)
plt.plot(prob, y_rr_comm, 'r--', label="rr")
plt.plot(prob, y_en_comm, 'b', label="cm")
ax2.set_xlabel('p_b')
ax2.set_ylabel('entropy')
plt.title("(2)")
plt.legend()


ax3 = plt.subplot(223)
plt.plot(prob, y_rr_comm + y_rr_error, 'r--', label="rr")
plt.plot(prob, y_en_comm + y_en_error, 'b', label="cm")
ax3.set_xlabel('p_b')
ax3.set_ylabel('total cost')
plt.title("(3)")
plt.legend()

ax4 = plt.subplot(224)
plt.plot(prob, [y[0] for y in y_en_count], 'b--', label='source a')
plt.plot(prob, [y[1] for y in y_en_count], 'b', label='source b')
#plt.plot(prob, [y[2] for y in y_en_count], 'b:', label='update nothing')
ax4.set_xlabel('p_b')
ax4.set_ylabel('update count')
plt.title("(4)")
plt.legend()


plt.suptitle("p_a = %f, beta=%f"%(0.3,beta))
plt.subplots_adjust(hspace = 0.3, wspace = 0.3)
plt.show()


