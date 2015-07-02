import collections
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Create the data

x = [1,1,1,1,1,1,1,1,2,2,2,3,4,4,4,4,5,6,6,6,7,7,7,7,7,7,7,7,8,8,9,9]


# Output the frequency

c = collections.Counter(x)
print c

count_sum = sum(c.values())
for k,v in c.iteritems():
	print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)


# Create and save a boxplot

plt.boxplot(x)
plt.show()
plt.savefig("x_boxplot.png")


# Create and save a histogram

plt.hist(x, histtype = 'bar')
plt.show()
plt.savefig("x_histogram.png")


# Create and save a QQ-plot

plt.figure()
graph1 = stats.probplot(x, dist = "norm", plot = plt)
plt.show()
plt.savefig("x_qq_plot.png")



