from nltk.corpus import stopwords
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import word2vec

LABELED_PATH = r'/home/apple/data/kaggle/senti_analysis/labeledTrainData.tsv'
TEST_PATH = r'/home/apple/data/kaggle/senti_analysis/testData.tsv'
BIN_PATH = '/home/apple/data/kaggle/senti_analysis/senti.bin'
CLUSTER_PATH = '/home/apple/data/kaggle/senti_analysis/senti-clusters.txt'

cluster_num = 100
clusters = word2vec.load_clusters(CLUSTER_PATH)

def clean_text(text, remove_stopwords=False):
    # 1. Remove HTML
    review_text = BeautifulSoup(text).get_text()
    #
    # 2. Remove non-letters
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    #
    # 6. Join the words back into one string separated by space,
    # and return the result.
    return " ".join(words)

def generateBagOfClusters(review):
    """
    Generate Bag of Clusters
    :param review:
    :return:
    """
    words = review.split()
    featureVec = np.zeros((cluster_num,),dtype=np.int)
    for i in xrange(0,len(words)):
        if words[i] in clusters.vocab:
            cluster_index = clusters.get_cluster(words[i])
            featureVec[cluster_index]+=1
    return featureVec

def generateFeatureVecs(reviews):
    """
    Generate feature vectors for whole review set
    :param reviews:
    :return:
    """
    size = len(reviews)
    featureVecs = np.zeros((size,cluster_num),dtype=np.int)
    for i in xrange(0,size):
        if (i+1)%100 == 0:
            print "Generated %d of %d" % (i+1, size)
        featureVecs[i] = generateBagOfClusters(reviews[i])
    return featureVecs

labelData = pd.read_csv(LABELED_PATH, header=0,
 delimiter="\t", quoting=3)
testData = pd.read_csv(TEST_PATH, header=0,
 delimiter="\t", quoting=3)

num_reviews = labelData["review"].size
test_reviews = labelData['review'].size

# Initialize an empty list to hold the clean reviews
clean_train_reviews = []
clean_test_reviews = []

# Loop over each review; create an index i that goes from 0 to the length
# of the movie review list
for i in xrange(0, num_reviews):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    if (i+1)%1000 ==0:
        print "Review %d of %d" % (i+1, num_reviews)
    clean_train_reviews.append(clean_text(labelData["review"][i], remove_stopwords=True))

for i in xrange(0, test_reviews):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    if (i+1)% 1000 ==0:
        print "Test Review %d of %d" % (i+1, test_reviews)
    clean_test_reviews.append(clean_text(testData["review"][i], remove_stopwords=True))

train_feature = generateFeatureVecs(clean_train_reviews)
train_target = labelData['sentiment']

test_feature = generateFeatureVecs(clean_test_reviews)

# Fit a random forest and extract predictions
forest = RandomForestClassifier(n_estimators=100)

# Fitting the forest may take a few minutes
print "Fitting a random forest to labeled training data..."
forest = forest.fit(train_feature, train_target)
result = forest.predict(test_feature)

# Write the test results
output = pd.DataFrame(data={"id":testData["id"], "sentiment":result})
output.to_csv(r"/home/apple/data/kaggle/senti_analysis/BagOfCentroids.csv", index=False, quoting=3)


