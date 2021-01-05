import os
import pickle
from typing import List

import textdistance

from utils.merge.file_reader import Reader


def load_files():
    with open('base_files.pickle', 'rb') as handle:
        base_files = pickle.load(handle)
    with open('variants_files.pickle', 'rb') as handle:
        variants_files = pickle.load(handle)

    return base_files, variants_files


def compare(b_name, v_name):
    similarity_1 = textdistance.hamming.normalized_similarity(b_name, v_name)
    similarity_2 = textdistance.levenshtein.normalized_similarity(b_name, v_name)
    similarity_3 = textdistance.overlap.normalized_similarity(b_name, v_name)
    similarity_4 = textdistance.cosine.normalized_similarity(b_name, v_name)
    similarity_5 = textdistance.sorensen.normalized_similarity(b_name, v_name)
    similarity_6 = textdistance.monge_elkan.normalized_similarity(b_name, v_name)
    similarity_7 = textdistance.tanimoto.normalized_similarity(b_name, v_name)
    similarity_8 = textdistance.jaccard.normalized_similarity(b_name, v_name)

    print("text", b_name, v_name)
    print("hamming", similarity_1)
    print("levenshtein", similarity_2)
    print("overlap", similarity_3)
    print("cosine", similarity_4)
    print("sorensen", similarity_5)
    print("monge_elkan", similarity_6)
    print("tanimoto", similarity_7)
    print("jaccard", similarity_8)

def main():
    # base_files, variants_files = load_files()


    # b1 = base_files[0][1]
    # v1 = [s for f, s in variants_files if f == '1_1_1.tei'][0]

    # base_reader = Reader(b1)
    # variant_reader = Reader(v1)

    compare("Американ бар", "Американка")
    compare("Египтянин Я выстроил себе благополучья дом", "Я выстроил себе благополучья дом")


if __name__ == '__main__':
    main()
