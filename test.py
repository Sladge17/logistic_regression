import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot()
 
y = np.random.normal(0, 2, 500)
ax.hist(y)
ax.grid()
plt.show()