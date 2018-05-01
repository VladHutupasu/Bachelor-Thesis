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
sns.lmplot('Close Off High', 'Day Diff', data=bitcoin_data, hue='Movement',
           palette='Set1', fit_reg=False, scatter_kws={"s": 70})

plt.show()

# Specify inputs for the model
# ingredients = recipes[['Flour', 'Milk', 'Sugar', 'Butter', 'Egg', 'Baking Powder', 'Vanilla', 'Salt']].as_matrix()
imp_features = bitcoin_data[['Close Off High','Day Diff']].as_matrix()
movement_label = np.where(bitcoin_data['Movement']=='Up', 1, 0)


# Feature names
bitcoin_features = bitcoin_data.columns.values[1:].tolist()



# Fit the SVM model
model = svm.SVC(kernel='linear')
model.fit(imp_features, movement_label)


def predict_movement(close_off_high, day_diff):
    if(model.predict([[close_off_high, day_diff]])) == 0:
        print('Down movement')
    else:
        print('Upwards movement')

# predict_movement(-5858, 212)

# Get the separating hyperplane
w = model.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(-10000, 10000) #min - max feature value
yy = a * xx - (model.intercept_[0]) / w[1]

# Plot the parallels to the separating hyperplane that pass through the support vectors
b = model.support_vectors_[0]
yy_down = a * xx + (b[1] - a * b[0])
b = model.support_vectors_[-1]
yy_up = a * xx + (b[1] - a * b[0])

# Plot the hyperplane
sns.lmplot('Close Off High','Day Diff', data=bitcoin_data, hue='Movement', palette='Set1', fit_reg=False, scatter_kws={"s": 70})
plt.plot(xx, yy, linewidth=2, color='black');



# # Look at the margins and support vectors
# sns.lmplot('Close Off High', 'Day Diff', data=bitcoin_data, hue='Movement', palette='Set1', fit_reg=False, scatter_kws={"s": 70})
# plt.plot(xx, yy, linewidth=2, color='black')
# plt.plot(xx, yy_down, 'k--')
# plt.plot(xx, yy_up, 'k--')
# plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
#             s=80, facecolors='none');



plt.show()
