## Modeling Pipeline

The files in this directory are responsible for training and optimizing the machine learning algorithms that drive YUMM. In particular: 

* `0_data_prep.py` : responsible for reading in the raw data provided by Yelp from file, converting to usable form, and filtering unnecessary information.

* `1_featurize_training_data.py` : responsible for reading in the manually-tagged training data and featurizing it for model training. 

* `2_grid_search_CV.py` : runs a grid search to optimize hyperparameters for both the opinion and sentiment models. In practice, this was always run using [domino](http://www.dominoup.com/). Note that the final models tuned by the grid search are ultimately pickled, for later use in YUMM's main summary-generation pipeline (see `../classes`). The results of the grid search are stored in `./results`

## Model Results

YUMM takes a two-stage modeling approach, first attempting to classify a given sentence as Opinionated vs. Not Opinionated, and only subsequently attempting to classify Opinionated sentences as being Positive or Negative. 

Currently, the Opinion Model is an SVM, and the Sentiment Model is a Logisitc Regression. Both models are currently trained using an extremely lightweight featureset (only 16 total features) that includes primaryily lexion- and syntactic-features (e.g. number/fraction of positive/negative words, number/fraction of various parts of speech). 

Given the minimal featuresets, both models currently perform quite respectably on cross validation:

##### Opinion Model:

Here is the performace report for the tuned SVM opinion model (0 is objective, 1 is subjective).

```
Opinion_Model Classification Report:
             precision    recall  f1-score   support

          0       0.40      0.62      0.49       152
          1       0.85      0.69      0.76       456

avg / total       0.74      0.67      0.69       608
```

![](/modeling/results/Opinion_Model.png)

##### Sentiment Model: 

Here is the performance report for the tuned Logisitc Regression sentiment model (1 is positive, -1 is negative): 

```
Sentiment_Model Classification Report:
             precision    recall  f1-score   support

         -1       0.46      0.75      0.57        84
          1       0.93      0.79      0.86       361

avg / total       0.84      0.78      0.80       445
```

![](/modeling/results/Sentiment_Model.png)

Note that precision is currently quite low on classifying Negative sentences; I expect that this is primarily due to the small amount of training data that was available, the majority of which was *not* negative: 

```
Size of complete development set: 3040
Target class breakdowns:
 1    1759 (positive)
 0     816 (objective)
-1     465 (negative)
```

Although the model does its best to account for this imabalance (e.g. by heavily weighting negative examples in the loss function), sometimes more data is simply needed. 
 
Future iterations of YUMM intend to build out the modeling featureset further, hopefully incorporating more lexicon-based features derived from a WordNet propogation scheme such as that of [Blair-Goldensohn et al. (2008)](http://www.ryanmcd.com/papers/local_service_summ.pdf). However, YUMM aims to avoid the complexity of a full-blown Bag-of-Words/TFIDF approach.  








