import argparse
import json
import sys

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
import pandas as pd
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
import numpy
from random import shuffle
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
import re
import preprocess  

# Vectorizing using DOC2VEC from gensim
def vectorize():    
    sentences, target = preprocess.bow('Dataset/classify_data.txt')
    # print(sentences[0])
    words = []
    for i in range(len(sentences)):
        words.append(sentences[i].split(' ')) 
    # print(words)
    class LabeledLineSentence(object):
        def __init__(self, filename):
            self.sentences = sentences
        def __iter__(self):
            for uid, line in enumerate(sentences):
                yield LabeledSentence(words=line.split(' '), tags=['SENT_%s' % uid])
        def sentences_perm(self):
            shuffle(self.sentences)
            return self.sentences
    trained_data = LabeledLineSentence(sentences)
    token_count = sum([len(words) for word in words])
    # trained_data = LabeledSentence(words, target)
    model = Doc2Vec(alpha=0.025, min_alpha=0.025)
    model.build_vocab(trained_data)
    for epoch in range(10):
        model.train(trained_data, total_examples=token_count, epochs = model.iter)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
    model.save('Dataset/classify_data_onlypos.d2v')

vectorize()


# Creating features and target from the doc2vec vectors
sentences, target = bow('Dataset/classify_data.txt')
print(sentences[1])
file = pd.read_csv('Dataset/classify_data.txt', delimiter='\t')
target = file['class']

# Loading the already saved model to increase time efficiency
model = Doc2Vec.load('Dataset/classify_data_onlypos.d2v')
features = numpy.zeros((276, 100))
for i in range(len(features)):
    features[i] = model.docvecs['SENT_'+str(i)]

# Creating test and train split for classification and using multiple classifiers from sklearn
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)
classifier = RandomForestClassifier(random_state=0)
# classifier = MLPClassifier(alpha=1)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
scores = cross_val_score(classifier, features, target, cv=10)
print("Cross val scores"+str(scores))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))
