import os
import sys
import pickle

from bs4 import BeautifulSoup

# We need it to pickle BS objects
# https://stackoverflow.com/a/37000227/733718
sys.setrecursionlimit(10000)

BASE_DIR = "../../base"
VARIANTS_DIR = "../../tei"


def check_ext(f: str):
    return f.endswith('tei') or f.endswith('xml')


def get_list_of_files(directory: str):
    files = os.listdir(directory)
    files.sort()
    return [(f, f'{directory}/{f}') for f in files if check_ext(f)]


def get_soups_for_dir(directory: str):
    directories = get_list_of_files(directory)
    print(f"Got files from {directory}")
    files = [(f, open(path, 'r')) for f, path in directories]
    print(f"Got files descriptors from {directory}")
    contents = [(f, file.read()) for f, file in files]
    print(f"Got files content from {directory}")
    soups = [(f, BeautifulSoup(content, 'html.parser')) for f, content in contents]
    print(f"Got soups from {directory}")
    return soups


def save_files():
    base_files = get_soups_for_dir(BASE_DIR)
    variants_files = get_soups_for_dir(VARIANTS_DIR)

    with open('base_files.pickle', 'wb') as handle:
        pickle.dump(base_files, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Wrote soups for base_files")

    with open('variants_files.pickle', 'wb') as handle:
        pickle.dump(variants_files, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Wrote soups for variants_files")


if __name__ == '__main__':
    save_files()
