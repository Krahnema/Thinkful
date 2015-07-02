import pandas as pd
import matplotlib.pyplot as plt

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')


# Look at the first 5 rows to get an idea of what the data looks like

loansData['Interest.Rate'][0:5]
loansData['Loan.Length'][0:5]
loansData['FICO.Range'][0:5]

# The data is all in different formats: strings, percentages, ranges.
# That needs to be cleaned and put into the same formats.

# use .map, remove %, convert to float, divide by 100 and round to 4 decimal places.
# Then make sure to replace the column in the dataframe.
cleanInterestRate = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) /100, 4))
loansData['Interest.Rate'] = cleanInterestRate

# Get rid of "months" in the data and convert to integer
cleanLoanLength = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
loansData['Loan.Length'] = cleanLoanLength

# Convert to a string so you can split data on the hyphen
loansData['FICO.Range'] = loansData['FICO.Range'].astype("string")

# This is another way to use map. Split on hyphen, select only lower number, convert to integer
cleanFICORange = map(lambda x: int(x.split('-')[0]), loansData['FICO.Range'])

# Save the output to a new column FICO.Score
loansData['FICO.Score'] = cleanFICORange


# loansData.shape()

plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

# The result is not a Gaussian distribution.

# Look at a scatterplot matrix to see the variables' relationship with each other.

plt.figure()
a = pd.scatter_matrix(loansData, alpha= 0.05, figsize = (10,10), diagonal = 'hist')
plt.show()

# There is a natural trend between Amounts Requested and Amounts Funded, as to be expected.
# You can also notice a clear trend in the relationship between FICO Scores and Interest Rate.
# There is an inverse relationship: As the FICO Score goes up, the interest rate goes down.


# FICO Score and Loan Amount are independent variables. The linear model will look like this:
# InterestRate = b + a1(FICOScore) + a2(LoanAmount)
# We need statsmodels to find the coefficients:

import numpy as np
import statsmodels.api as sm

# Extract necessary columns to make it easier:
intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

# Since we are extracting from a DataFrame, the columns will be returned as Series,
# so we need to reshape.
y = np.matrix(intrate).transpose()    # Dependent variable
x1 = np.matrix(fico).transpose()      # Independent variable
x2 = np.matrix(loanamt).transpose()   # Independent variable

# Put both columns together for an input matrix:
x = np.column_stack([x1,x2])

# Now we can create the linear model and output the results:
X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()
f.summary()






