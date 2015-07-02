import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats


# Read in the data

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# Remove rows that have null values

loansData.dropna(inplace = True)


# Visualize the data for the "Amount.Requested" column and compare
# it to the "Amount.Funded.By.Investors"

# Boxplot

loansData.boxplot(column = "Amount.Requested")
plt.show()
plt.savefig("loansData_requ_box.png")

# The 1st to 3rd quartile show the data for amount requested lies 
# between $6,000 and $17,000. This is very similar to the actual
# amount that was funded by investors with, however, a slightly 
# lower median.


# Histogram

loansData.hist(column = "Amount.Requested")
plt.show()
plt.savefig("loansData_requ_hist.png")

# The overall frequency of amounts requested and funded are similar.
# However, the 5,000-10,000 range is not as predominantly requested
# as it was funded. This is most likely due to people requesting a
# higher amount than they have gotten funded. This is supported by
# overall higher frequencies for larger amounts requested. up to 35


# QQ-Plot

plt.figure()
graph = stats.probplot(loansData["Amount.Requested"], dist = "norm", plot = plt)
plt.show()
plt.savefig("loansData_requ_qqplot.png")

# Both the amounts requested and funded show the same style QQ Plot.
# The data is not normally distributed. from 0 - 35






