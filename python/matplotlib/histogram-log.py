import matplotlib.pyplot as plt
import numpy as np

data = [1.2, 14, 150]
bins = 10 ** (np.arange(0, 4))
print("bins: ", bins)
plt.xscale("log")
plt.hist(data, bins=bins)

plt.show()
