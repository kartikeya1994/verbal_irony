"""
Prints number of sentences with aligned antonyms
Sentences that match this filter are saved to .log file

Usage:
    python check_aligned_antonyms_dev.py \
            dev.txt alignments.txt antonyms.txt \
            antonym_prefixes.txt
"""

import sys
import datetime
from utils import file_iterator, parse_alignment, load_antonyms
from utils import load_antonym_prefixes, are_prefixed
from utils import parse_corpus_line_dev

from nltk.stem.wordnet import WordNetLemmatizer
Lemmatizer = WordNetLemmatizer()

def are_antonyms(word1, word2, antonyms, antonym_prefixes):
    global Lemmatizer

    if word1 in antonyms.get(word2, set()) \
                    or word2 in antonyms.get(word1, set()) \
                    or are_prefixed(word1, word2, antonym_prefixes):
        return True

    word1_l = Lemmatizer.lemmatize(word1, 'v')
    word2_l = Lemmatizer.lemmatize(word2, 'v')

    if word1_l in antonyms.get(word2_l, set()) \
                    or word2_l in antonyms.get(word1_l, set()) \
                    or are_prefixed(word1_l, word2_l, antonym_prefixes):
        return True
    return False

def log_sample(log_file, word1, word2, idx, ground_truth, alignment):
    log_file.write("{} - {}\n".format(word1, word2))
    log_file.write("{}({})\n".format(idx, ground_truth))
    log_file.write("Alignment: {}\n\n".format(str(alignment)))

if __name__ == '__main__':
    
    if len(sys.argv) < 5:
        sys.exit("Need 4 args: dev file, alignments, antonyms, prefixes")
    
    dev_file = sys.argv[1]
    data_file = sys.argv[2]
    antonyms_file = sys.argv[3]
    antonym_prefix_file = sys.argv[4]

    antonyms = load_antonyms(antonyms_file)
    antonym_prefixes = load_antonym_prefixes(antonym_prefix_file)

    total_count = 0.0
    ants_count = 0.0
    true_pos = 0.0
    false_neg = 0.0
    false_pos = 0.0
    expected = 0.0

    tp = datetime.datetime.now().strftime("%y.%m.%d-%H.%M.%S")
    true_pos_log = open('logs/ant_dev_tru_pos_' + tp + '.log', 'w')
    false_pos_log = open('logs/ant_dev_fal_pos_' + tp + '.log', 'w')
    false_neg_log = open('logs/ant_dev_fal_neg_' + tp + '.log', 'w')

    dev = []
    for line in file_iterator(dev_file):
        tokens = parse_corpus_line_dev(line)
        if 'antonym' in tokens[5].split(','):
            expected +=1
        dev.append((tokens[0], tokens[5]))
    total_count = len(dev)

    alignments = []
    for sentence in file_iterator(data_file):
        if sentence is None:
            continue
        align = parse_alignment(sentence)
        alignments.append(align)
    
    for idx,ground_truth in dev: 
        found = False
        for tups in alignments[int(idx)]:
            word1 = tups[0]
            word2 = tups[2]
            if are_antonyms(word1, word2, antonyms, antonym_prefixes):
                # found antonym pair
                ants_count += 1
                if 'antonym' in ground_truth.split(','):
                    true_pos += 1
                    log_sample(true_pos_log, word1, word2, idx, ground_truth,\
                            alignments[int(idx)])
                else:
                    false_pos += 1
                    log_sample(false_pos_log, word1, word2, idx, ground_truth, \
                            alignments[int(idx)])
                found = True
                break
        if not found and 'antonym' in ground_truth.split(','):
            false_neg += 1
            log_sample(false_neg_log, '', '', idx, ground_truth, alignments[int(idx)])

    true_neg = total_count - true_pos - false_pos - false_neg
    print("Total sentences:\t{}".format(total_count))
    print("Antonym pairs expected:\t{}".format(expected))
    print("Antonym pairs detected:\t{}".format(ants_count))
    print("Antonym pairs detected correctly:\t{}".format(true_pos))
    print("Antonym pairs missed:\t{}".format(false_neg))
    precision = true_pos / (true_pos + false_pos)
    recall = true_pos / (true_pos + false_neg)
    f1 = 2 * precision * recall / (precision + recall)
    print("Precision:\t{}\nRecall:\t{}\nF1:\t{}\n".format(precision, recall, f1))
    true_pos_log.close()
    false_pos_log.close()
    false_neg_log.close()
