with open('negations.txt', 'r') as f:
    lines = f.readlines()
lines = [l.strip() for l in lines]
"""
couldn't --> couldn
"""

for l in lines: 
    if "'" in l:
        print l.split("'")[0]

