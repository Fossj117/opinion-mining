from __future__ import division

class BaseFeaturizer(object):

	def __init__(self):
		pass

	def featurize(self, Sentence):
		"""
		Return a feature dict for this Sentence
		"""
		pass

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

	PATH_TO_LEXICONS = "/Users/jeff/Zipfian/opinion-mining/data/Lexicons"

	def __init__(self):
		"""
		Read in the lexicons. 
		"""

		pos_path = self.PATH_TO_LEXICONS + "/Liu/positive-words.txt"
		neg_path = self.PATH_TO_LEXICONS + "/Liu/negative-words.txt"

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
		'''

		features = {}

		tokens = sent.tokenized

		sent_len = len(tokens)
		assert sent_len > 0, "Can't featurize sentence with no tokens"

		num_pos = sum([1 if tok in self.pos_lex else 0 for tok in tokens])
		num_neg = sum([1 if tok in self.neg_lex else 0 for tok in tokens])

		features['raw'] = num_pos - num_neg		
		features['frac_pos'] = num_pos / sent_len
		features['frac_neg'] = num_neg / sent_len

		return features