#-*- encoding:utf-8 -*-

from sklearn import gaussian_process
from scipy.io import loadmat

# Currently best result
# regr 'linear' 'absolute_exponential' mean squared error 7000/200
# nugget 1.20 0.00529941624265
# result
# hour(predict) gpr svr
# 1 0.00529941624265 0.0114827317953
# 2 0.0119753252329  0.017409596707
# 3 0.0183334545067  0.0239514596978
# 4 0.0240665391347  0.0313535837877
# 5 0.0288206417149  0.0378738951131
# 6 0.0322829683652  0.039860187969

from sklearn import svm
from sklearn.gaussian_process.gaussian_process import MACHINE_EPSILON

FEATURE_PATH = '/home/apple/data/wind_power/feature2.mat'
PREDICT_PATH = '/home/apple/data/wind_power/predict2.mat'

feature = loadmat(FEATURE_PATH)['feature']
predict = loadmat(PREDICT_PATH)['predict']

ncount, feature_count = feature.shape

# Split the whole dataset into training set and test set
print 'Loading dataset...'
trn_ratio = 0.8
# trn_count = int(ncount*trn_ratio)
trn_count = 7000
test_count = 200
# test_count = ncount - trn_count
x_trn = feature[0:trn_count, :]
y_trn = predict[0:trn_count, 0]
x_test = feature[ncount-test_count:, :]
y_test = predict[ncount-test_count:, 0]

print 'Training...'
gp = gaussian_process.GaussianProcess(regr='linear',
                                      corr='absolute_exponential',
                                      nugget=1.20)
gp.fit(x_trn, y_trn)

# SVR
clf = svm.SVR()
clf.fit(x_trn, y_trn)
y_pred_svm = clf.predict(x_test)

print 'Predicting...'
# y_pred is the prediction value of corresponding x_test
y_pred, sigma2_pred = gp.predict(x_test, eval_MSE=True)

# See what's happening with the test samples
print 'Computing relative error...'
for i in range(0, test_count):
    if y_test[i] != 0.0:
        print "%d,%.11f,%.11f" % (i+1, (abs(y_test[i]-y_pred[i]))/y_test[i],(abs(y_test[i]-y_pred_svm[i]))/y_test[i])

print 'Computing Average Squared Error...'
print sum((y_pred-y_test)**2)/test_count
print sum((y_pred_svm-y_test)**2)/test_count
