#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from xml.dom import minidom
import sys
import collections

in_f = open(sys.argv[1], 'r') #Input Tab Separated File:
out_f = open(sys.argv[2], 'w') #Output XML File:

""" Input Format:
        This script maps a tab separated file to the required XML format.
        On each line in the input file, we have the following structure,
        separated by tabs '\t':
            <SourceName        PredictedTargetName        Rank        Confidence>
            Example input file:
                saeed        SAEED        1        0.9
                saeed        SAIED        3        0.85
                saeed        SAEID        4        0.8
                saeed        SAIID        5        0.7
                ...
"""

""" The attributes of the <TransliterationTaskResults> tag in the output XML:

    SourceLang = "[source_language]"
    TargetLang = "[target_language]"
    GroupID = "[your_institution_name]"
    RunID = "[your_submission_number]"
    RunType = "Standard"
    Comments = "[your_comments_here]"
    TaskID = "[task_id]"

"""
#For now, we use default values, but upon final submission, we will provide meaningful values.
SourceLang = 'Default'
TargetLang = 'Default'
GroupID = 'Default'
RunID = 'Default'
RunType = 'Default'
Comments = 'Default'
TaskID = 'Default'

def to_xml():
    dic = collections.OrderedDict()
    for line in in_f.readlines():
        line = line.strip().decode('utf-8')
        if len(line)!=0: #ignore newline
            line_lst = line.split('\t')
            try:
                source = line_lst[0]
                target = line_lst[1]
                rank = int(line_lst[2])
                if source in dic:
                    dic[source][0].append(target) #add target to targets list
                    dic[source][1].append(rank) #add rank to ranks list
                else:
                    targets = [target] #create target list
                    ranks = [rank] #create rank list
                    dic[source] = (targets, ranks)
            except:
                print("Format error in the input file!")

    in_f.close()

    #sort targets w.r.t. ranks for each source
    for source in dic:
        (targets, ranks) = dic[source]
        sorted_r_t = sorted(zip(ranks,targets))
        sorted_targets = [t for _,t in sorted_r_t]
        sorted_ranks = [r for r,_ in sorted_r_t]
        dic[source] = (sorted_targets, sorted_ranks)

    #write to xml
    root = ET.Element('TransliterationTaskResults')
    root.set('SourceLang', SourceLang)
    root.set('TargetLang', TargetLang)
    root.set('GroupID', GroupID)
    root.set('RunID', RunID)
    root.set('RunType', RunType)
    root.set('Comments', Comments)
    root.set('TaskID', TaskID)
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
    xmlstr_lines[0] = '<?xml version="1.0" encoding="utf-8"?>'
    xmlstr_final = '\n'.join(xmlstr_lines)
    out_f.write(xmlstr_final.encode("utf-8"))
    out_f.close()


if __name__ == '__main__':
    to_xml()
