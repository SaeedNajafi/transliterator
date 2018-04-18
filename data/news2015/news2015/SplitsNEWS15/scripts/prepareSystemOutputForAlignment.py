#!/usr/bin/env python3 

''' this script takes output file(s) that looks like

    adam   trans lit_er 
    and prints an output that looks like
    a d a m  t r a n s % l i t ! e r  that can be m2m aligned now

'''


import sys


with open(sys.argv[1], 'r') as file:
    for line in file:
        try:
            source, trans = line.strip().replace(" ", "%").replace("_", "#").split('\t') # replace _ with ! and space with % so m2m can handle it
            if trans == "!":
                continue # to handle Sequitur ! that were unable to be de-romanized

            source = " ".join(source)
            trans = " ".join(trans)
        except:
            #print("Problem with line: {0}".format(line.strip()))
            continue # should just be an empty line so move on since don't wanna pass that to M2M
        print("\t".join([source,trans]))
