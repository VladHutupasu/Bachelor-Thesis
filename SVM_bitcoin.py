# Packages for analysis
import pandas as pd
import numpy as np
from sklearn import svm

# Packages for visuals
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)

# Pickle package
import pickle

bitcoin_data = pd.read_csv('features.csv')
# print(bitcoin_data)

# Plot two ingredients
sns.lmplot('Close Off High', 'Volatility', data=bitcoin_data, hue='Movement',
           palette='Set1', fit_reg=False, scatter_kws={"s": 70})

plt.show()