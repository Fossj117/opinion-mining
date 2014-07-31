## Summary Generation Pipeline

The files in this directory manage YUMM's main summary generation pipeline. The files in the top level of this directory (i.e. `business.py`, `review.py`, and `sentence.py`) are correspond to the "objects" that are passed through YUMM's pipeline, each managing analytical components at different levels of granularity (i.e. business-level analytics are handled by `Business` objects, whereas sentence-level analyses/processing are handled by `Sentence` objects). 

By contrast, the classes found in the `./transformers` should be thought of as *acting on* the business/review/sentence objects, performing various transformations or analyses such as tokenization or aspect extraction, the results of which are then stored by the corresponding business/review/sentece object.

