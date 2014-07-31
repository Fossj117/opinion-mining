## Modeling Pipeline

The files in this directory are responsible for training and optimizing the machine learning algorithms that drive YUMM. In particular: 

* `0_data_prep.py` : responsible for reading in the raw data provided by Yelp from file, converting to usable form, and filtering unnecessary information.

* `1_featurize_training_data.py` : responsible for reading in the manually-tagged training data and featurizing it for model training. 

* `2_grid_search_CV.py` : runs a grid search to optimize hyperparameters for both the opinion and sentiment models. In practice, this was always run using [domino](http://www.dominoup.com/).