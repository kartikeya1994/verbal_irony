"""
Prints number of sentences with aligned antonyms
Sentences that match this filter are saved to .log file

Usage: python check_aligned_antonyms.py data_file antonyms.txt
"""

import sys
import datetime
from utils import file_iterator, parse_alignment, load_antonyms
from utils import are_prefixed, load_antonym_prefixes

if __name__ == '__main__':
    
    data_file = sys.argv[1]
    antonyms_file = sys.argv[2]
    antonym_prefixes_file = sys.argv[3]
    
    antonyms = load_antonyms(antonyms_file)
    antonym_prefixes = load_antonym_prefixes(antonym_prefixes_file)

    total_count = 0
    ants_count = 0
    
    log_file_name = datetime.datetime.now().strftime("%y.%m.%d-%H.%M.%S")
    log_file_name = 'logs/ants_untagged' + log_file_name + '.log'
    log_file = open(log_file_name, 'w')

    for sentence in file_iterator(data_file):
        if sentence is None:
            continue
        total_count += 1
        align = parse_alignment(sentence)
        for tup in align:
            word1 = tup[0]
            word2 = tup[2]
            if word1 in antonyms.get(word2, set()) \
                    or word2 in antonyms.get(word1, set()) \
                    or are_prefixed(word1, word2, antonym_prefixes):
                ants_count += 1
                log_file.write("{} - {}\n".format(word1, word2))
                log_file.write("Alignment: {}\n".format(str(tup)))
                log_file.write("Sentence: {}\n\n".format(sentence))
                break

    print("Total sentences: {}".format(total_count))
    print("Antonyms found in: {}".format(ants_count))
    log_file.close()
