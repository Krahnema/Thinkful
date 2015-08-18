import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# read in the data

df = pd.read_csv('/Users/kimya/Desktop/LoanStats3b.csv', header=1, low_memory=False)

# convert strings to datetime objects in pandas

df['issue_d_format'] = pd.to_datetime(df['issue_d'])
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x: x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

# plot the loan data

# pd.scatter(loan_count_summary, funded_amnt)

plt.figure()
plt.plot(loan_count_summary)
plt.show()


sm.graphics.tsa.plot_acf(loan_count_summary)

sm.graphics.tsa.plot_pacf(loan_count_summary)




