import preprocess
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd
from sklearn.svm import SVC

# LOAD THE DATA AFTER BOW
# sentences, target = preprocess.bow('Dataset/classify_data.txt')
file = pd.read_csv('Dataset/nlapi_classify.txt', delimiter='\t')
sentences = file['text']
target = file['class']

# VECTORIZE THE TEXT
# vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 1000)
vectorizer = TfidfVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 1000)
features = vectorizer.fit_transform(sentences)
# vocab = vectorizer.get_feature_names()
# print(vocab)
features = features.toarray()


# TO SAVE THE FEATURES AND TARGET AS A CSV.
savedata = np.hstack((features, target.values.reshape(-1, 1)))
print("savedata shape:"+str(savedata.shape))
# np.savetxt('data.csv', savedata, delimiter=',')


# TRAIN AND TEST SPLIT
train_features, test_features, train_target, test_target = train_test_split(features, target, train_size=0.8, random_state=42)
# print(train_features.shape, test_features.shape)


# USING MULTIPLE CLASSIFIERS FROM SKLEARN
# classifier = RandomForestClassifier(random_state=0)
classifier = LogisticRegression()
# classifier = SVC(kernel = 'sigmoid')
# classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100, 20), random_state=1)
# classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42)
print("Using all the features")
classifier = classifier.fit(train_features, train_target)
test_predict = classifier.predict(test_features)
scores = cross_val_score(classifier, features, target, cv=5)
print("Cross val scores"+str(scores))
print("Confusion Matrix:")
print(confusion_matrix(test_target, test_predict))
print("Classification Report:")
print(classification_report(test_target, test_predict))
print("Accuracy:")
print(accuracy_score(test_target, test_predict))
# print(classifier.coef_)


# SELECTING TOP N FEATURES USING LOGISTIC REGRESSION COEFFICIENTS
n = 800
print("Using top"+str(n)+" features and RandomForestClassifier")
arr = classifier.coef_
idx = np.argpartition(arr[0], -n)[-n:]
print(arr.shape, idx.shape)
print(len(idx))
train_features = train_features[:, idx]
test_features = test_features[:, idx]
features = features[:, idx]
print(train_features.shape)

# USING SOME FEATURE SELECTION METHODS FROM SKLEARN
# train_features = SelectKBest(chi2, k=2).fit_transform(train_features, train_target)
# test_features = SelectKBest(chi2, k=2).fit_transform(test_features, test_target)


# USING MULTIPLE CLASSIFIERS FROM SKLEARN
# classifier = RandomForestClassifier(random_state=0)
# classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42)
# classifier = LogisticRegression()
classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10, 30), random_state=1)
classifier = classifier.fit(train_features, train_target)
test_predict = classifier.predict(test_features)
scores = cross_val_score(classifier, features, target, cv=5)
print("Cross val scores"+str(scores))
print("Confusion Matrix:")
print(confusion_matrix(test_target, test_predict))
print("Classification Report:")
print(classification_report(test_target, test_predict))
print("Accuracy:")
print(accuracy_score(test_target, test_predict))





