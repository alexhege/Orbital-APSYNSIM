import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


mean = [-10, 0]
cov = [[5, 0], [0, 2]]
#cov = [[0, 10], [1, 0]]
#cov = [[1, 10], [10, 11]]

x, y = np.random.multivariate_normal(mean, cov, 5000000).T

mean = [10, 0]
x2, y2 = np.random.multivariate_normal(mean, cov, 5000000).T

x = np.concatenate((x, x2))
y = np.concatenate((y, y2))


fig = plt.figure()
ax=fig.add_subplot(1,1,1)
plt.axis('off')



#plt.axis([-20, 20, -20, 20])
plt.hist2d(x, y, bins=750, range = [[-20, 20], [-20, 20]], cmap=plt.get_cmap('afmhot'))

#ax.imshow(cmap=plt.get_cmap('afmhot'))
#plt.axis([-20, 20, -20, 20])

plt.show()

fig.savefig('out.png', bbox_inches='tight', pad_inches=0.0)
