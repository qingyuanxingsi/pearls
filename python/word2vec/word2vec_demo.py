__author__ = 'apple'

import word2vec

'''
A simple word2vec demo illustrating the use of the python word2vec interface
@Date:2015-5-22
'''

TEXT_PATH = '/home/apple/data/pearls/text8'
PHRASE_PATH = '/home/apple/data/pearls/text8-phrase'
BIN_PATH = '/home/apple/data/pearls/text8.bin'
CLUSTER_PATH = '/home/apple/data/pearls/text8-clusters.txt'


word2vec.word2phrase(TEXT_PATH, PHRASE_PATH, verbose=True)

# Train word2vec model using the text8-phrase output
word2vec.word2vec(PHRASE_PATH, BIN_PATH, size=100, verbose=True)

# Do the clustering of the vectors based on the trained model
word2vec.word2clusters(TEXT_PATH, CLUSTER_PATH, 100, verbose=True)

print 'Training the word2vec model...'
model = word2vec.load(BIN_PATH)
print model.vocab
print model.vectors.shape
print model['dog'][:10]

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
