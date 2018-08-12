import sys

sys.path.append("../wrangle")

import util

from flair.data import Sentence
from flair.models import SequenceTagger


fs = util.get_filenames()
fs = [f for f in fs if f.name  == 'Astroturfing.txt']
tagger = SequenceTagger.load('de-ner-germeval')
# fs = [f for f in fs if f.name.lower() == 'Bund Katholischer Unternehmer.txt'.lower()]
for f in fs:
    doc = util.preprocess(f, '/home/filter/spacy-data/de_core_news_sm-2.0.0/de_core_news_sm/de_core_news_sm-2.0.0')
    sents = [Sentence(' '.join([str(t) for t in s])) for s in doc.sents]
    tagger.predict(sents, mini_batch_size=64)
    res = []
    for sentence in sents:
        for token in sentence:
             if token.tags['ner'] != '' and token.tags['ner'] != 'O':
                   res.append(token.text + ' ' + token.tags['ner'])
    print(sents)
    print(res)
    with open('../data/res2/' + f.name, 'w') as outfile:
        outfile.write('\n'.join(res))
