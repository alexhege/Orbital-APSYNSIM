import numpy as np
import matplotlib.pyplot as plt


mean = [-10, 0]
cov = [[5, 0], [0, 2]]


x, y = np.random.multivariate_normal(mean, cov, 50000).T

mean = [10, 0]
x2, y2 = np.random.multivariate_normal(mean, cov, 50000).T

x = np.concatenate((x, x2))
y = np.concatenate((y, y2))


fig = plt.figure()
ax=fig.add_subplot(1,1,1)
plt.axis('off')


extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

plt.hist2d(x, y, bins=750, range = [[-20, 20], [-20, 20]], cmap=plt.get_cmap('afmhot'))

#plt.show()

fig.savefig('out.png', bbox_inches=extent)


