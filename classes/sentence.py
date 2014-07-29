import nltk
import numpy as np

from nltk.stem.wordnet import WordNetLemmatizer

from transformers.tokenizers import MyPottsTokenizer
from transformers.featurizers import MetaFeaturizer, SubjFeaturizer, LiuFeaturizer
from transformers.asp_extractors import SentenceAspectExtractor

class Sentence(object):
	"""
	Class corresponding to a sentence in a review. Stores/manages word tokenization,
	part of speech (POS)tagging and lemmatization as well as some components
	of the final analysis such as aspect extraction. 
	"""

	# Tokenizer for converting a raw string (sentence) to a list of strings (words)
	WORD_TOKENIZER = MyPottsTokenizer(preserve_case=False)
	
	#STANFORD_POS_TAGGER = POSTagger(
	#			'/Users/jeff/Zipfian/opinion-mining/references/resources/stanford-pos/stanford-postagger-2014-06-16/models/english-bidirectional-distsim.tagger', 
	#           '/Users/jeff/Zipfian/opinion-mining/references/resources/stanford-pos/stanford-postagger-2014-06-16/stanford-postagger.jar')

	# Lemmatizer
	LEMMATIZER = WordNetLemmatizer()

	# Featurizer
	FEATURIZER = MetaFeaturizer([SubjFeaturizer(), LiuFeaturizer()]) #combine two featurizer objects

	# Aspect Extractor
	ASP_EXTRACTOR = SentenceAspectExtractor()

	def __init__(self, raw, review=None):
		"""
		INPUT: string (raw text of sentence), (optional) Review object

		Stores raw sentence in attribute and performs/stores
		tokenization and POS tagging via class-variable tokenizer/tagger. 
		"""
		
		self.raw = raw #string
		self.tokenized = self.word_tokenize(raw) #list of strings
		self.pos_tagged = self.pos_tag(self.tokenized) #list of tuples
		self.lemmatized = self.lemmatize(self.pos_tagged) #list of tuples

		if review: #if passed, store a reference to the review this came from
			self.review = review
			self.stars = self.review.stars # star pointer to number of stars (for featurization)

		# compute and store features for this sentence
		#self.features = self.compute_features()

		# compute and store aspects for this sentence
		self.aspects = self.compute_aspects()

	def word_tokenize(self, raw):
		"""
		INPUT: Sentence, string (raw text of a sentence)
		OUTPUT: List of strings (words in sentence)

		Tokenizes a sentence into a list of words. 
		"""

		return Sentence.WORD_TOKENIZER.tokenize(raw)

	def pos_tag(self, tokenized_sent):
		"""
		INPUT: List of strings (tokenized sentence)
		OUTPUT: List of tuples of form: (STRING, POS)
		
		Given a tokenized sentence, return 
		a list of tuples of form (token, POS)
		where POS is the part of speech of token using
		the standard NLTK POS tagger. 
		"""

		# Using Stanford tagger: 
		#return Sentence.STANFORD_POS_TAGGER.tag(tokenized_sent)
		return nltk.pos_tag(tokenized_sent)

	def lemmatize(self, pos_tagged_sent):
		"""
		INPUT: List of tuples (word, POS)
		OUTPUT: List of tuples (lemma, POS)

		Given a POS tagged sentence, use wordnet to lemmatize it. 
		"""

		lemmatized_sent = []

		# Logic to use POS tag if possible
		for wrd, pos in pos_tagged_sent:
			try: 
				lemmatized_sent.append((Sentence.LEMMATIZER.lemmatize(wrd, pos), pos))
			except KeyError:
				lemmatized_sent.append((Sentence.LEMMATIZER.lemmatize(wrd), pos))

		return lemmatized_sent

	def get_features(self, asarray = False):
		"""
		INPUT: Sentence
		OUTPUT: dict mapping string to ints/floats
		
		Returns an (ordered) feature dict for this Sentence
		"""

		if not hasattr(self, 'features'):
			self.features = Sentence.FEATURIZER.featurize(self)

		if not asarray:
			return self.features

		else:
			return np.array([val for _, val in self.features.iteritems()])

	def compute_aspects(self):
		"""
		INPUT: Sentence
		OUTPUT: list of lists of strings (i.e. list of aspects)
		"""
		return Sentence.ASP_EXTRACTOR.get_sent_aspects(self)

	def has_aspect(self, asp_string):
		"""
		INPUT: Sentence, string (aspect)
		OUTPUT: boolean
		"""

		# re-tokenize the aspect
		asp_toks = asp_string.split(" ")

		# return true if all the aspect tokens are in this sentence 
		return all([tok in self.tokenized for tok in asp_toks])

	def encode(self):
		"""
		INPUT: Sentence
		OUTPUT: dict of this sentence's data

		Encodes this sentence and associated metadata
		to insert into database. 
		"""
		return {'text': self.raw,
				'user': self.review.user_name
				}

	def __str__(self):
		"""
		INPUT: Sentence
		OUTPUT: string

		Return a string representation of this sentence (i.e. raw text of the sentence)
		"""
		return self.raw




