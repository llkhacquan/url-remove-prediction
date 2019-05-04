import numpy as np
import pandas as pd
import sys
import os

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn import tree, preprocessing
from sklearn import svm
from subprocess import call
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

if len(sys.argv) > 1:
    data_file = sys.argv[1]
else:
    logging.error(
        'usage: python3 tree.py <data-feature-file> [prediction_output_file]')
    exit(-1)
logging.info('Using feature file ' + data_file)

if len(sys.argv) > 2:
    host = sys.argv[2]
else:
    logging.error(
        'usage: python3 tree.py <data-feature-file> [prediction_output_file]')
    exit(-1)
data = pd.read_csv(data_file, sep=' ', header=None)
print("Dataset length", len(data))
print("Dataset shape", data.shape)
print("Data example:")
print(data.head())

X = data.values[:, 1:]
Y = data.values[:, 0].astype('int')

test_size = 1 - min(100000/len(data), 0.5)
print("Test size =", test_size, "(", len(data)*test_size, ")")
print("Training size =", 1-test_size, "(", len(data)*(1-test_size), ")")

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=test_size)

clf = DecisionTreeClassifier()
logging.info("start training")
clf.fit(X_train[:, 2:], y_train)
logging.info("done training")

score = clf.score(X_test[:, 2:], y_test)
print("score", score)

y_pred = clf.predict(X_test[:, 2:])
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

if len(sys.argv) > 2:
    logging.info("Extract predicted result to %s", (sys.argv[2]))
    dummy_data1 = [y_pred, y_test, X_test[:, 0]]
    df1 = pd.DataFrame(dummy_data1).transpose()
    df1.to_csv(sys.argv[2], sep=' ', header=None, index=False)

logging.info("Done")
