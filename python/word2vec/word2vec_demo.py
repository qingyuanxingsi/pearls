__author__ = 'apple'

import word2vec
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import CountVectorizer

'''
A simple word2vec demo illustrating the use of the python word2vec interface
@Date:2015-5-22
'''

TEXT_PATH = '/home/apple/data/kaggle/senti_analysis/unlabeledTrainData.tsv'
WORD_PATH = '/home/apple/data/kaggle/senti_analysis/train_text'
PHRASE_PATH = '/home/apple/data/kaggle/senti_analysis/senti-phrase'
BIN_PATH = '/home/apple/data/kaggle/senti_analysis/senti.bin'
CLUSTER_PATH = '/home/apple/data/kaggle/senti_analysis/senti-clusters.txt'

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

tag = 0
f_word = open(WORD_PATH, 'w')
corpura = []
with open(TEXT_PATH) as f:
    for line in f:
        if tag != 0:
            orig_text = line.split('\t', 1)[1]
            f_word.write(clean_text(orig_text,remove_stopwords=True))
        tag+=1

'''
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)
train_data_features = vectorizer.fit_transform(corpura)
train_data_features = train_data_features.toarray()
print train_data_features.shape
'''

word2vec.word2phrase(WORD_PATH, PHRASE_PATH, verbose=True)

# Train word2vec model using the text8-phrase output
word2vec.word2vec(PHRASE_PATH, BIN_PATH, size=300, verbose=True)

# Do the clustering of the vectors based on the trained model
word2vec.word2clusters(WORD_PATH, CLUSTER_PATH, 100, verbose=True)

print '\nLoading the word2vec model...'
model = word2vec.load(BIN_PATH)
print model.vocab
print model.vectors.shape
print model['movie'][:10]

print 'Find words similar to the given word using cosine distance...'
indexes, metrics = model.cosine('dog')
print model.generate_response(indexes,metrics)

# Find analogies
print 'Finding analogies...'
indexes_ana, metrics_ana = model.analogy(pos=['king', 'woman'], neg=['man'], n=10)
print model.generate_response(indexes_ana, metrics_ana)

# Play with clusters
print 'Playing with clusters'
clusters = word2vec.load_clusters(CLUSTER_PATH)

# Get the cluster word 'dog' belongs to
print clusters['dog']

print clusters.get_words_on_cluster(90)[:10]

model.clusters = clusters
indexes_cluster, metrics_cluster = model.analogy(pos=['paris', 'germany'], neg=['france'], n=10)
print model.generate_response(indexes_cluster, metrics_cluster)