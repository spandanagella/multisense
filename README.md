# multisense


To download images in MultiSense dataset please follow the link [**here**](https://drive.google.com/open?id=1e0ebK7KWlBzlc0j2u3CpXWJ0zVupPxM9)

[gold_german_query_classes.csv](../master/gold_german_query_classes.csv): 
  This file has verb, query phrase and its Spanish translation.

[gold_spanish_query_classes.csv](../master/gold_spanish_query_classes.csv): 
  This file has verb, query phrase and its Spanish translation.

Evaluate the verb accuracy (VAcc; Table 4) of the predicted translations: 
>python eval_verb_accuracy.py TRANSLATIONS

Dependencies:

* spacy
* `python -m spacy download de_core_news_sm`

Creation of the MultiSense dataset is described in the below paper:

Spandana Gella, Desmond Elliot, and Frank Keller. 2019. Crosslingual Visual Verb Sense Disambiguation. In Proceedings of the Human Language Technology Conference of the North American Chapter of the Association for Computational Linguistics (NAACL 2019). Minneapolis, USA.
