#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from xml.dom import minidom
import sys


in_f = open(sys.argv[1], 'r') #Input Tab Separated File:
out_f = open(sys.argv[2], 'w') #Output XML File:
out_f_raw = open(sys.argv[3], 'w') #This will be the source side of the XML

CorpusFormat='Default'
CorpusID='Default'
CorpusSize= 0
CorpusType='Tune'
NameSource='Default'
SourceLang='Default'
TargetLang='Default'

def to_xml():
    dic = {}
    for line in in_f.readlines():
        line = line.strip().decode('utf-8')
        if len(line)!=0: #ignore newline
            line_lst = line.split('\t')
            try:
                source = line_lst[0].replace("   ", "_@_").replace(' ', '').replace("_@_", " ")
                target = line_lst[1].replace("   ", "_@_").replace(' ', '').replace("_@_", " ")
                if source in dic:
                    dic[source].append(target) #add target to targets list
                else:
                    targets = [target] #create target list
                    dic[source] = targets
            except:
                print("Format error in the input file!")

    in_f.close()

    CorpusSize = str(len(dic))

    for source in dic:
	raw_line = ' '.join(list(source))+'\n'
	out_f_raw.write(raw_line.encode('utf-8'))
        targets = dic[source]
	ranks = [str(rank) for rank in range(1, len(targets)+1)]
        dic[source] = (targets, ranks)

    out_f_raw.close()

    #write to xml
    root = ET.Element('TransliterationCorpus')
    root.set('CorpusFormat', CorpusFormat)
    root.set('CorpusID', CorpusID)
    root.set('CorpusSize', CorpusSize)
    root.set('CorpusType', CorpusType)
    root.set('NameSource', NameSource)
    root.set('SourceLang', SourceLang)
    root.set('TargetLang', TargetLang)
    count = 0
    for source in dic:
        count += 1
        (targets, ranks) = dic[source]
        name = ET.SubElement(root, 'Name')
        name.set('ID', str(count))
        sourceName = ET.SubElement(name, 'SourceName')
        sourceName.text = source
        for i in range(len(targets)):
            t = targets[i]
            r = ranks[i]
            targetName = ET.SubElement(name, 'TargetName')
            targetName.set('ID', str(r))
            targetName.text = t

    xml = ET.tostring(root)
    xmlstr = minidom.parseString(xml).toprettyxml(indent="   ")
    xmlstr_lines = xmlstr.split("\n")
    xmlstr_lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    xmlstr_final = '\n'.join(xmlstr_lines)
    out_f.write(xmlstr_final.encode("UTF-8"))
    out_f.close()

if __name__ == '__main__':
    to_xml()
