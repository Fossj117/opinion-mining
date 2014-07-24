"""
This file reads in the following Yelp datasets:

- review data set
- business data set
- user data set

It then merges the two datasets and retains only Restaurants
that have a large number of reviews. It then writes the resulting
DataFrame to disk for later consumption
"""

import json
import pandas as pd

PATH = '/Users/jeff/Zipfian/opinion-mining/data/yelp_phoenix_academic_dataset_2/'

def read_from_json(fpath):
	"""
	INPUT: string (file path)
	OUTPUT: pandas DataFrame
	"""

	print "Reading data from %s ..." % fpath
	with open(fpath, 'r') as f:
		df = pd.DataFrame([json.loads(r) for r in f.readlines()])

	print "Done."
	return df

#if __name__ == "__main__":

###################################################
# GLOBALS #########################################
###################################################

NUM_REVIEW_THRESH = 300 
OUT_FNAME = '/Users/jeff/Zipfian/opinion-mining/data/high_review_restaurants.csv'

###################################################
# PROCESS BUSINESS DATA FRAME #####################
###################################################

# read in the raw data
business_path = PATH + 'yelp_academic_dataset_business.json'
business_df = read_from_json(business_path)

# only keep necessary columns
keeps = ['name', 'attributes', 'stars', 'categories', 'review_count', 'business_id']
business_df = business_df[keeps]

# clean json
business_df.categories = business_df.categories.apply(lambda categories: set(categories))

# keep only restaurants
restaurant_df = business_df[business_df.categories.apply(
					lambda categories: 'Restaurants' in categories)].copy()
del business_df

# keep only restaurants with many reviews
restaurant_df = restaurant_df[restaurant_df.review_count > NUM_REVIEW_THRESH].copy()

# rename a column
restaurant_df['rest_overall_stars'] = restaurant_df['stars']
del restaurant_df['stars']

# Clean up the categories column for later usage. 
def clean_categories(cat):
	"""
	Function to clean up the categories column
	in 'business' data frame for later use. 
	"""
	return "<CAT>".join([c for c in cat])

restaurant_df['categories'] = restaurant_df.categories.apply(clean_categories)

# Clean the attribute column for later usage
def clean_attribs(attrib):
	"""	
	Function to encode the ambiance data for later use. 
	"""

	ambiance = attrib['Ambience']

	# keep list of ambiance attributes that apply to this restaurant
	which_ambs = [k for k,v in ambiance.iteritems() if v] 
	return "<AMB>".join(which_ambs)

restaurant_df['ambiance'] = restaurant_df.attributes.apply(clean_attribs)
del restaurant_df['attributes']


###################################################
# PROCESS USERS DATA FRAME ########################
###################################################

user_path = PATH + 'yelp_academic_dataset_user.json'
user_df = read_from_json(user_path)

keeps = ['user_id', 'average_stars', 'name']
user_df = user_df[keeps]

keeps['user_avg_stars'] = user_df['average_stars']
del user_df['average_stars']

###################################################
# PROCESS REVIEWS DATA FRAME ######################
###################################################

review_path = PATH + 'yelp_academic_dataset_review.json'
review_df = read_from_json(review_path)

# only keep necessary columns
keeps = ['business_id', 'review_id', 'stars', 'text', 'user_id']
review_df = review_df[keeps]

# rename stars column
review_df['rev_stars'] = review_df['stars']
del review_df['stars']

###################################################
# MERGE THE DATA FRAMES ###########################
###################################################

# MERGE review and restaurant dfs
review_restaurant = review_df.merge(restaurant_df, on='business_id', how='inner')

# merge in the user info
review_restaurant_user = review_restaurant.merge(user_df, on='user_id', how='left')

# Write to csv
review_restaurant_user.to_csv(OUT_FNAME, encoding='utf-8')




