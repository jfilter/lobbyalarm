import os

import spacy

def cut_away_sources(text):
    # cut away unnesarray information

    start = text.find("== weitere führende Literatur und Multimedia ==")
    if start > 0:
        text = text[:start]

    start = text.find("== Weiterführende Informationen ==")
    if start > 0:
        text = text[:start]

    start = text.find("== Einzelnachweise ==")
    if start > 0:
        text = text[:start]
    return text

def preprocess(filename, space_model='/Users/filter/spacy-data/de_core_news_sm-2.0.0/de_core_news_sm/de_core_news_sm-2.0.0'):
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load(space_model)

    print(filename)
    with open(filename) as f:
        text = f.read()

    text = cut_away_sources(text)

    # remove confusion characters
    text = text.replace('=', '')
    text = text.replace('\n\n', ' . ')
    print(text)

    return nlp(text)


def get_filenames(dir_path='../data/documents'):
    fs = [entry for entry in os.scandir(
        dir_path) if entry.is_file() and not entry.name.startswith('.')]

    fs = [f for f in fs if f.name not in [
        'Zitieren und Quellenangabe.txt', 'FAQ.txt']]
    return fs
