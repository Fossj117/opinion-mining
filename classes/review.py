import nltk
from sentence import Sentence

class Review(object):
	"""
	Class to store metadata about a particular review (e.g. who was the reviewer,
	how many stars did they give, etc.). Also manages sentence tokenization and 
	creates a list of sentence objects upon initialization. Iterating over a Review 
	object iterates over the constituent sentence objects. 
	"""

	# Tokenizer for converting a review to a list of sentences. 
	SENT_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')

	def __init__(self, review_dict, business=None):
		"""
		INPUT: dict corresponding to one row of pd DataFrame of reviews (data for one review) 

		- Maps metadata to class attributes. 
		- Converts raw text into a list of sentences w/tokenizer. 
		"""

		# Store review-level metadata
		self.review_id = review_dict['review_id'] #string
		self.user_id = review_dict['user_id'] #string
		self.user_name = review_dict['user_name'] #string
		self.stars = int(review_dict['review_stars']) #int
		self.text = review_dict['text']	#string	

		# if passed, store reference to business this review is about
		if business:
			self.business = business

		# Create the list of sentences for this review
		self.sentences = self.sentence_tokenize(self.text)

	def sentence_tokenize(self, review_text):
		"""
		INPUT: String (full raw text of review)
		OUTPUT: List of Sentence objects

		Convert the raw text of a review to a list of sentence objects. 
		"""	
		return [Sentence(sent, review=self) for sent in  Review.SENT_TOKENIZER.tokenize(review_text)]

	def __iter__(self):
		"""
		INPUT: Review object
		OUTPUT: Iterator over the sentences in this review. 

		Returns an iterator over the sentences in this review. 
		"""
		return self.sentences.__iter__()

	def __str__(self):
		"""
		INPUT: Review
		OUTPUT: string

		Return a string representation of this review (i.e. full text of the review)
		"""
		return self.text