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

from pprint import pprint
from time import time

print "Reading data..."
featurized_df = pd.read_csv("featurized.csv")

#y = featurized_df['sentiment'].values.astype(int)
#X = featurized_df.drop(['sentiment', 'opinionated'], axis=1).values

senti = featurized_df.sentiment.values.astype(int)
opin = featurized_df.opinionated.values.astype(int)
X = featurized_df.drop(['sentiment', 'opinionated'], axis=1).values

# create the GLOBAL holdout... (PRISTINE HOLDOUT) of 20% of data
X_devel, X_holdout, senti_devel, senti_holdout, opin_devel, opin_holdout = train_test_split(X, senti, opin, test_size = 0.2, random_state=117)
print "Created global holdout of size %d" % len(X_holdout)

###### BUILDING OPINION CLASSIFIER #######
# In this section we optimize / train an 
# SVM to discriminate opinionated sentences 
# vs. non-opinionated sentences. 
##########################################

X_train_opin, X_test_opin, opin_train, opin_test = train_test_split(X_devel, opin_devel, test_size=0.2)

print "Size of opinionated train set: %d" % len(opin_train)
print "Size of opinionated test set: %d" % len(opin_test)

scaler = StandardScaler()

opin_pipeline = Pipeline([('scaler', StandardScaler()),
					 	  ('clf', SVC(class_weight='auto', probability=True))
						])

# opin_parameters = [{'clf__kernel': ['rbf'], 'clf__gamma': [100, 10, 1, 1e-2, 1e-3, 1e-4],'clf__C': [.01, 1, 10, 100, 1000]},
# 			  {'clf__kernel': ['linear'], 'clf__C': [.01, 1, 10, 100, 1000]}]

# opin_parameters = [{'clf__kernel': ['rbf'], 'clf__gamma': [1e-2, 1e-3, 1e-4],'clf__C': [.01, 1, 10, 100, 1000]},
# 			  {'clf__kernel': ['linear'], 'clf__C': [.01, 1, 10, 100, 1000]}]

opin_parameters = [{'clf__kernel': ['rbf']},
					{'clf__kernel': ['linear']}]

opin_score = 'roc_auc'

opin_grid_search = GridSearchCV(opin_pipeline, opin_parameters, n_jobs = -1, verbose=.5, scoring=opin_score)

# run the grid search
opin_grid_search.fit(X_train_opin, opin_train)

print "Best opinionated params found:"
print opin_grid_search.best_estimator_
print ''
print 'Grid scores on train set:'
for params, mean_score, scores in opin_grid_search.grid_scores_:
	print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std()/2, params)
print ""
print "Opinionated classification report:"

y_true, y_pred = opin_test, opin_grid_search.predict(X_test_opin)

print classification_report(y_true, y_pred)

best_opin = opin_grid_search.best_estimator_.fit(X_devel, opin_devel)

###### BUILDING SENTIMENT CLASSIFIER #############
# In this section we optimize / train an 
# SVM to discriminate positive sentences 
# vs. negative sentences (assuming opinionatedness)
###################################################

# Only train sentiment classifier on opinionated sentences
X_devel_senti = X_devel[senti_devel!=0, :]
senti_devel = senti_devel[senti_devel!=0]

X_train_senti, X_test_senti, senti_train, senti_test = train_test_split(X_devel_senti, senti_devel, test_size=0.2)

senti_clf = LogisticRegression(class_weight='auto')
senti_params = {'C':[0.01, 0.1, 1.0, 10.0], 'penalty': ['l1', 'l2']}
#senti_params = {'C': [1.0]}

senti_score = 'roc_auc'

senti_grid_search = GridSearchCV(senti_clf, senti_params, n_jobs = -1, verbose=.5, scoring=senti_score)

# run the grid search
senti_grid_search.fit(X_train_senti, senti_train)

print "Best sentiment params found:"
print senti_grid_search.best_estimator_
print ''
print 'Grid scores on train set:'
for params, mean_score, scores in senti_grid_search.grid_scores_:
	print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std()/2, params)
print ""
print "Sentiment classification report:"

y_true, y_pred = senti_test, senti_grid_search.predict_proba(X_test_senti)[:,-1]

print classification_report(y_true, y_pred)

best_senti = senti_grid_search.best_estimator_.fit(X_devel_senti, senti_devel)

######## EVALUATE THE FINAL MODEL ############

# X_holdout, senti_holdout

opin_predics = best_opin.predict_proba(X_holdout)[:,-1] #prob of 1
senti_predics = best_senti.predict_proba(X_holdout)[:,-1] #prob 1

temp = zip(opin_predics, senti_predics)

final_predics = []

for opin, senti in temp: 
	final_predics.append(0 if opin<=.8 else senti)

final_predics = np.array(final_predics)

print "FINAL CLASSIFICATION REPORT:"
print classification_report(senti_holdout, final_predics)























