import re
# re.search, s).group(3)

def file_iterator(filename):
    """
    Generator that returns a file line by line
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

regex = r'(\w+) (\[opposite\-of\]) (\w+) .*'
count = 0
with open('verbocean_antonyms.txt', 'w') as output:
    for line in file_iterator('verbocean_relations.txt'):
        match_obj = re.search(regex, line)
        if match_obj:
            count += 1
            output.write("%s %s\n" % (match_obj.group(1), match_obj.group(3)))
print "Found %d antonyms" % count
