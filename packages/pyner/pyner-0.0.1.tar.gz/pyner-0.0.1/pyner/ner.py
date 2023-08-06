#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Wang, Bodhi Faqun <jyxz5@hotmail.com>
#
"""ner

This program is SDK of Ner service API.

It can handle one sentence and simple text file in chinese

usage: ner.py [-h] [--endpoint ENDPOINT] [--sentence SENTENCE] [--path PATH]

Process one sentence or simple textfile in chinese by Ner service

optional arguments:
  -h, --help           show this help message and exit
  --endpoint ENDPOINT  Endpoint of Ner service
  --sentence SENTENCE  Sentence to process
  --path PATH          Path file to process
  
For instance:

$ python ner.py --endpoint http://example.com/ner/bert/normal --path test.txt --sentence '康龙化成(03759)拟续聘安永华明为2020年度境内会计师事 务所'
{'ORG': ['康龙化成', '安永华明']}
{'LOC': ['新冠', '新疆'],
 'ORG': ['华资实业',
         '明科',
         '中葡',
         '亚星',
         '厦华',
         '中房股份',
         '中房股份',
         '西域旅游',
         '西域旅游',
         '丰华股份',
         '丰华股份',
         '壳公司']}
"""
__author__ = "Wang Bodhi Faqun<jyxz5@hotmail.com>"
__copyright__ = "Copyright 2021 Wang Bodhi Wang"
__license__ = "MIT"
__version__ = "0.1"

import requests
from jsonmerge import merge

class ner:
    schema = {
             "properties": {
                 "LOC": {
                     "mergeStrategy": "append"
                 },
                 "ORG": {
                     "mergeStrategy": "append"
                 },
                 "PER": {
                     "mergeStrategy": "append"
                 }
            }
        }

    def __init__(self, endpoint:str):
        self.endpoint = endpoint

    def getEndpoint(self):
        return self.endpoint

    def ner_sentence(self, sentence:str):
        return requests.post(self.endpoint,
                             json={'sentence':sentence}).json()

    def ner_file(self, path:str, encoding="utf-8"):
        with open(path, "r", encoding=encoding) as f:
            lines = f.readlines()
        lines = [ line.strip() for line in lines if line.strip()!='']

        result = dict()
        for line in lines:
            r=self.ner_sentence(line)
            if r != dict():
                result = merge(result, r, ner.schema)
                #result = tmp

        return result


if __name__ == "__main__":
    from pprint import pprint
    import pybase64, argparse, os, sys

    default_ner_endpoint= pybase64.b64decode(
        b'aHR0cDovL2RhaS5kZWxvaXR0ZS5jb206MzA1MDAvbmVyL2JlcnQvbm9ybWFs').decode("utf-8")


    """Entry point of the program when called as a script.
    """
    # Parse command line options
    parser = argparse.ArgumentParser (description=
                    """Process one sentence and simple text"""
                    """file in chinese by Ner service""")
    parser.add_argument ('--endpoint', dest='endpoint',
                         help='Endpoint of Ner service')
    parser.add_argument ('--sentence', dest='sentence',
                         help='Sentence to process')
    parser.add_argument ('--path', dest='path',
                         help='Path file to process')
    args = parser.parse_args ()
    endpoint = args.endpoint
    if endpoint is None:
        try:
            endpoint = os.getenv ("NER_ENDPOINT", default_ner_endpoint)
        except Exception as e:
            print("[getenv]{}".format(e))
            sys.exit(1)

    sentence = args.sentence
    path = args.path

    if sentence is None and path is None:
        print("Please input sentence or file name to process!")
        parser.print_help()
        sys.exit(1)

    bert_normal = ner (endpoint)

    if sentence is not None:
        try:
            result = bert_normal.ner_sentence(sentence)
            pprint(result, width=40)
        except Exception as e:
            print("[sentence]Failed!{}".format(e))
            sys.exit(1)

    if path is not None:
        try:
            result = bert_normal.ner_file(path)
            pprint(result)
        except Exception as e:
            print("[file]Failed!{}".format(e))
            sys.exit(1)

    sys.exit(0)
