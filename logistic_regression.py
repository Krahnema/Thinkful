import pandas as pd
import statsmodels.api as sm
from numpy import e

loansData = pd.read_csv('/Users/kimya/Desktop/loansData.csv')

cleanInterestRate = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) /100, 4))
loansData['Interest.Rate'] = cleanInterestRate

cleanLoanLength = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))
loansData['Loan.Length'] = cleanLoanLength

loansData['FICO.Range'] = loansData['FICO.Range'].astype("string")
cleanFICORange = map(lambda x: int(x.split('-')[0]), loansData['FICO.Range'])
loansData['FICO.Score'] = cleanFICORange


loansData.to_csv('loansData_clean.csv', header = True, index = False)


# Create binary value: 0 if interest rate is below 12%, 1 if it is above

loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x < 0.12 else 0)

loansData[loansData['Interest.Rate'] == 0.10].head()
loansData[loansData['Interest.Rate'] <= 0.12].head()

loansData['Intercept'] = 1.0



ind_vars = ['Amount.Requested', 'FICO.Score', 'Intercept']

# ind_vars = ['Amount.Requested', 'FICO.Score', 'Interest.Rate', 'Intercept']

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])


result = logit.fit()
coeff = result.params
print coeff


# Function that takes FICO Score and Loan Amount and returns p

def logistic_function(FICO, LoanAmt, coeff):
	p = 1 / (1 + e**(- coeff[2] - coeff[1]*FICO - coeff[0]*LoanAmt))
	return p

# What is the probability we can obtain a loan at <12% interest rate for
# $10,000 with a FICO score of 720?

logistic_function(720, 10000, coeff)

# The probability is 0.75, above our threshold 0.70, meaning we will get
# the loan.

import matplotlib.pyplot as plt
import numpy as np

# Create a subset that will only have the rows where the loan amount is 10,000
new = loansData[loansData['Amount.Requested'] == 10000]

fi = np.arange(650, 850)

# plot the data
plt.scatter(new['FICO.Score'], new['IR_TF'])
# plt.show()

# plot your model
plt.plot(fi, logistic_function(fi, 10000, coeff), 'r-')   # r- to get a red line
plt.show()



