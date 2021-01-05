import os
import pickle
from collections import defaultdict
from typing import List

import textdistance

from utils.merge.file_reader import Reader


def load_files():
    with open('base_files.pickle', 'rb') as handle:
        base_files = pickle.load(handle)
    with open('variants_files.pickle', 'rb') as handle:
        variants_files = pickle.load(handle)

    return base_files, variants_files


def clean(name):
    name = name.replace('*', '')
    name = name.replace('«', '')
    name = name.replace('»', '')
    name = name.replace(',', '')
    name = name.replace('—', '')
    name = name.replace(':', '')
    name = name.replace('…', '')
    name = name.replace('...', '')
    name = name.replace('..', '')
    name = name.replace('.', '')
    name = name.replace('!', '')
    name = name.replace(';', '')
    name = name.replace(';', '')
    name = name.replace(')', '')
    name = name.replace('(', '')
    return name


def main():
    base_files, variants_files = load_files()
    base_files_names = set([name for (name, _) in base_files])
    variants_files_names = set([name for (name, _) in variants_files])
    used = set()
    pairs = defaultdict(list)

    i = 0
    for base_file_name, base_soup in base_files:
        for variant_file_name, variant_soup in variants_files:
            base_reader = Reader(base_soup)
            variant_reader = Reader(variant_soup)
            b_name = base_reader.get_name_from_header()
            v_name = variant_reader.get_name_from_header()
            b_name = clean(b_name)
            v_name = clean(v_name)
            jaccard_similarity = round(textdistance.jaccard.normalized_similarity(b_name, v_name), 3)
            levenshtein_similarity = round(textdistance.levenshtein.normalized_similarity(b_name, v_name), 3)
            if jaccard_similarity > 0.7 and levenshtein_similarity > 0.7:
                print(base_file_name,
                      variant_file_name,
                      b_name,
                      v_name,
                      f'j:{jaccard_similarity} l:{levenshtein_similarity} ')
                pairs[base_file_name].append(variant_file_name)
                used.add(base_file_name)
                used.add(variant_file_name)
            i = i + 1

        if i % 10000 == 0:
            print(f'pass {i} iterations')
    print('Unused base', base_files_names - used)
    print('Unused variants', variants_files_names - used)
    with open('pairs.pickle', 'wb') as handle:
        pickle.dump(pairs, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()
