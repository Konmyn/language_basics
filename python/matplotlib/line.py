import matplotlib.pyplot as plt
import numpy as np

# print(np.arange(10))
# print(np.random.randint(1, 6, 10))

fig = plt.figure()

ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

ax1.plot(np.arange(10), np.random.randint(1, 5, 10))
ax2.plot(np.arange(10), np.random.randint(1, 5, 10))
ax3.plot(np.arange(10), np.random.randint(1, 5, 10), c="r", label="rand1")
ax3.plot(np.arange(10), np.random.randint(1, 5, 10), c="g", label="rand2")
ax3.plot(np.arange(10), np.random.randint(1, 5, 10), c="b", label="rand3")

# plt.legend(loc="best")
plt.legend(loc="upper left")

# why it is for last subplot?
plt.xlabel("hello")
plt.ylabel("number")
plt.title("random number gen")

plt.show()
