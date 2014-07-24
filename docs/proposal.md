#Feature-Based Opinion Mining on Yelp Reviews

Jeff Fossett## Overview and BackgroundMy proposal is to develop a feature-based opinion mining (i.e. “aspect-based sentiment summarization”) tool for Yelp reviews. Rather than the aggregate “positive/negative” classification that is done in classical sentiment analysis, the goal in feature-based opinion mining is to take as input a set of user reviews for a particular product or service and produce:
1. A set of relevant aspects, 2. An aggregate sentiment score for each aspect, and 3. Supporting textual evidence. 
Thus, rather than determining whether a review of a restaurant is, on-the-whole, positive or negative, the aim is to extract user attitudes towards the food vs. the décor vs. the service. These attitudes can then be aggregated across users to give a clear picture of exactly what users like/dislike about a particular restaurant/product/service. This is a difficult problem, but it has been studied fairly extensively in the past,given its obvious business value, and is just beginning to be put in to practice by leading tech firms (e.g. on Amazon see “Popular Discussion Topics (beta)” in the reviews section [here](http://www.amazon.com/Canon-PowerShot-SX510-Digital-Optical/dp/B00EFILPHA/ref=sr_1_1?ie=UTF8&qid=1403439375&sr=8-1&keywords=canon+camera); similarly, see the “What people are saying” section of Google Shopping [here](https://www.google.com/shopping/product/7051366981881603591?hl=en&q=canon t3i&oq=canon &ei=Q8qmU5zCNZOpyASK-4CoAg&ved=0CJwEEKYrMAA&prds=hsec:reviews); Yelp is also beginning to provide “Review Highlights”). My goal would be to replicate these results on review data from Yelp. This is a non-trivial task given the domain-specificity of high quality sentiment analysis/NLP (especially aspect extraction). ## Data AcquisitionI need to acquire three kinds of data for the complete version of this project: 
1. Yelp Data
2. Sentiment Analysis Data
3. (Static) Aspect Extraction Data
There are several options for how to acquire each dataset: #### Yelp Data:The primary data necessary for this project is the raw text of a (flexible) number of reviews, as well as some of the associated meta-data. There are several options for data acquisition here, each with various pros and cons:
**Option 1: Use Yelp Dataset Challenge Data** 
Yelp has publicly released a significant sample of their data (inluding over 300,000 reviews) as part of their [Dataset Challenge](http://www.yelp.com/dataset_challenge/). I could use this data for my project. Advantages of this approach:

1. Data is easy/quick to acquire2. Could enter my project in Yelp Dataset Challenge (& possibly win money/recognition)

Disadvantages of this approach: 

1. Don't get to demonstrate my ability to scrape data to employers (though I have evidence of this elsewhere).2. Data is from the greater Pheonix, AZ metropolitan area, and thus less relevant to me & Bay Area employers. 
** Option 2: Scrape Data**
I could also scrape data from Yelp. This wouldn't be too tough, but would take a bit more time than simply downloading from the Dataset Challenge. 

#### Sentiment Data: 

To train my sentiment analysis classifier, I will also need some tagged sentiment data. There are again several options: 

1. Contact author of original paper to see if he will share original data. 
2. Acquire comparable data from elsewhere: 
	* [Bing Liu](http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#datasets)
	* [Movie Review Dataset](http://ai.stanford.edu/~amaas/data/sentiment/)
3. Create my own (domain-targeted) dataset using crowdflower or Mechanical Turk. 
4. Create my own dataset by hand (personally)

#### Static Aspect Extraction Data:

Need data to classifiy sentences as being pertinent to particular static aspects relevant to the restaurant domain (e.g. 'food', 'decor' etc.). About 1500 hand-labeled examples should suffice. This would take about a day to do by hand. Could also use crowdflower/mechanical turk.

##Analysis & PresentationMy general analytical approach will follow the method outlined in [this](http://www.ryanmcd.com/papers/local_service_summ.pdf) paper from Google and will thus involve several stages/components:1. Sentiment Classification
2. Aspect Extraction (Dynamic & Static)
3. Summarization & Presentation
I outlined each in turn: **Sentiment Classification**: 
* **Lexicon Construction** (using WordNet propogation from a seed set of positive/negative words to be selected by hand)
* **Building a Classifer**: 
	* Supervised approach likely using Logistic Regression or Naive Bayes.  	* *Feature extraction* will primarily involve intelligently using the lexicon built in the previous step.  Depending on where my data comes from, the overall rating of the review (e.g. '4 stars') will also be a feature in my model. 	* Training will use manually-tagged data. **Aspect Extraction**: 
I will use a hybrid approach involving both "Dynamic" and "Static" approaches: 
* **Dynamic Aspect Extraction**: Dynamic in the sense that it relies only on the text of a set of reviews to determine the ratable aspects for a service. 
	* General idea is to identify aspects as short strings which appear with high frequency in opinion statements, uing a series of filters that employ syntactic patterns, relative word freqnecy, and sentiment lexicon. 
	* Unsupervised. 
* **Static Aspect Extraction**: Idea here is to identify a priori aspects of interest for the domain of restaurants (e.g. "food", "decor", "service", "value") and build a classifier to determine whether particular sentence/fragment includes a reference to this category. Original paper used 1500 hand-labeled examples. 		
* **Combining Static & Dynamic Aspect Extraction**: See original paper for heuristic approach to this. 
	
**Summarization & Presentation**: Final step of the project is to summarize and display the findings of the whole system in a useful way. The minimal approach here would be to simply create a static presentation containing some results (e.g. a powerpoint, paper etc.).
A prefereable but more time-intensive possibility would be to create a simple web front-end as in the "case-study" project that we recently completed. Ideally, this would be hooked up to a database of results, and could display my system's results based on a query. 
In addition to these deliverables, I also hope to complete several blog posts as I progress through the project, detailing smaller components of the project (e.g. explaining WordNet propogation). ### Resources: 

* [Building a Sentiment Summarizer for Local Service Reviews](http://www.ryanmcd.com/papers/local_service_summ.pdf)
* [Opinion Mining, Sentiment Analysis, and Opinion Spam Detection](http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html) (Bing Liu)
* [Sentiment Symposium Tutorial](http://sentiment.christopherpotts.net/) (Chris Potts)
	* [WordNet Propogation](http://sentiment.christopherpotts.net/lexicons.html#wnpropagate) 