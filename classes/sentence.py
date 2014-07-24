import nltk

from nltk.stem.wordnet import WordNetLemmatizer
from transformers.tokenizers import MyPottsTokenizer
from transformers.featurizers import LiuFeaturizer

from transformers.aspect_extraction.extractor import SentenceAspectExtractor

class Sentence(object):
	"""
	Class corresponding to a sentence in a review. Manages word tokenization
	and part of speech (POS) tagging and stores/provides access to each version 
	of the sentence via getter methods (get_raw, get_tokens, get_pos_tokens)
	"""

	# Tokenizer for converting a raw string (sentence) to a list of strings (words)
	WORD_TOKENIZER = MyPottsTokenizer(preserve_case=False)
	
	#STANFORD_POS_TAGGER = POSTagger(
	#			'/Users/jeff/Zipfian/opinion-mining/references/resources/stanford-pos/stanford-postagger-2014-06-16/models/english-bidirectional-distsim.tagger', 
	#           '/Users/jeff/Zipfian/opinion-mining/references/resources/stanford-pos/stanford-postagger-2014-06-16/stanford-postagger.jar')

	# Lemmatizer
	LEMMATIZER = WordNetLemmatizer()

	# Featurizer
	FEATURIZER = LiuFeaturizer()

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

		# compute and store features for this sentence
		self.features = self.compute_features()

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

	def compute_features(self):
		"""
		INPUT: Sentence
		OUTPUT: dict mapping string to ints
		
		Returns a feature dict for this Sentence
		"""
		return Sentence.FEATURIZER.featurize(self)

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
		try:
			return asp_string in self.raw
		except:
			return False

	def get_sentiment(self):
		"""
		INPUT: Sentence
		OUTPUT: int (sentiment score)
		"""
		# TODO
		return self.features['raw'] #temporary 

	def __str__(self):
		"""
		INPUT: Sentence
		OUTPUT: string

		Return a string representation of this sentence (i.e. raw text of the sentence)
		"""
		return self.raw