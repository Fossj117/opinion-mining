from __future__ import division
from tokenizers import NegationSuffixAdder
from collections import OrderedDict
import os

class BaseFeaturizer(object):

	def __init__(self):
		pass

	def featurize(self, sent):
		"""
		Return a feature dict for this Sentence
		"""
		pass

class MetaFeaturizer(BaseFeaturizer):

	def __init__(self, featurizer_list):
		"""
		INPUT: MetaFeaturizer, list of BaseFeaturizer objs
		
		Combines a number of featurizer objects
		"""

		self.featurizer_list = featurizer_list

	def featurize(self, sent):
		"""
		INPUT: MetaFeaturizer, Sentence
		OUPUT: dict

		Returns combined feature dict for this sentence
		based on constituent featurizers
		"""

		features = {}

		for featurizer in self.featurizer_list:

			features = dict(features.items() + featurizer.featurize(sent).items())

		features['review_stars'] = sent.stars # add one last feature

		return OrderedDict(sorted(features.items())) # need to preserve order. 

class SubjFeaturizer(BaseFeaturizer):
	
	PATH_TO_LEXICON = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'files/subjclueslen1-HLTEMNLP05.tff')) 

	TAG_MAP = {'NN': 'noun',
			   'NNS': 'noun',
			   'NNP': 'noun',
			   'JJ': 'adj',
			   'JJR': 'adj',
			   'JJS': 'adj',
			   'RB': 'adverb',
			   'RBR': 'adverb',
			   'RBS': 'adverb',
			   'VB': 'verb',
			   'VBD': 'verb',
			   'VBG': 'verb',
			   'VBN': 'verb',
			   'VBP': 'verb',
			   'VBZ': 'verb'}

	def __init__(self):

		self.lex_dict = self.read_lexicon(SubjFeaturizer.PATH_TO_LEXICON)

	def read_lexicon(self, path):
		"""
		Read the lexicon from file
		"""

		with open(path, 'r') as f: 
			parsed = [self.parse_line(line) for line in f.readlines()]

		lex_dict = {}

		for wrd in parsed: 
			lex_dict = dict(lex_dict.items() + wrd.items())

		return lex_dict

	def parse_line(self, raw_line):
		"""
		INPUT: string
		OUTPUT: dictionary of this line's attributes

		Parses one line of the subjectivity lexicon
		"""
		line = raw_line.strip().split(" ")
		out = dict([o.split("=") for o in line])

		the_word = out['word1']
		the_pos = out['pos1']
		del out['word1']
		del out['pos1']

		return {(the_word, the_pos):out}

	def featurize(self, sent):
		"""
		INPUT: SubjFeaturizer, Sentence
		OUTPUT: dict

		"""

		n_weaksubj = 0
		n_strongsubj = 0
		# n_positive = 0
		# n_negative = 0

		n_wrds = len(sent.tokenized)

		for wrd, pos in sent.lemmatized: 

			info = self.get_from_lexicon(wrd, pos)

			if info: 

				subj_type = info['type']
				polarity = info['priorpolarity']

				if subj_type=='strongsubj':
					n_strongsubj += 1
				elif subj_type=='weaksubj':
					n_weaksubj += 1

				# if polarity=='negative':
				# 	n_negative +=1
				# elif polarity=='positive':
				# 	n_positive +=1

		features = {}
		features['frac_strongsubj'] = n_strongsubj / n_wrds
		features['frac_weaksubj'] = n_weaksubj / n_wrds
		features['total_subj'] = n_strongsubj + n_weaksubj

		return features

	def get_from_lexicon(self, wrd, pos):
		"""
		INPUT: string, string
		OUTPUT: dict or None

		See if this word/pos combo is in the lexicon.
		If it is, return the info about it. If not, return None. 
		"""

		info = None

		if (wrd, self.map_pos(pos)) in self.lex_dict:
		
			info = self.lex_dict[(wrd, self.map_pos(pos))]

		elif (wrd, 'anypos') in self.lex_dict:
		
			info = self.lex_dict[(wrd, 'anypos')]

		return info


	def map_pos(self, pos_tag):
		"""
		Map an NLTK pos tag to something compatible with the subjectivity lexicon
		"""

		if pos_tag in SubjFeaturizer.TAG_MAP:
			return SubjFeaturizer.TAG_MAP[pos_tag]
		else: 
			return 'N/A'


class LiuFeaturizer(BaseFeaturizer):
	"""
	Class for scoring sentences using Bing Liu's Opinion Lexicon. 

	Source:

	Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
       Proceedings of the ACM SIGKDD International Conference on Knowledge 
       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
       Washington, USA,

    Download lexicon at: http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar
	"""

	PATH_TO_LEXICONS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'files'))
	NEG_SUFFIXER = NegationSuffixAdder()

	def __init__(self):
		"""
		Read in the lexicons. 
		"""

		pos_path = self.PATH_TO_LEXICONS + "/positive-words.txt"
		neg_path = self.PATH_TO_LEXICONS + "/negative-words.txt"

		self.pos_lex = self.read_lexicon(pos_path)
		self.neg_lex = self.read_lexicon(neg_path)

	def read_lexicon(self, path):
		'''
		INPUT: LiuFeaturizer, string (path)
		OUTPUT: set of strings

		Takes path to Liu lexicon and 
		returns set containing the full 
		content of the lexicon. 
		'''

		start_read = False
		lexicon = set() # set for quick look-up

		with open(path, 'r') as f: 
			for line in f: 
				if start_read:
					lexicon.add(line.strip())
				if line.strip() == "":
					start_read = True
		return lexicon

	def featurize(self, sent):
		'''
		INPUT: LiuFeaturizer, Sentence
		OUTPUT: dict

		Get complete feature set for a sentence. 
		'''

		# get various types of features
		lex_feats = self.get_lex_feats(sent)
		pos_feats = self.get_pos_feats(sent)

		# return all features
		return dict(lex_feats.items() + pos_feats.items())

	def get_pos_feats(self, sent):
		'''
		INPUT: LiuFeaturizer, Sentence
		OUTPUT: dict

		Get pos-based feature-set:

		- n_pos : number of words of this part-of-speech (pos)
		- frac_pos : fraction of words in sentence of this part-of-speech (pos)

		'''

		# pos tag sets
		nouns = {'NN', 'NNS', 'NNP', 'NNPS'}
		adjs = {'JJ', 'JJR', 'JJS'}
		advbs = {'RB', 'RBR', 'RBS'}
		pronouns = {'PRP', 'PRP$'}

		# extract pos tags for this sentence
		tags = [pos for _, pos in sent.pos_tagged]

		# number of words
		n_wrds = len(sent.pos_tagged)

		# count number of various parts of speech
		n_nouns = len([pos for pos in tags if pos in nouns])
		n_adjs = len([pos for pos in tags if pos in adjs])
		n_advbs = len([pos for pos in tags if pos in advbs])

		# normalize by sentence length
		frac_nouns = n_nouns / n_wrds
		frac_adjs = n_adjs / n_wrds
		frac_advbs = n_advbs / n_wrds

		# binary variables for presence/absence of indicative POS tags
		has_pronoun = 1 if any([tag in pronouns for tag in tags]) else 0
		has_cardinal = 1 if any([tag in pronouns for tag in tags]) else 0 
		has_modal = 1 if any([tag=='MD' and wrd!='will' for wrd, tag in sent.pos_tagged]) else 0

		# return feature dict
		return {'n_nouns': n_nouns,
				'n_adjs': n_adjs,
				'n_advbs': n_advbs,
				'frac_nouns': frac_nouns,
				'frac_adjs': frac_adjs,
				'frac_advbs': frac_advbs,
				'has_pronoun': has_pronoun,
				'has_cardinal': has_cardinal,
				'has_modal': has_modal
				}

	def get_lex_feats(self, sent):
		'''
		INPUT: LiuFeaturizer, Sentence
		OUTPUT: dict

		Get the lexically-based feature-set:
		
		- raw: # of pos words - # of neg words (negation-adjusted)
		- frac_pos: fraction of sentence that is positive words
		- frac_neg: fraction of sentence that is negative words

		'''

		# get tokenized 
		tokens = LiuFeaturizer.NEG_SUFFIXER.add_negation_suffixes(sent.tokenized)

		sent_len = len(tokens)
		assert sent_len > 0, "Can't featurize sentence with no tokens"

		num_pos = 0
		num_neg = 0

		for tok in tokens:

			# if inside a negation block, add to opposite tally
			if tok.endswith("_NEG"): 
				if tok.strip("_NEG") in self.pos_lex:
					num_neg+=1 
				elif tok.strip("_NEG") in self.neg_lex:
					num_pos+=1
			
			# otherwise, add to normal tally
			else: 
				if tok in self.pos_lex:
					num_pos +=1
				elif tok in self.neg_lex:
					num_neg += 1

		features = {}
		features['raw'] = num_pos - num_neg		
		features['frac_pos'] = num_pos / sent_len
		features['frac_neg'] = num_neg / sent_len

		return features



