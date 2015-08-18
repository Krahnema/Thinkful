import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/kimya/Desktop/LoanStats3c.csv', header=1, low_memory = False)

# remove null values
data = data.dropna()

data['int_rate'] = data['int_rate'].astype("string")
y = data['int_rate'].map(lambda x: float(x.rstrip('%')) /100)
data['Annual.Inc'] = data['annual_inc'].astype("float")
x = data['Annual.Inc']

# model 1
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()
model.summary()


# Add home ownership to the model

# make a new column that converst home ownership into a binary variable
data['Home'] = data['home_ownership'].map(lambda x: 1 if x == "MORTGAGE" else 0)
x_model2 = data[['Annual.Inc', 'Home']]

# model 2
X_model2 = sm.add_constant(x_model2)
model2 = sm.OLS(y, X_model2).fit()
model2.summary()

# Does it affect the significance of the coefficients in the first model?
# Yes, the p values decrease, yet still above 0.05. This means they are
# still not statistically significant if we take an alpha < 0.05 threshold.


# Add the interaction of home ownership and income to the model

data['Inc.Home'] = data['Annual.Inc'] * data['Home']

x_model3 = data[['Annual.Inc', 'Home', 'Inc.Home']]


# model 3
X_model3 = sm.add_constant(x_model3)
model3 = sm.OLS(y, X_model3).fit()
model3.summary()

# This model does not explain the data very well. The R-squared continues to
# be very low (not even 0.1).

plt.figure()
plt.scatter(x, y)

plt.plot(x, model3.params[0] + model3.params[1] * data['Annual.Inc'] + model3.params[2] * 1 + model3.params[3] * 1, 'r')

plt.show()












