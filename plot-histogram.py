#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

# v = 10m/s => a = -10m/s^2 => save distance = 5m
(mu, sigma) = (5, 2)
x = mu + sigma * np.random.randn(100)

# x must be the save distance of the respective vehicle at the speed
x = [ 5, 5, 3, 4, 3, 4, 6, 7, 8, 9, 10 ]

# the histogram of the data
n, bins, patches = plt.hist(x, 20, facecolor='g', alpha=0.75) # density=True,


plt.xlabel('Save distance in m')
plt.ylabel('Count')
plt.title('Histogram for car save distance at v=10 m/s')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.xlim(0, 20)
plt.grid(True)
plt.show()
