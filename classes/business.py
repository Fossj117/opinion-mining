from __future__ import division

from review import Review
from collections import Counter
from operator import itemgetter

class Business(object):
	"""
	Class to store the full corpus of reviews and meta-data 
	about a particular Business. Upon creation, a Business
	generates a list of constituent Review objects. Iterating over a 
	Business iterates over these Review objects. 
	"""

	def __init__(self, review_df):
		"""
		INPUT: pandas DataFrame with each row a review, and columns:
			- business_id: id of the business (must be all same)
			- review_id: id of the review
			- stars: number of stars reviewer gave
			- text: raw text of the review
			- user_id: id of the user who made review
			- name: name of the Business
			- categories: set of categories for Business
			- overall_stars: overall rating of this Business
		
		Takes raw DataFrame of reviews about a particular Business (where
		each row corresponds to a particular review of the Business, and 
			1. Stores all the metadata associated with the Business
			2. Converts the reviews (rows) into Review objects. 
		"""

		# Ensure only got data about *one* Business
		assert len(review_df.business_id.unique()) == 1, "Must pass data for a single business to Business"

		# Store business-level meta data
		self.business_id = str(review_df.business_id.iloc[0]) # string 
		self.business_name = str(review_df.name.iloc[0]) # string
		self.overall_stars = int(review_df.rest_overall_stars.iloc[0]) # int
		#self.categories = self.parse_categories(review_df.categories.iloc[0]) # TODO

		# Create the list of Reviews for this Business
		self.reviews = [Review(dict(review_row), business=self) for _,review_row in review_df.iterrows()]

	def __iter__(self):
		"""
		INPUT: Business
		OUTPUT: an iterator over the set of reviews for this Business. 
		
		Allows the use of "do_something(review) for review in Business"
		"""
		return self.reviews.__iter__()

	def __str__(self):
		"""
		INPUT: Business
		OUTPUT: string

		Return a string representation of this Business (i.e. the name of the Business)
		"""
		return self.business_name

	## ANALYSIS METHODS ##

	def aspect_based_summary(self):
		"""
		INPUT: Business
		OUTPUT: Complicated JSON object thing. 

		Returns the final output JSON object, encoding the aspect-based
		sentiment summary for the given business, ready to be written to MongoDB.
		"""
		# TODO

		aspects = self.extract_aspects()
		return dict([(aspect, self.aspect_summary(aspect)) for aspect in aspects])			

	def extract_aspects(self):
		"""
		INPUT: business
		OUTPUT: list of lists of strings
			- e.g. [['pepperoni','pizza'], ['wine'], ['service']]

		Returns a list of the aspects that are 
		most often commented on in this business 
		"""

		# TUNING PARAMS
		SINGLE_WORD_THRESH = 0.012
		MULTI_WORD_THRESH = 0.003

		asp_sents = [sent.aspects for rev in self for sent in rev]
		n_sents = float(len(asp_sents))

		single_asps = [] #list of lists (aspects)
		multi_asps = [] #list of lists

		# create single-word and multi-word aspect lists
		for sent in asp_sents: 
			for asp in sent:
				if len(asp) == 1:
					single_asps.append(" ".join(asp))
				elif len(asp) > 1:
					multi_asps.append(" ".join(asp))
				else:
					continue # shouldn't happen

		# Get sufficiently-common single- and multi-word aspects
		single_asps = [(asp, count) for asp, count in Counter(single_asps).most_common(30) if count/n_sents > SINGLE_WORD_THRESH]
		multi_asps = [(asp, count) for asp, count in Counter(multi_asps).most_common(30) if count/n_sents > MULTI_WORD_THRESH]

		# filter redundant single-word aspects
		single_asps = self.filter_single_asps(single_asps, multi_asps)

		# return the full aspect list, sorted by frequency
		return [asp for asp,_ in sorted(single_asps + multi_asps, key=itemgetter(1))]

	def aspect_summary(self, aspect):
		"""
		INPUT: business, string (aspect)
		OUTPUT: dict with keys 'pos' and 'neg' which 
		map to a list of positive sentences (strings) and
		a list of negative sentences (strings) correspondingly. 
		"""

		pos_sents = []
		neg_sents = []

		for sent in self.get_sents_by_aspect(aspect):
			if sent.get_sentiment() > 0:
				pos_sents.append(sent.raw)
			else: 
				neg_sents.append(sent.raw)

		return {'pos': pos_sents,
				'neg': neg_sents }

	def get_sents_by_aspect(self, aspect):
		"""
		INPUT: 
		OUTPUT: List of Sentence objects
		"""
		return [sent for review in self for sent in review if sent.has_aspect(aspect)] 

	def filter_single_asps(self, single_asps, multi_asps):
		"""
		INPUT: list of strings (aspects)
		OUTPUT: list of strings (filtered aspects)

		Filter out those one-word aspects that are subsumed in a multi-word aspect. E.g. 
		filter out "chicken" if "pesto chicken" is a multi-word aspect. 
		"""

		return [(sing_asp, count) for sing_asp, count in single_asps if not any([sing_asp in mult_asp for mult_asp, _ in multi_asps])]




