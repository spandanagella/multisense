import csv
import sys
import spacy
import argparse


VERBOSE = False


def load_query_trans_dict(file, lang):
    '''
    Create the Query->Translation lookup dictionary from the file `gold_german_query_classes.csv`
    '''
    query_trans_dict = dict()

    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = row['query'].strip()
            if lang == 'en':
                query_trans_dict[query] = row['verb'].strip()
            elif lang == 'de':
                query_trans_dict[query] = row['verb_translation'].strip()

    return query_trans_dict


def load_gold_lemmas(filename, query_trans, spacy_model):
    '''
    Map each of the image name prefixes onto the expected German translation.
    The data for this mapping is gold standard for German.
    '''
    image_names = open(filename).readlines()
    gold_lemma_forms = []

    for name in image_names:
        form = query_trans[name.split("__")[0].replace("_", " ")]
        lemma = spacy_model(form)[0].lemma_
        gold_lemma_forms.append(form)

    return gold_lemma_forms


def create_correction_dict():
    '''
    Create a dictionary that we use to fix the mistakes made by SpaCy.
    '''
    corrections = dict()
    corrections['herausstreckt'] = 'heraustrecken'
    corrections['blockt'] = 'blocken'
    corrections['fällt'] = 'fallen'
    corrections['fällen'] = 'fallen'
    corrections['schreit'] = 'schreiten'
    corrections['kremt'] = 'kremen'
    corrections['passt'] = 'passen'
    corrections['coupiert'] = 'coupieren'
    corrections['presst'] = 'pressen'
    corrections['gezogen'] = 'ziehen'
    corrections['abzublocken'] = 'abblocken'
    corrections['diving'] = 'dive'
    corrections['riding'] = 'ride'
    corrections['rid'] = 'ride'
    return corrections


def tidy_lemmatization(sentence, corrections):
    '''
    Sometimes SpaCy just does the wrong thing so let's fix it here.
    '''
    for token in sentence:
        if token.pos_ == "VERB" and token.lemma_ in corrections:
            token.lemma_ = corrections[token.lemma_]
    return sentence


def eval_verb_accuracy(infile, gold_lemma_forms, lang, images, spacy_model):
    '''
    Process the translations proposed by a given system:
    1. Read the lines
    2. Lemmatize the lines
    3. Look for exact matches between any output word and the gold_lemma_form
    '''
    if type(infile) is not list:
        data = open(infile).readlines()
    else:
        data = infile
    correct = 0.
    total = len(data)
    found = False
    image_names = open(images).readlines()
    corrections = create_correction_dict()

    for line, gold, image in zip(data, gold_lemma_forms, image_names):
        line = line.replace("\n", "")
        doc = spacy_model(u"{}".format(line))
        doc = tidy_lemmatization(doc, corrections)
        for token in doc:
            if (token.lemma_ == gold and token.pos_ == "VERB") or (lang == "de" and gold.endswith(token.lemma_)):
                correct += 1.
                found = True
                break
        if found == False:
            if VERBOSE:
                print('{} | {} | {}'.format(line, [token.lemma_ for token in doc], gold))
        found = False

    print('{} verb translation accuracy: {}'.format(lang, 100*(correct/total)))


def main(input, query_dict, images, lang):
    if lang == "en":
        spacy_lang = "en_core_news_sm" 
    elif lang == "de":
        spacy_lang = "de_core_news_sm"
    else:
        print("This script currently only support EN or DE.")
        return

    spacy_model = spacy.load(spacy_lang)
    query_trans_dict = load_query_trans_dict(query_dict, lang)
    gold_lemma_forms = load_gold_lemmas(images, query_trans_dict, spacy_model)
    eval_verb_accuracy(input, gold_lemma_forms, lang, images, spacy_model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="Text file pointing to the model output")
    parser.add_argument("--images", type=str, help="Text file defining the evaluation images", default="images.txt")
    parser.add_argument("--querydict", type=str, help="File the defines the transaltions of the ambiguous source langauge tokens in the target language", default="gold_german_query_classes.csv")
    parser.add_argument("--lang", type=str, help="Target language for evaluation", default="de")

    args = parser.parse_args()

    main(args.input, args.querydict, args.images, args.lang)
