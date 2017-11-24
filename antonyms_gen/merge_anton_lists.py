# takes list of antonym files as cmd line arguments and merges them into
# output file antonyms.txt

import sys

antonyms = {}
files = [f.strip() for f in sys.argv[1:]]

for fname in files:
    with open(fname, 'r') as f:
        lines = f.readlines()
    
    # add to dict
    for l in lines:
        pair = l.strip().split(' ')
        word1 = pair[0].strip()
        word2 = pair[1].strip()
        if (word1, word2) not in antonyms:
            antonyms[(word1, word2)] = 1

# save unique antonyms to file in sorted order
count = 0
with open('antonyms.txt', 'w') as output: 
    pairs = list(antonyms.keys())
    pairs.sort()
    for pair in pairs:
        count += 1
        output.write("{} {}\n".format(pair[0], pair[1]))

print("Wrote {} antonym pairs to antonyms.txt".format(count))
