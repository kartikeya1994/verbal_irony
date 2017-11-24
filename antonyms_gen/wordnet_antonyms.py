from nltk.corpus import wordnet as wn

count = 0
with open('wordnet_antonyms.txt','w') as output:
    for i in wn.all_synsets():
        for j in i.lemmas(): # Iterating through lemmas for each synset.
            for ant in j.antonyms(): # If adj has antonym.
                # Prints the adj-antonym pair.
                count += 1 
                output.write("%s %s\n" % (j.name(), ant.name()))

print "Found %d pairs" % count
