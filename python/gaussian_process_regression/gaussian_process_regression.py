__author__ = 'apple'

import numpy as np
from sklearn import gaussian_process
from scipy.io import loadmat
import math

FEATURE_PATH = r'/home/apple/data/wind_power/feature2.mat'
PREDICT_PATH = r'/home/apple/data/wind_power/predict2.mat'

feature = loadmat(FEATURE_PATH)['feature']
predict = loadmat(PREDICT_PATH)['predict']

ncount, feature_count = feature.shape

# Split the whole dataset into training set and test set
print 'Loading dataset...'
trn_ratio = 0.8
# Comment out this to run the full training samples
# trn_count = int(ncount*trn_ratio)
trn_count = 3000
test_count = ncount - trn_count
x_trn = feature[0:trn_count,:]
y_trn = predict[0:trn_count,0]
x_test = feature[ncount-test_count:,:]
y_test = predict[ncount-test_count:,0]

print 'Training...'
gp = gaussian_process.GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1)
gp.fit(x_trn, y_trn)

print 'Predicting...'
y_pred, sigma2_pred = gp.predict(x_test, eval_MSE=True)

# Test such number of samples
test_num = 50
for i in range(0,test_num):
    if y_test[i]!=0.0:
        print i
        print abs(y_test[i]-y_pred[i])/y_test[i]

# Computing mean squred error
print 'Computing mean squared error...'
print sum((y_test-y_pred)**2)/test_count

