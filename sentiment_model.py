import os
import pandas as pd

PATH_TO_SENT = "/Users/jeff/Projects/yelp_opinion_mining/data/Sentiment/" # hand-tagged training data
PATH_TO_YELP = '/Users/jeff/Projects/yelp_opinion_mining/data/yelp_data/raw/yelp_academic_dataset_review.json'

train_fnames = [fname for fname in os.listdir(PATH_TO_SENT) if fname.startswith("Training")]

# Load data and fix columns

print "Reading in the training data..."
train_dfs = [pd.read_csv(PATH_TO_SENT+fname) for fname in train_fnames]
for df in train_dfs:
    df.columns = ['review_id', 'sentence', 'sentiment'] #clean up column names for merging

# merge all the data frames

print "Mergin' data"
base_df = train_dfs.pop()
for remaining_df in train_dfs:
    base_df = base_df.append(remaining_df, ignore_index=True)

# fix stray value
base_df.sentiment[base_df.sentiment=='Neutral'] = 'Negative'

#### Read in the Yelp Data ####
print "Reading yelp data"
processed_df = pd.read_csv('/Users/jeff/Projects/yelp_opinion_mining/data/yelp_data/processed.csv')

# keep only what's needed
keeps =['business_id', 'review_id', 'user_id', 'review_stars', 'user_avg_stars']
processed_df = processed_df[keeps]

# Merge the two data frames
print "Mergin' data frames"
final_df = base_df.merge(processed_df, how='left', on='review_id')

# drop couple unmatched values
final_df = final_df[~final_df.business_id.isnull()]

# FEATURIZE
import sys
sys.path.append('/Users/jeff/Projects/yelp_opinion_mining')

from classes.sentence import Sentence

print "Featurizing the data frame (may take a while)"
featurized_df = pd.DataFrame([Sentence(sent).compute_features() for sent in final_df.sentence])
featurized_df['review_stars'] = final_df.review_stars
featurized_df['sentiment'] = final_df.sentiment

featurized_df = featurized_df[~featurized_df.sentiment.isnull()]
print "Done."

featurized_df.sentiment[featurized_df.sentiment=='Positive'] = 1
featurized_df.sentiment[featurized_df.sentiment=='Negative'] = -1
featurized_df.sentiment[featurized_df.sentiment=='Objective'] = 0

#y = featurized_df['sentiment'].values.astype(int)
#X = featurized_df.drop(['sentiment'], axis=1).values

senti_df = featurized_df[featurized_df.sentiment!=0]

y = senti_df.sentiment.values.astype(int)
X = senti_df.drop(['sentiment'], axis=1).values

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2)

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(class_weight='auto')

lr.fit(X_train, y_train)

# predict probabilistically
test_probas = lr.predict_proba(X_test)

def plot_roc_curve(y_true, y_pred_probas):
	import pylab as pl
	from sklearn.metrics import roc_curve, auc

	fpr, tpr, thresholds = roc_curve(y_test, y_pred_probas[:, 1])
	roc_auc = auc(fpr, tpr)

	# Plot ROC curve
	pl.clf()
	pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
	pl.plot([0, 1], [0, 1], 'k--')
	pl.xlim([0.0, 1.0])
	pl.ylim([0.0, 1.0])
	pl.xlabel('False Positive Rate')
	pl.ylabel('True Positive Rate')
	pl.title('Receiver operating characteristic example')
	pl.legend(loc="lower right")
	pl.show()










