import re

class NegationSuffixAdder():
	"""
	Class to add simple negation marking to tokenized
	text to aid in sentiment analysis. 

	A good explanation of negation marking, along with 
	details of the approach used here can be found at: 

	http://sentiment.christopherpotts.net/lingstruc.html#negation

	As defined in the link above, the basic approach is to 
	"Append a _NEG suffix to every word appearing between a 
	negation and a clause-level punctuation mark". Here, negation
	words are defined as those that match the NEGATION_RE regex, and
	clause-level punctuation marks are those that match the PUNCT_RE regex. 

	Please note that this method is due to Das & Chen (2001) and
	Pang, Lee & Vaithyanathan (2002)

	"""

	# Regex credit: Chris Potts

	# regex to match negation tokens
	NEGATION_RE = re.compile("""(?x)(?:
    ^(?:never|no|nothing|nowhere|noone|none|not|
        havent|hasnt|hadnt|cant|couldnt|shouldnt|
        wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
	 )$
	)
	|
	n't""")

	# regex to match punctuation tokens
	PUNCT_RE = re.compile("^[.:;!?]$")

	def __init__(self):
		pass

	def add_negation_suffixes(self, tokens):
		"""
		INPUT: List of strings (tokenized sentence)
		OUTPUT: List of string with negation suffixes added

		Adds negation markings to a tokenized string. 
		"""

		# negation tokenization
		neg_tokens = []
		append_neg = False # stores whether to add "_NEG"
		
		for token in tokens:
			
			# if we see clause-level punctuation, 
			# stop appending suffix
			if self.PUNCT_RE.match(token):
				append_neg = False

			# Do or do not append suffix, depending
			# on state of 'append_neg'
			if append_neg: 
				neg_tokens.append(token + "_NEG")
			else:
				neg_tokens.append(token)	
			
			# if we see negation word, 
			# start appending suffix
			if self.NEGATION_RE.match(token):
				append_neg = True

		return neg_tokens