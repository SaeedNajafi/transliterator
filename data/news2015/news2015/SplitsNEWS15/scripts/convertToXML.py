#!/usr/bin/env python3 

'''
        script takes an output file from DirectTl in the form of 

        aalto	אלטו
        aamir	עאמיר
        aaronsohn	ארונסון
        aatef	עאטף

        and converts it to the proper XML format for evaluation.
 
        There can be multiple output transliterations for a given source word

        usage: ./convertToXML.py dtlOutputFile > XMLFile
'''

import sys


# can change these, but probably won't actually affect the evaluation script
sourceLang = "English"
targetLang = "Hebrew"

print('<?xml version="1.0" encoding="UTF-8"?>')
print()
print('<TransliterationTaskResults')
print('\tSourceLang = "{0}"'.format(sourceLang))
print('\tTargetLang = "{0}"'.format(targetLang))
print('\tGroupID = "University of Alberta"')
print('\tRunID = "1"')
print('\tRunType = "standard"')
print('\tComments = "">')
print()






def printOut(currentSource, currentList, nameID):
    print('\t<Name ID="{0}">'.format(nameID))
    print('\t\t<SourceName>{0}</SourceName>'.format(currentSource))
    count = 1
    for trans in currentList:
        print('\t\t<TargetName ID="{0}">{1}</TargetName>'.format(count, trans))
        count += 1
    print('\t</Name>')


''' replaces the special characters of XML so the news_evalution script works fine '''
def replaceSpecialChars(string):
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\"', '&quot;').replace('\'', '&apos;')


currentSource = ""
currentList = []
nameID = 0

with open(sys.argv[1], 'r') as inputFile:
    # for each source word, appends each possible output to the current list
    # once the souce word changes, prints out the source word with all output words in the desired XML format
    for line in inputFile:
        line = line.strip() # strip newline
        try:
            source, translit = line.split('\t')
        except:
            sys.stderr.write("problem on line: {0}\n".format(line))
            exit(-1)

        if translit == "":
            continue # if it's an empty transliteration then move on 

        source = replaceSpecialChars(source)
        translit = replaceSpecialChars(translit)

        if (source == currentSource):
            # still a transliteration for the same source word
            currentList.append(translit)
        else:
            # on to a new source word, so print all transliterations
            if (currentList != []): # this check is so the first printout isnt empty
                printOut(currentSource, currentList, nameID)
            
            currentSource = source
            nameID += 1
            currentList = [translit] # start a new currentList

    printOut(currentSource, currentList, nameID) # need to print the last name since no change in source occured after the last line of file

print()
print('</TransliterationTaskResults>')







