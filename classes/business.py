from __future__ import division

from review import Review
from collections import Counter
from operator import itemgetter

from transformers.sentiment import SentimentModel, OpinionModel

class Business(object):
	"""
	Class to store the full corpus of reviews and meta-data 
	about a particular Business. Upon creation, a Business
	generates a list of constituent Review objects. Iterating over a 
	Business iterates over these Review objects. 
	"""

	SENTIMENT_MODEL = SentimentModel()
	OPINION_MODEL = OpinionModel()

	def __init__(self, review_df):
		"""
		INPUT: pandas DataFrame with each row a review, and columns:

			- business_id: id of the business (must be all same)
			- business_name: name of the Business
			- business_ambiance: encoded list of ambiance attributes for this business
			- business_categories: encoded list of categories for this business
			- business_overall_stars: average stars rating for this business
			- review_count: number of reviews that exist for this business

			- review_id: id of the review
			- review_stars: number of stars reviewer gave
			- text: raw text of the review

			- user_id: id of the user who made review
			- user_name: first name of the user who made review
			- user_avg_stars: average number of stars given by reviewer

		Takes raw DataFrame of reviews about a particular Business (where
		each row corresponds to a particular review of the Business, and 
			1. Stores all the metadata associated with the Business
			2. Converts the reviews (rows) into Review objects. 
		"""

		# Ensure only got data about *one* Business
		assert len(review_df.business_id.unique()) == 1, "Must pass data for a single business to Business"

		# Store business-level meta data
		self.business_id = str(review_df.business_id.iloc[0]) # string 
		self.business_name = str(review_df.business_name.iloc[0]) # string
		self.overall_stars = int(review_df.business_overall_stars.iloc[0]) # int
		self.categories = review_df.business_categories.iloc[0].split('<CAT>') #list of strings
		self.ambiance = review_df.business_ambiance.iloc[0].split('<AMB>') #list of strings

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
		OUTPUT: dict 

		Returns the final output JSON object, encoding the aspect-based
		sentiment summary for the given business, ready to be written to MongoDB.
		"""

		aspects = self.extract_aspects()
		asp_dict = dict([(aspect, self.aspect_summary(aspect)) for aspect in aspects])			

		asp_dict = self.filter_asp_dict(asp_dict) # final filtering

		return {'business_id': self.business_id,
				'business_name': self.business_name,
				'business_stars': self.overall_stars,
				'aspect_summary': asp_dict	
				}

	def extract_aspects(self, single_word_thresh=0.012, multi_word_thresh=0.003):
		"""
		INPUT:
			- Business
			- single_word_thresh : how common does a single-word aspect need to be
								   in order to get included in the summary?
			- multi_word_thresh : how common does a multi-word aspect need to be in
								  order to get included in the summary? 

		OUTPUT: list of lists of strings
			- e.g. [['pepperoni','pizza'], ['wine'], ['service']]

		Returns a list of the aspects that are most often commented on in this business 
		"""

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
		single_asps = [(asp, count) for asp, count in Counter(single_asps).most_common(30) if count/n_sents > single_word_thresh]
		multi_asps = [(asp, count) for asp, count in Counter(multi_asps).most_common(30) if count/n_sents > multi_word_thresh]

		# filter redundant single-word aspects
		single_asps = self.filter_single_asps(single_asps, multi_asps)

		# the full aspect list, sorted by frequency
		all_asps =  [asp for asp,_ in sorted(single_asps + multi_asps, key=itemgetter(1))]

		return self.filter_all_asps(all_asps)

	def aspect_summary(self, aspect):
		"""
		INPUT: business, string (aspect)
		OUTPUT: dict with keys 'pos' and 'neg' which 
		map to a list of positive sentences (strings) and
		a list of negative sentences (strings) correspondingly. 
		
		Gets summary for a *particular* aspect. 
		"""

		OPIN_THRESH = 0.7
		HARD_MIN_OPIN_THRESH = 0.6

		POS_THRESH = 0.85
		NEG_THRESH = 0.85

		# override the opinion classifier if 
		# sentiment classifier is REALLY sure. 
		SENTI_OVERRIDE_THRESHOLD = .95 

		SENTENCE_LEN_THRESHOLD = 30 # number of words

		pos_sents = []
		neg_sents = []

		aspect_sents = self.get_sents_by_aspect(aspect)

		for sent in aspect_sents:

			if len(sent.tokenized) > SENTENCE_LEN_THRESHOLD:
				continue #filter really long sentences

			prob_opin = Business.OPINION_MODEL.get_opinionated_proba(sent)
			prob_pos = Business.SENTIMENT_MODEL.get_positive_proba(sent)
			prob_neg = 1 - prob_pos

			sent_dict = sent.encode()
			sent_dict['prob_opin'] = prob_opin
			sent_dict['prob_pos'] = prob_pos
			sent_dict['prob_neg'] = prob_neg
			sent_dict['sorter'] = prob_opin*max(prob_pos, prob_neg) #used to order sentences for display

			if prob_opin > OPIN_THRESH or (max(prob_pos, prob_neg) > SENTI_OVERRIDE_THRESHOLD and prob_opin > HARD_MIN_OPIN_THRESH):

				if prob_pos > POS_THRESH:
					pos_sents.append(sent_dict)
				elif prob_neg > NEG_THRESH:
					neg_sents.append(sent_dict)

		n_sents = len(pos_sents) + len(neg_sents) if len(pos_sents) + len(neg_sents) > 0 else 1

		return {'pos': sorted(pos_sents, key=itemgetter('prob_pos'), reverse=True), # sort by confidence
				'neg': sorted(neg_sents, key=itemgetter('prob_neg'), reverse=True), # sort by confidence
				'num_pos': len(pos_sents),
				'num_neg': len(neg_sents),
				'frac_pos': len(pos_sents) / n_sents
				}

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

	def filter_asp_dict(self, asp_dict, num_valid_threshold = 5):
		"""
		INPUT: Business, aspect dictionary, int
		OUTPUT: filtered aspect dictionary

		Filters aspects that don't have enough valid sentences 
		"""
		return dict([(k, v) for k,v in asp_dict.iteritems() if v['num_pos'] > num_valid_threshold or v['num_neg'] > num_valid_threshold])

	def filter_all_asps(self, asps):
		"""
		INPUT: Business
		OUTPUT: list of strings
		"""
		# TODO if needed
		# filter aspects that are too close to the restaurant's name?
		return asps







