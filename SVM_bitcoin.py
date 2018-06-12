import pandas as pd
import numpy as np
from sklearn import svm
import sklearn.decomposition as pca
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale=1.2)

# Pickle package
import pickle

def predict_movement(day_diff, volatility, sia):
    if(model.predict([[day_diff, volatility, sia]])) == 0:
        return 'Down'
    else:
        return 'Up'

# train_data = pd.read_csv('trainMe.csv') #--- USE SIA2 instead of Volatility
# test_data = pd.read_csv('testMe.csv')
# train_data = pd.read_csv('combinedTRAIN.csv')
# test_data = pd.read_csv('combinedTEST.csv')

train_data = pd.read_csv('checkTRAIN.csv')
test_data = pd.read_csv('checkTEST.csv')

train_data['Volume'] = train_data['Volume']/1000000;
test_data['Volume'] = test_data['Volume']/1000000;

print('Length train data: '+str(len(train_data)))
print('Length test data: '+str(len(test_data)))

# Plot two features
sns.lmplot('Day Diff', 'SIA', data=train_data, hue='Movement',
           palette='Set1', fit_reg=False, scatter_kws={"s": 70})
plt.show()


# Specify inputs for the model
imp_features = train_data[['Day Diff', 'SIA', 'Volatility']].as_matrix()
movement_label = np.where(train_data['Movement']=='Up', 1, 0)





# PCA fitting
PCA = pca.PCA(n_components=3)
PCA.fit(imp_features)
new_features = PCA.transform(imp_features)


# Fit the SVM model
model = svm.SVC(kernel='linear')
print('Fitting model..')
model.fit(new_features, movement_label)

i=0
accuracy=0

while i < len(test_data):

    result = predict_movement(test_data['Day Diff'][i], test_data['SIA'][i], test_data['Volatility'][i])
    if(result == test_data['Movement'][i]):
        print('Accuracy result for: ' + test_data['Date'][i] + result + ' -> TRUE')
        accuracy=accuracy+1
    else:
        print('Accuracy for: ' + test_data['Date'][i] + result + ' -> FALSE')

    i = i + 1

final_accuracy = accuracy/len(test_data) *100
print('ACCURACY IS:'+str(final_accuracy)+'%')






# # Get the separating hyperplane
# w = model.coef_[0]
# a = -w[0] / w[1]
# xx = np.linspace(-10000, 10000) #min - max feature value
# yy = a * xx - (model.intercept_[0]) / w[1]
#
# # Plot the parallels to the separating hyperplane that pass through the support vectors
# b = model.support_vectors_[0]
# yy_down = a * xx + (b[1] - a * b[0])
# b = model.support_vectors_[-1]
# yy_up = a * xx + (b[1] - a * b[0])
#
# # Plot the hyperplane
# sns.lmplot('Close Off High','Day Diff', data=train_data, hue='Movement', palette='Set1', fit_reg=False, scatter_kws={"s": 70})
# plt.plot(xx, yy, linewidth=2, color='black');
# plt.show()
#
#
# # Look at the margins and support vectors
# sns.lmplot('Close Off High', 'Day Diff', data=train_data, hue='Movement', palette='Set1', fit_reg=False, scatter_kws={"s": 70})
# plt.plot(xx, yy, linewidth=2, color='black')
# plt.plot(xx, yy_down, 'k--')
# plt.plot(xx, yy_up, 'k--')
# plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
#             s=80, facecolors='none');
# plt.show()




