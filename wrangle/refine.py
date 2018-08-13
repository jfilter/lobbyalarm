import glob
import os
import collections
import json

import util


blocklist = ('Ulrich Müller/Heidi Klein', 'Ulrich Müller/Heidi', 'AmCham Denmark', 'Adam Smith', 'Axel Springer', 'a. D.', 'Ernst & Young', 'Carstensen II', 'Barroso I', 'Barroso II', 'Robin Wood', 'CMS-Rui Pena', 'JP Morgan', 'Lehman Brothers', 'Goldman Sachs', 'Keller and Heckman', 'H. Lundbeck', 'Robert Bosch', 'Clifford Chance', 'Morgan Stanley', 'J.P. Morgan Chase', 'Krauss-Maffei Wegmann', 'Otto von Guericke', "'s Tengelmann", 'Friedrich A.', 'G. Rodenstock')

def find_names():
    fns = util.get_filenames('../data/res2')
    all_names = set()
    for fn in fns:
        print(fn.name)
        with open(f'../data/res2/{fn.name}') as f:
            text = f.read()
        lines = text.split('\n')
        lines = [l.split(' ') for l in lines if ' ' in l]

        res = []

        index = 0
        while index < len(lines):
            tok, tag = lines[index]
            next_possible = index + 1 < len(lines)

            # find special cases
            if tag == 'B-PERparg' and next_possible:
                tok_n, tag_n = lines[index + 1]
                if tag_n == 'S-PER':
                    res.append(tok + ' ' + tok_n)
                    index += 1 # skip

            # find all PER consisting of at least 2 token
            if tag == 'B-PER' and next_possible:
                full_word = [tok]
                end_index = index + 1
                while end_index < len(lines):
                    tok_n, tag_n = lines[end_index]
                    if tag_n == 'I-PER':
                        full_word.append(tok_n)
                        end_index +=1
                    elif tag_n == 'E-PER':
                        full_word.append(tok_n)
                        res.append(' '.join(full_word))
                        break
                    else:
                        # ignore all other tokens
                        break
            index +=1

        # filter out useless stuff
        res = [r.replace('a.D.', '').replace('Katzemich/', 'Katzemich').replace('/CSU', '').replace('/FDP', '').replace('/Hamburgisches', '').replace(').Darüber', '').replace(')August', '').replace('AG.', '').replace('(CDU', '').replace('Prof.', '').replace(':\"Überraschenderweise', '').replace('/CDU', '').replace('informieren.\"', '').strip() for r in res if r not in blocklist and 'stiftung' not in r.lower() and 'von hayek' not in r.lower()]
        res = [r for r in res if not r.startswith('Dr. ')]
        all_names.update(res)

    # remove entries that are consumed by other entries
    final = []
    for na in all_names:
        skip = False
        for na2 in all_names:
            if na == na2:
                continue
            if na.lower() in na2.lower() and na.lower() + 's' != na2.lower():
                skip = True
                break
            # remove e.g. 'Helmut Kohls' and keep 'Helmut Kohl'
            if na.lower() == na2.lower() + 's':
                skip =True
                break
        if not skip:
            final.append(na)

    return set(final)


def create_link(name):
    if name.endswith('.txt'):
        name = name.split('.txt')[0]
    # name = name.replace(' ', '_')
    # return f'https://lobbypedia.de/wiki/{name}'
    return name

def create_data():
    names_set = find_names()

    site = {}

    for file in glob.glob("../data/documents/*.txt"):
        name = file.split('.txt')[0].split('/')[-1]
        if name in names_set:
            site[name] = create_link(name)
            print(name)

    files = {}

    for fn in util.get_filenames('../data/documents'):
        with open(fn) as file:
            text = util.cut_away_sources(file.read())
            files[fn.name.split('.txt')[0]] = text


    occ = collections.defaultdict(list)

    # search for occurences of people in all documents
    for name in names_set:
        for page_name, text in files.items():
            if name in text:
                occ[name].append(create_link(page_name))
    print(occ)

    merged = {}

    print(site)
    print(site.keys())

    # # take filenames as special interest and search in all files
    # remaining_files = [f for f in files.keys() if f not in occ.keys()]

    # print(remaining_files)

    # for name in remaining_files:
    #     for page_name, text in files.items():
    #         if name in text:
    #             occ[name].append(create_link(page_name))

    # create final data object
    for name, pages in occ.items():
        if name in site.keys():
            # remove profile from other pages
            if site[name] in pages:
                pages.remove(site[name])
            merged[name] = {'pages': pages, 'profile': site[name]}
        else:
            merged[name] = {'pages': pages}

    with open('../extension/data.js', 'w') as outfile:
        json.dump(merged, outfile, ensure_ascii=False)
    with open('../extension/data.js', 'r+') as file:
        text_json = file.read()
        file.seek(0)
        file.write('var data = ' + text_json + ';')
        file.truncate()

if __name__ == "__main__":
    create_data()
