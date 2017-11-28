"""
Remove duplicate lines
python dedup.py filename.txt
"""
import sys

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
print('Found {} lines'.format(len(lines)))

s = set()
out = open(sys.argv[1] + '.dedup', 'w')
for l in lines:
    l = l.strip()
    if l not in s:
        out.write(l + '\n')
    s.add(l)
out.close()
print('Unique lines: {}'.format(len(s)))
