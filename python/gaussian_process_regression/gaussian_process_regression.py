__author__ = 'apple'

from sklearn import gaussian_process
from scipy.io import loadmat

# Currently best result
# regr 'linear' 'absolute_exponential' mean squared error 7000/200 0.00784017636428

FEATURE_PATH = r'/home/apple/data/wind_power/feature2.mat'
PREDICT_PATH = r'/home/apple/data/wind_power/predict2.mat'

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
x_trn = feature[0:trn_count,:]
y_trn = predict[0:trn_count,0]
x_test = feature[ncount-test_count:,:]
y_test = predict[ncount-test_count:,0]

print 'Training...'
gp = gaussian_process.GaussianProcess(regr='linear', corr='absolute_exponential')
gp.fit(x_trn, y_trn)

print 'Predicting...'
y_pred, sigma2_pred = gp.predict(x_test, eval_MSE=True)

# See what's happening with the test samples
print 'Computing relative error...'
for i in range(0, test_count):
    if y_test[i] != 0.0:
        print "%d,%.11f" % (i+1, (abs(y_test[i]-y_pred[i]))/y_test[i])

print 'Computing Mean Squared Error...'
print sum((y_pred-y_test)**2)/test_count

