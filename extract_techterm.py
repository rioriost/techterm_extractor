#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse

# Download pytermextract-0_01.zip from http://gensen.dl.itc.u-tokyo.ac.jp/pytermextract/
# python setup.py install 
import termextract.mecab
import termextract.core
import collections

# pip install mecab-python3 unidic
# python -m unidic download
import MeCab
import unidic

mecab = MeCab.Tagger('-d "{}"'.format(unidic.DICDIR))

def parse_text(file_path):
    source_text = open(file_path, 'r', encoding='utf-8').read()
    res = mecab.parse(source_text)
    return res

def extract_tech_term(tagged_text):
    frequency = termextract.mecab.cmp_noun_dict(tagged_text)
    lr = termextract.core.score_lr(
        frequency,
        ignore_words = termextract.mecab.IGNORE_WORDS,
        lr_mode = 1, average_rate = 1
        )
    term_imp = termextract.core.term_importance(frequency, lr)

    data_collection = collections.Counter(term_imp)
    for cmp_noun, value in data_collection.most_common():
        print(termextract.core.modify_agglutinative_lang(cmp_noun), value, sep='\t')

def main():
    parser = argparse.ArgumentParser(description = 'Import data from text file')
    parser.add_argument('file_path',
        help = 'Path of a text file')
    args = parser.parse_args()

    tagged_text = parse_text(args.file_path)

    extract_tech_term(tagged_text)

if __name__ == '__main__':
    main()