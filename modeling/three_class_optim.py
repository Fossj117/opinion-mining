from __future__ import division

import pandas as pd
import numpy as np

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedKFold, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from pprint import pprint
from time import time

print "Reading data..."
featurized_df = pd.read_csv("featurized.csv")

y = featurized_df.sentiment.values.astype(int)
X = featurized_df.drop(['sentiment', 'opinionated'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# scaler = StandardScaler()

# pipeline = Pipeline([('scaler', StandardScaler()),
# 					 	  ('clf', SVC(class_weight='auto'))
# 						])

# parameters = [{'clf__kernel': ['rbf'], 'clf__gamma': [1000, 100, 10, 1, 1e-2, 1e-3, 1e-4],'clf__C': [0.001, .01, 1, 10, 100, 1000]},
# 			  {'clf__kernel': ['linear'], 'clf__C': [0.01, .01, 1, 10, 100, 1000]}]

#parameters = {'n_estimators':[10,100,500,1000], 'criterion':['gini', 'entropy'], 'max_features':['auto', 0.2, 0.1], 'max_depth': [3,10, 20, None]}

#score = 'accuracy'

# grid_search = GridSearchCV(RandomForestClassifier(n_jobs=-1), parameters, n_jobs = -1, verbose=.5, scoring=score)

# # run the grid search
#grid_search.fit(X_train, y_train)
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# print "Best opinionated params found:"
# print grid_search.best_estimator_
# print ''
# print 'Grid scores on train set:'
# for params, mean_score, scores in grid_search.grid_scores_:
# 	print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std()/2, params)
# print ""
# print "Opinionated classification report:"

#y_true, y_pred = y_test, grid_search.predict(X_test)
y_true, y_pred = y_test, gnb.predict(X_test)

print classification_report(y_true, y_pred)
