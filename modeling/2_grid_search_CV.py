"""
2_grid_search_CV

This file:
- Reads in the development set
- Runs a grid search for:
	- Best OPINION MODEL (opinionated vs. not opinionated)
	- Best SENTIMENT MODEL (positive vs. negative, assuming opinionated)

In practice, I have been running this using Domino Data Labs, which 

"""
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV

from sklearn.metrics import classification_report, roc_curve, auc

import pylab as pl
import pandas as pd
import pickle

def print_grid_search_results(grid_search, name):
	"""
	Print out summary of the grid search
	"""

	print "Best params found for %s:" % name
	print grid_search.best_estimator_
	print ''
	print 'Grid scores on train set:'
	for params, mean_score, scores in grid_search.grid_scores_:
		print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std()/2, params)
	print ""

def print_classifier_results(y_true, y_pred, y_proba, name):
	"""
	Generate standard metrics for binary classification evaluation:
	- classification_report
	- ROC plot
	"""

	print "%s Classification Report:" % name
	print classification_report(y_true, y_pred)
	print ""

	fpr, tpr, thresholds = roc_curve(y_true, y_proba)
	roc_auc = auc(fpr, tpr)
	print "Area under the ROC curve: %f" % roc_auc

	pl.clf()
	pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
	pl.plot([0, 1], [0, 1], 'k--')
	pl.xlim([0.0, 1.0])
	pl.ylim([0.0, 1.0])
	pl.xlabel('False Positive Rate')
	pl.ylabel('True Positive Rate')
	pl.title('ROC Curve: ' + name)
	pl.legend(loc="lower right")
	pl.savefig("./results/"+name+'.png', format='png')

def run_opinion_grid_search(full_df):
	"""
	Runs SVM grid search for OPINION MODEL
	"""
	name = "Opinion_Model"

	y = full_df.opinionated.astype(int)
	X = full_df.drop(['sentiment', 'opinionated'], axis=1).values

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=117)

	print "%s model train size: %d" % (name, len(y_train))
	print "%s model test size: %d" % (name, len(y_test))

	scaler = StandardScaler()

	pipeline = Pipeline([('scaler', StandardScaler()),
						 	  ('clf', SVC(class_weight='auto', probability=True))
							])

	params = [{'clf__kernel': ['rbf'], 'clf__gamma': [100, 10, 1, 1e-2, 1e-3, 1e-4],'clf__C': [.01, 1, 10, 100, 1000]},
	 			  {'clf__kernel': ['linear'], 'clf__C': [.01, 1, 10, 100, 1000]}]
	# params = [{'clf__kernel': ['rbf']},
	# 		  {'clf__kernel': ['linear']}]

	grid_search = GridSearchCV(pipeline, params, n_jobs = -1, verbose=.5, scoring='roc_auc')

	# run the grid search
	grid_search.fit(X_train, y_train)

	# print results
	print_grid_search_results(grid_search, name)	

	y_true, y_pred =  y_test, grid_search.best_estimator_.predict(X_test)
	y_proba = grid_search.best_estimator_.predict_proba(X_test)[:,1]

	print_classifier_results(y_true, y_pred, y_proba, name)

	return grid_search, grid_search.best_estimator_.fit(X, y)


def run_senti_grid_search(full_df):
	"""
	Runs LogisticRegression grid search for SENTIMENT MODEL
	"""
	name = "Sentiment_Model"

	# get rid of objective rows
	only_polar = full_df[full_df.sentiment!=0].copy()

	y = only_polar.sentiment.astype(int)
	X = only_polar.drop(['sentiment', 'opinionated'], axis=1).values

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=117)

	print "%s model train size: %d" % (name, len(y_train))
	print "%s model test size: %d" % (name, len(y_test))

	clf = LogisticRegression(class_weight='auto')
	params = {'C':[0.01, 0.1, 1.0, 10.0], 'penalty': ['l1', 'l2']}
	#params = {'C': [1.0]}

	grid_search = GridSearchCV(clf, params, n_jobs = -1, verbose=.5, scoring='roc_auc')

	# run the grid search
	grid_search.fit(X_train, y_train)

	# print results
	print_grid_search_results(grid_search, name)	

	y_true, y_pred =  y_test, grid_search.best_estimator_.predict(X_test)
	y_proba = grid_search.best_estimator_.predict_proba(X_test)[:,1]

	print_classifier_results(y_true, y_pred, y_proba, name)

	return grid_search, grid_search.best_estimator_.fit(X,y)


if __name__ == "__main__":

	print "Reading data..."

	development_df = pd.read_csv("./data/featurized_development.csv") # raw data set

	print "Size of complete development set: %d" % len(development_df)
	print "Target class breakdowns:"
	print development_df.sentiment.value_counts()
	print ""
	print development_df.opinionated.value_counts()

	opin_gs, opin_best_est = run_opinion_grid_search(development_df	)

	senti_gs, senti_best_est = run_senti_grid_search(development_df)

	### STORE THE FINAL MODELS ####

	pickle.dump(opin_best_est, open("./results/final_models/opin_pred.p", 'wb'))
	pickle.dump(senti_best_est, open("./results/final_models/senti_pred.p", 'wb'))







