"""
Extract tweets with '?' from json obj file and save to file on new line
"""

import sys
import json

def file_iterator(filename):
    """ 
    Returns generator
    Generates file line by line
    If blank line, return None instead
    """
    corpus_file = file(filename, 'r')
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            yield line
        else: # Empty line
            yield None
        l = corpus_file.readline()

def print_tweets(filename):
    out = open(filename + '.tweets', 'w')
    count = 0
    for l in file_iterator(filename):
        if l is not None:
            tweet = json.loads(l)
            text = tweet['full_text']
            if '?' not in text:
                continue
            text = text.replace('\n',' ') + unicode('\n')
            print(text)
            out.write(text.encode('utf-8'))
            count += 1
    out.close()
    print("Found {} tweets with ?".format(count))

filename = sys.argv[1]
print_tweets(filename)

