### Aspect-Based Opinion Mining on Yelp Reviews

The goal of this project is to use machine learning and NLP to generate a helpful *aspect-based summary* from the raw text of reviews about a particular restaurant or product. An aspect-based summary of a set of reviews about, say, a pizza place might look as follows: 

* **Pizza**: *5/5*
	* "…I loved the pizza here!" - Joe P.  
* **Wine**: *3/5*
	* "The wine here is excellent…" - Jen A.
* **Service**: *2/5*
	* "…service was slow here…" - Tom B. 
* **Ambiance**: *3/5*
	* "I really enjoyed the atmosphere…" - Sam K.

where "Pizza", "Wine", "Service", and "Ambiance" are the *aspects* of the restaurant which are most commonly mentioned by reviewers, and the scores (e.g. 3/5) reflect reviewers' overall attitudes toward the corresponding aspect. A summary of this form allows consumers to quickly understand a large body of reviews about a product or service and thereby make an informed decision about what or where to buy. 

See `./docs/proposal.md` for more details on this project. 

**References:**

The problem of aspect-based opinion mining has been addressed in academic literature. See especially: 

* Blair-Goldensohn et al.'s ["Building a Sentiment Summarizer for Local Service Reviews"](http://www.ryanmcd.com/papers/local_service_summ.pdf) (2008)
* Bing Liu's [Sentiment Analysis and Opinion Mining](http://www.cs.uic.edu/~liub/FBS/SentimentAnalysis-and-OpinionMining.pdf) (2012)
* Hu & Liu's [Mining and Summarizing Customer Reviews](http://users.cis.fiu.edu/~lli003/Sum/KDD/2004/p168-hu.pdf) (2004)