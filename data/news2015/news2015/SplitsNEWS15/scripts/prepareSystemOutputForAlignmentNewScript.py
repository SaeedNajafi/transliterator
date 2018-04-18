#!/usr/bin/env python3 

''' this script takes output file(s) that looks like

    adam   trans lit_er 
    and prints an output that looks like
    a d a m  t1 r1 a1 n1 s1 %1 l1 i1 t1 #1 e1 r1  that can be m2m aligned now

    the second argument should be 1,2, or 3 and is used to append to the chars to make each system supplmental data look like its from a different script
    the hope is that lei's dtl can then learn about each system individually

'''


import sys

number = sys.argv[2] # this is 1 for dtl, 2 for seq, 3 for smt. used so lei's dtl sees each suppl data as a different "script"

with open(sys.argv[1], 'r') as file:
    for line in file:
        try:
            source, trans = line.strip().replace(" ", "%").replace("_", "#").split('\t') # replace _ with ! and space with % so m2m can handle it
            if trans == "!":
                continue # to handle Sequitur ! that were unable to be de-romanized

            source = " ".join(source)
            trans = " ".join(trans)

            newScript = ""
            for char in trans:
                if char == " ":
                    newScript += char
                else:
                    newScript += char+number


        except:
            #print("Problem with line: {0}".format(line.strip()))
            continue # should just be an empty line so move on since don't wanna pass that to M2M
        print("\t".join([source,newScript]))
