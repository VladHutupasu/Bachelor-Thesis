# Packages for analysis
import pandas as pd
import numpy as np
from sklearn import svm

# Packages for visuals
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)

# Pickle package
import pickle

def predict_movement(close_off_high, day_diff):
    if(model.predict([[close_off_high, day_diff]])) == 0:
        return 'Down'
    else:
        return 'Up'

train_data = pd.read_csv('2017_train_data.csv')
test_data = pd.read_csv('2018_test_data.csv')

print('Length train data: '+str(len(train_data)))
print('Length test data: '+str(len(test_data)))

# Plot two features
sns.lmplot('Close Off High', 'Day Diff', data=train_data, hue='Movement',
           palette='Set1', fit_reg=False, scatter_kws={"s": 70})
plt.show()


# Specify inputs for the model
imp_features = train_data[['Close Off High', 'Day Diff']].as_matrix()
movement_label = np.where(train_data['Movement']=='Up', 1, 0)

# Feature names
bitcoin_features = train_data.columns.values[1:].tolist()



# Fit the SVM model
model = svm.SVC(kernel='linear')
model.fit(imp_features, movement_label)

# i=0
# accuracy=0
#
# while i < len(test_data):
#
#     result = predict_movement(test_data['Close Off High'][i], test_data['Day Diff'][i])
#     if(result == test_data['Movement'][i]):
#         print('Accuracy for: ' + str(i) + ' -> TRUE')
#         accuracy=accuracy+1
#     else:
#         print('Accuracy for: ' + str(i) + ' -> FALSE')
#
#     i = i + 1
#
# final_accuracy = accuracy/len(test_data) *100
# print('ACCURACY IS:'+str(final_accuracy)+'%')






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
sns.lmplot('Close Off High','Day Diff', data=train_data, hue='Movement', palette='Set1', fit_reg=False, scatter_kws={"s": 70})
plt.plot(xx, yy, linewidth=2, color='black');
plt.show()


# Look at the margins and support vectors
sns.lmplot('Close Off High', 'Day Diff', data=train_data, hue='Movement', palette='Set1', fit_reg=False, scatter_kws={"s": 70})
plt.plot(xx, yy, linewidth=2, color='black')
plt.plot(xx, yy_down, 'k--')
plt.plot(xx, yy_up, 'k--')
plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
            s=80, facecolors='none');
plt.show()




