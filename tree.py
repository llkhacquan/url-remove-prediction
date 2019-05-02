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
    logging.error('usage: python3 tree.py <data-feature-file> <host> [svm|tree]')
    exit(-1)
logging.info('Using feature file ' + data_file)
if len(sys.argv) > 2:
    host = sys.argv[2]
else:
    logging.error('usage: python3 tree.py <data-feature-file> <host> [svm|tree]')
    exit(-1)

if len(sys.argv) > 3:
    algo = sys.argv[3]
else:
    algo = 'tree'
if algo == 'tree' or algo == 'svm':
    logging.info("Use algorithm " + algo)
else:
    logging.error(algo + ' is not a valid algorithm (use tree or svm)')
    exit(-1)

if not os.path.exists('data'):
    os.makedirs('data')

input_file = 'data/' + host + '.gz'
logging.info("Processing host: [" + host + '] data file [' + input_file + ']')
if not os.path.isfile(input_file):
    logging.info('Data does not exist, creating [' + input_file+']')
    os.system('zcat ' + data_file + ' |awk \'$3=="' + host + '"\' |gzip > data/' + host + '.gz')
else:
    logging.info('Data exists [' + input_file+']')
data = pd.read_csv(input_file, sep=' ', header=None)
print("Dataset length", len(data))
print("Dataset shape", data.shape)
print("Data example:")
print(data.head())

X = data.values[:, 3:]
Y = data.values[:, 0]
Y = Y.astype('int')

test_size = 1 - min(100000/len(data), 0.5)
print("Test size =", test_size, "(", len(data)*test_size, ")")
print("Training size =", 1-test_size, "(", len(data)*(1-test_size), ")")

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=test_size)

if algo == 'svm':
    clf = svm.SVC(gamma='scale')
else:
    clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)
print("score", score)

y_pred = clf.predict(X_test) 
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred))  