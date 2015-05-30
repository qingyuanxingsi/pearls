__author__ = 'apple'

import word2vec

'''
A simple word2vec demo illustrating the use of the python word2vec interface
@Date:2015-5-22
'''

TEXT_PATH = '/home/apple/data/kaggle/senti_analysis/unlabeledTrainData.tsv'
WORD_PATH = '/home/apple/data/kaggle/senti_analysis/train_text'
PHRASE_PATH = '/home/apple/data/kaggle/senti_analysis/senti-phrase'
BIN_PATH = '/home/apple/data/kaggle/senti_analysis/senti.bin'
CLUSTER_PATH = '/home/apple/data/kaggle/senti_analysis/senti-clusters.txt'

tag = 0
f_word = open(WORD_PATH, 'w')
with open(TEXT_PATH) as f:
    for line in f:
        if tag!=0:
            f_word.write(line.split('\t', 1)[1])
        tag+=1

word2vec.word2phrase(WORD_PATH, PHRASE_PATH, verbose=True)

# Train word2vec model using the text8-phrase output
word2vec.word2vec(PHRASE_PATH, BIN_PATH, size=300, verbose=True)

# Do the clustering of the vectors based on the trained model
word2vec.word2clusters(TEXT_PATH, CLUSTER_PATH, 100, verbose=True)

print '\nLoading the word2vec model...'
model = word2vec.load(BIN_PATH)
print model.vocab
print model.vectors.shape
print model['a'][:10]

print 'Find words similar to the given word using cosine distance...'
indexes, metrics = model.cosine('dog')
print model.generate_response(indexes,metrics)

# Find analogies
print 'Finding analogies...'
indexes_ana, metrics_ana = model.analogy(pos=['king', 'woman'], neg=['man'], n=10)
print model.generate_response(indexes_ana, metrics_ana)

# Play with clusters
print 'Pla' \
      '' \
      'ying with clusters'
clusters = word2vec.load_clusters(CLUSTER_PATH)

# Get the cluster word 'dog' belongs to
print clusters['dog']

print clusters.get_words_on_cluster(90)[:10]

"""
model.clusters = clusters
indexes_cluster, metrics_cluster = model.analogy(pos=['paris', 'germany'], neg=['france'], n=10)
print model.generate_response(indexes_cluster, metrics_cluster)
"""