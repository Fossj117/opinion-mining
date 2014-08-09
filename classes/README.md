## Summary Generation Pipeline

The files in this directory manage YUMM's main summary generation pipeline. The files in the top level of this directory (i.e. `business.py`, `review.py`, and `sentence.py`) correspond to the "entities" that are passed through YUMM's pipeline, each storing data and managing analytical components at different levels of granularity (i.e. business-level data and analytics are handled by `Business` objects, whereas sentence-level data/analyses/processing are handled by `Sentence` objects). 

By contrast, the classes found in the `./transformers` should be thought of as *acting on* the business/review/sentence entities, performing various transformations or analyses such as tokenization or aspect extraction, the results of which are then stored by the corresponding business/review/sentece object.

In general, `transformer` objects are instantiated as class variables of entities, since we only need, e.g., *one* word tokenizer (a `transformer`) for *all* of the `Sentence` objects, and we would like to avoid the overhead of creating a new transformer for every `Sentence` instance. This is because, in some cases, there is significant start-up cost associated with instantiating a `transformer`--e.g. see some of the `featurizer` transformers--and there are many `Sentence` objects. 

The **entity** instances (e.g. `Sentence`s) are then typically responsible for calling their class-level transformer to transform themselves. So, for example, a `Sentence` object is responsible for tokenizing itself by calling the `WORD_TOKENIZER` transformer that is a class variable of the `Sentence` class. 

This discussion has been somewhat abstract, but hopefully gives a general sense of the structure of the project.

### One Exception

Currently the one exception to this general architecture sits with `Business` entities, which currently also manage the opinion/sentiment modeling (which is a sentence-level analysis). This exception is unnecessary and will likely be changed in future iterations. 



