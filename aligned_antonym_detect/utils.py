import re
import sys

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
            yield line.lower()
        else: # Empty line
            yield None
        l = corpus_file.readline()

def parse_corpus_line_dev(line):
    """
    For lines with 6 tab separated tokens
    
    0
    3H6W48L9F42CC50XQMM7DPHVFTZPWI  
    423103189333082112      
    Nothing like waiting in line for books. #hooray #great  
    Nothing is worse than waiting in line for books.        
    antonym
    
    """
    cols = line.split('\t')
    if len(cols) != 6:
        sys.exit("Something wrong with line: \n{}\n".format(line))
    return cols

def parse_corpus_line(line):
    """
    Each line has 9 tab separated tokens: 

    3H6W48L9F42CC50XQMM7DPHVFTZPWI
    423103189333082112
    Nothing like waiting in line for books. #hooray #great  
    A2Z64DTPQY8DNV   
    Nothing is worse than waiting in line for books.
    3
    BLANK_STRING
    3FCO4VKOZ4QTPZA690YKRXJA9FE7E8  
    3
    
    """
    cols = line.split('\t')
    if len(cols) != 9:
        sys.exit("Something wrong with line: \n{}\n".format(line))
    return cols

def _parse_alignment_token(token):
    """
    Handle the case: gold|||23--|||26
    """
    token = token.split('|||')
    if len(token) != 3:
        sys.exit("Error: Something wrong with token: {}".format(token))
    word1 = token[0]
    pos2 = int(token[2])
    middle = token[1]
    case1 = re.search(r"(\d+)-",middle) # 23--
    if case1:
        pos1 = case1.group(1)
        word2 = middle[len(pos1)+1:]
        return (word1, pos1, word2, pos2)
    else:
        sys.exit("Error: Something wrong with token: {}".format(str(token)))
    
def parse_alignment(sentence):
    """
    Each alignment is of form: word1|||pos1-word2|||pos2
    Returns list of (word1, pos1, word2, pos2)
    """
    tokens = sentence.split(' ')
    # tokens = [token.strip() for token in tokens]
    parsed = []
    for token in tokens:
        parsed_token = _parse_alignment_token(token)
        parsed.append(parsed_token)
    return parsed

def parse_alignments(filename):
    """
    Return list of list of tuples. 
    Inner list of tuples is alignment info for one sentence. 
    """
    alignemnts = []
    for sentence in file_iterator(filename):
        if sentence is not None:
            alignments.append(parse_alignment(sentence))
    return alignments

def load_antonyms(filename):
    """
    Return dict[word] = set(antonyms of word)
    """
    antonyms = {}
    for pair in file_iterator(filename):
        pair = pair.lower().split(' ')
        word1 = pair[0].strip()
        word2 = pair[1].strip()
        
        word1_ants = antonyms.get(word1, set())
        word1_ants.add(word2)
        antonyms[word1] = word1_ants

        word2_ants = antonyms.get(word2, set())
        word2_ants.add(word1)
        antonyms[word2] = word2_ants

    return antonyms

def load_list(filename):
    """
    Returns list from file
    Each line of file is entry in list
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [l.strip().lower() for l in lines]
    lines.sort()
    return lines

def load_set(filename):
    """
    Returns set of lines in file
    """
    return set(load_list(filename))

def load_negations(filename):
    """
    Returns set of negation markers
    """
    return load_set(filename)

def load_antonym_prefixes(filename):
    """
    Returns set of antonym prefixes
    """
    return load_set(filename)

def are_prefixed(word1, word2, prefixes):
    """
    Returns True if either word is formed by using a prefix
    from the prefix set. Return False otherwise.
    """
    if len(word1) > len(word2):
        word1, word2 = word2, word1
    # now word2 is the longer word
    for p in prefixes:
        if p + word1 == word2:
            return True
    return False
