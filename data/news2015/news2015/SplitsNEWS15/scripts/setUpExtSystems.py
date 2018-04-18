#!/usr/bin/env python3 

''' this script takes aligned output file(s) from m2m that looks like:
a|a|l|t|o|ע|א|ל|ט|ו|
a|a|l|t|o|ע:'|א|ל|ט|ו|
a|a|l|t|o|ע|_|ל|ט|ו|
a|a|l|t|o|ע|י|ל|ט|ו|
a|a|l|t|o|א|_|ל|ט|ו|
a|a|l|t|o|א|א|ל|ט|ו|
a|a|l|t|o|ע|ע|ל|ט|ו|
a|a|l|t|o|ע|_|ל|ט|ו|
a|a|l|t|o|א:י|א|ל|ט|ו|
a|a|l|t|o|א|_|ל|ט|ו|

and puts top  possible transliterations for each system onto one line in the form that lei's joint direcTL expects (like his enhi.ext file)
and prints it out

'''


import sys
data = {}



# read in the file as a dict with keys as the sources, and values as a list of all its transliterations
for i in range(len(sys.argv)):
    if i == 0:
        continue # the program name
    thisSystem = set() # a set to keep track of the words seen in this system's output. only want one translit for each so use this to keep track
    with open(sys.argv[i], 'r') as file:
        for line in file:
            try:
                source, trans = line.strip('\n').split('\t')


                if source in thisSystem:
                    continue # already seen this source word

                thisSystem.add(source) # add to show we have now seen this source

                # otherwise we haven't seen this source yet, so add it to the data dict as either a new entry or append
                if not source in data:
                    data[source] = [trans]
                else:
                    data[source].append(trans)


            except:
                continue # an empty line or something

for source in sorted(data):
    print("\t".join([source] + data[source]))
    # print out source followed by all its transliterations separated with tabs
