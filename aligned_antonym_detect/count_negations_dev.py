"""
Prints number of sentences with negations markers
Sentences that match this filter are saved to .log file

This is for _dev files (that have no hash between S_H and S_I)

Usage: python count_negations_dev.py data_file negations.txt
"""

import sys
import datetime
from utils import file_iterator, parse_corpus_line_dev as parse_corpus_line, load_negations 

if __name__ == '__main__':
    
    data_file = sys.argv[1]
    negations_file = sys.argv[2]
    
    negation_markers = load_negations(negations_file)
    
    total_count = 0
    negs_count = 0
    
    timestamp = datetime.datetime.now().strftime("%y.%m.%d-%H.%M.%S")
    log_file_name = 'negation' + timestamp + '.log'
    log_file = open(log_file_name, 'w')

    for line in file_iterator(data_file):
        if line is None:
            continue
        total_count += 1
        cols = parse_corpus_line(line)
        words = cols[3].split(' ') + cols[4].split(' ')
        for word in words:       
            if word in negation_markers:
                negs_count += 1
                log_file.write("Marker: {}\n".format(word))
                log_file.write("Sentence: {}\t{}\n\n".format(cols[2], cols[4]))

    print("Total sentences: {}".format(total_count))
    print("Negations found in: {}".format(negs_count))
    log_file.close()
