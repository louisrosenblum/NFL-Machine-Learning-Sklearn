import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import csv
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


train_data = pd.read_csv("train.csv", sep=",")

predict = "Actual"

X = np.array(train_data.drop([predict], 1)) # Features
y = np.array(train_data[predict]) # Labels

test_data = pd.read_csv("test.csv", sep=",")

x_test = np.array(test_data)


linear = linear_model.LassoCV()

xdel = np.delete(X,0,1)
xdel2 = np.delete(x_test,0,1)

# Apply min max scaler to the datasets
sc = MinMaxScaler()                    
sc.fit(X)                          
X_train_std = sc.transform(xdel)      
X_test_std = sc.transform(xdel2)

linear.fit(X_train_std,y)

predictions = linear.predict(X_test_std)  # Gets a list of all predictions

with open('flex.csv', mode='w') as flex:
    writer = csv.writer(flex, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')

    for x in range(len(predictions)):
        writer.writerow([x_test[x][0],predictions[x]])
