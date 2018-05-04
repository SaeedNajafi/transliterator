#run with python3
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from xml.dom import minidom
import sys
import collections
import codecs


in_f = codecs.open(sys.argv[1], 'r', 'utf-8') #Input Tab Separated File:
out_f = codecs.open(sys.argv[2], 'w', 'utf-8') #Output XML File:
out_f_raw = codecs.open(sys.argv[3], 'w', 'utf-8') #This will be the source side of the XML

CorpusFormat='Default'
CorpusID='Default'
CorpusSize= 0
CorpusType='Tune'
NameSource='Default'
SourceLang='Default'
TargetLang='Default'

def to_xml():
    dic = collections.OrderedDict()
    for line in in_f.readlines():
        line = line.strip()
        if len(line)!=0: #ignore newline
            line_lst = line.split('\t')
            try:
                source = line_lst[0].replace("   ", "_@_").replace(" ", "").replace("_@_", " ")
                target = line_lst[1].replace("   ", "_@_").replace(" ", "").replace("_@_", " ")
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
        out_f_raw.write(raw_line)
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

    xml = ET.tostring(root, encoding="utf-8", method="xml")
    xml = '<?xml version="1.0" encoding="utf-8"?>' + xml.decode('utf-8')
    out_f.write(xml)
    out_f.close()

if __name__ == '__main__':
    to_xml()
