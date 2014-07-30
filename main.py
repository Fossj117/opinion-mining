import json
import time
import pandas as pd

from pymongo import MongoClient
from classes.business import Business

def get_reviews_for_business(bus_id, df):
	"""
	INPUT: business id, pandas DataFrame
	OUTPUT: Series with only texts
	
	For a given business id, return the review_id and 
	text of all reviews for that business. 
	"""
	return df[df.business_id==bus_id]

def read_data():
	"""
	INPUT: None
	OUTPUT: pandas data frame from file
	"""
	return pd.read_csv('./raw_data/yelp_data/processed.csv')

def main(): 

	client = MongoClient()
	db = client.yelptest2
	summaries_coll = db.summaries	

	print "Loading data..."
	df = read_data()
	bus_ids = df.business_id.unique()[21:]

	for bus_id in bus_ids:

		print "Working on biz_id %s" % bus_id
		start = time.time()

		biz = Business(get_reviews_for_business(bus_id,df))
		summary = biz.aspect_based_summary()
		
		summaries_coll.insert(summary)

		print "Inserted summary for %s into Mongo" % biz.business_name

		elapsed = time.time() - start
		print "Time elapsed: %d" % elapsed


if __name__ == "__main__":
	main()
	# import time

	# OUTFILE = "test_summary.json"

	# print "Loading data..."
	# df = read_data()
	# bus_id = df.business_id.iloc[4000]

	# start = time.time()
	# biz = Business(get_reviews_for_business(bus_id, df))
	# summary = biz.aspect_based_summary()

	# with open(OUTFILE, 'w') as f:
	# 	f.write(json.dumps(summary))

	# elapsed = time.time() - start
	# print "Time elapsed: %d" % elapsed


