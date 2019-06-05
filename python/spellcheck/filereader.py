import os
import re
import sys

from spellchecker import SpellChecker

path = "auth.go"

proj_path = "/home/matrix/workspace/github/kubernetes"

def load_known_words():
    known_words = set()
    with open("known_words.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            if l:
                known_words.add(l)
    return known_words

def load_file(path=path):
    all_words = set()
    with open(path, "r") as f:
        for l in f.readlines():
            if "'" in l or '"' in l:
                words = re.findall("\w+", l.lower())
                for w in words:
                    if len(w) <= 2 or len(w) > 10:
                        continue
                    if "_" in w:
                        continue
                    if re.findall(r"\d", w):
                        continue
                    # print(w)
                    all_words.add(w)
    return all_words


spell = SpellChecker()
spell.word_frequency.load_words(load_known_words())

def check_misspell(path):
    all_words = load_file(path)
    misspelled = spell.unknown(all_words)
    # print(spell.known(all_words))
    for w in misspelled:
        print(w)
    if misspelled:
        sys.exit(1)


proj_path = "/home/matrix/workspace/github/kubernetes"

def walk_through(ppath):
    all_content = os.walk(ppath)
    for a in all_content:
        path, dirs, files = a
        for f in files:
            if not f.endswith("go"):
                continue
            full_path = os.path.join(path, f)
            print(full_path)
            check_misspell(full_path)


if __name__ == "__main__":
    walk_through(proj_path)