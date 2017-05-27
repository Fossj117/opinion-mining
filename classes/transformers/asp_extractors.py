import nltk
import re
from nltk.corpus import stopwords

class SentenceAspectExtractor():

    # Grammar for NP chunking
    GRAMMAR = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR><IN|CC><NBAR>}  # Above, connected with in/of/etc...
        {<NBAR>}
    """    

    CHUNKER = nltk.RegexpParser(GRAMMAR)

    _my_stopword_additions = ["it's", "i'm", "star", "", "time", "night", "try", "sure", "times", "way", "friends"]
    STOPWORDS = set(stopwords.words('english') + _my_stopword_additions)

    PUNCT_RE = re.compile("^[\".:;!?')(/]$")
    
    FORBIDDEN = {'great', 'good', 'time', 'friend', 'way', 'friends'}

    def __init__(self):
        pass

    def get_sent_aspects(self, sentence):
        """
        INPUT: Sentence
        OUTPUT: list of lists of strings 

        Given a sentence, return the aspects
        """

        tagged_sent = sentence.pos_tagged
        tree = SentenceAspectExtractor.CHUNKER.parse(tagged_sent)
        aspects = self.get_NPs(tree)

        # filter invalid aspects
        return [asp for asp in aspects if self.valid_aspect(asp)]

    def get_NPs(self, tree):
        """
        Given a chunk tree, return the noun phrases
        """

        return [[w for w,t in leaf] for leaf in self.leaves(tree)]

    def leaves(self, tree):
        """
        Generator of NP (nounphrase) leaf nodes of a chunk tree.
        """

        for subtree in tree.subtrees(filter=lambda t: t.label()=='NP'):
            yield subtree.leaves()

    def valid_aspect(self, aspect):
        """
        INPUT: list of strings
        OUTPUT: boolean
        """

        no_stops = [w for w in aspect if w not in SentenceAspectExtractor.STOPWORDS and not self.PUNCT_RE.match(w)]

        if len(no_stops) < 1: #
            return False
        elif any([forbid_wrd in aspect for forbid_wrd in SentenceAspectExtractor.FORBIDDEN]):
            return False
        else:
            return True


