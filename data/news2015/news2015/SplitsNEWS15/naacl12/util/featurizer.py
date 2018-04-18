#!/usr/bin/env python3

import optparse
from collections import defaultdict
from operator import itemgetter
from sys import argv, intern, stderr

__author__ = 'Aditya Bhargava'
__license__ = 'FreeBSD'
__version__ = '1.0.0'
__email__ = 'aditya@cs.toronto.edu'


def errordie(msg):
    print(argv[0], ': error: ', msg, sep='', file=stderr)
    exit(1)

parser = optparse.OptionParser(usage='usage: %prog [options] GOLD-TRN IN-TRN '
                               'OUT-TRN GOLD-TST IN-TST OUT-TST')
parser.add_option('-c', '--no-context', dest='context',
                  action='store_false', default=True,
                  help="don't use context features")
parser.add_option('-C', '--no-rcontext', dest='rcontext',
                  action='store_false', default=True,
                  help="don't use reverse context features")
parser.add_option('-t', '--no-transition', dest='transition',
                  action='store_false', default=True,
                  help="don't use transition features")
parser.add_option('-l', '--no-linear-chain', action='store_false',
                  dest='lchain', default=True,
                  help="don't use linear chain features")
parser.add_option('-L', '--no-reverse-chain', action='store_false',
                  dest='rlchain', default=True,
                  help="don't use reverse linear chain features")
parser.add_option('-j', '--no-joint-ngram', dest='joint',
                  action='store_false', default=True,
                  help="don't use joint n-gram features")
parser.add_option('-m', '--m2m-limit', dest='limit', type='int',
                  default=-100, help='lower limit for m2m scores; 0 means no '
                  'limit')
parser.add_option('-M', '--use-MRR', action='store_true', dest='useMRR',
                  default=False, help='use MRR instead of system score')
parser.add_option('-s', '--no-scores', action='store_false', dest='scores',
                  default=True, help="don't use score features")
parser.add_option('-d', '--no-score-diffs', action='store_false',
                  dest='diffs', default=True, help="don't use score "
                  "differences")
parser.add_option('-n', '--no-sys-align', action='store_false',
                  dest='salign', default=True, help="don't use system "
                  "alignments")
parser.add_option('-N', '--no-ngram', action='store_false',
                  dest='ngram', default=True, help="don't use n-gram features")

options, args = parser.parse_args()

if len(args) == 0:
    errordie('no gold train file specified')
elif len(args) == 1:
    errordie('no input train file specified')
elif len(args) == 2:
    errordie('no output train file specified')
elif len(args) == 3:
    errordie('no gold test file specified')
elif len(args) == 4:
    errordie('no input test file specified')
elif len(args) == 5:
    errordie('no output test file specified')
elif len(args) > 6:
    errordie('too many options')
if options.limit >= 0:
    errordie('lower limit must be negative')

anyNGramFeatures = options.context or options.rcontext or options.transition \
                   or options.lchain or options.rlchain or options.joint

anyNGramFeatures = anyNGramFeatures and options.ngram
CONTEXT = 5
RCONTEXT = 5
TRANSITION = 1
JOINT = 4

# read in the gold (answers): should be a tab-delimited file of inputs and
# outputs (no extra characters---just straight letters on one side and phonemes
# on the other)
gold = defaultdict(list)
with open(args[0]) as goldin:
    for line in goldin:
        en, ph = line.strip().replace(' ', '').split('\t')
        gold[en].append(ph)

#print("gold = ")
#print(gold)

gold2 = defaultdict(list)
if args[3] != '/dev/null':
    with open(args[3]) as goldin:
        for line in goldin:
            en, ph = line.strip().replace(' ', '').split('\t')
            gold2[en].append(ph)

#print("gold2 = ")
#print(gold2)


# read in the data
inputs = defaultdict(list)
inplist = []
#print(args[1])
with open(args[1]) as inp:
    for line in inp:
        stuff = line.strip().split('\t')
        en = stuff[0].replace('|', '').replace('_', '')
        ph = stuff[1].replace('|', '').replace('_', '')
        correct = ph in gold[en]

        if en not in inplist:
            inplist.append(en)
        inputs[en].append([ph, correct, stuff])

#print("inputs = ")
#print(inputs.items())



inputs2 = defaultdict(list)
inplist2 = []
with open(args[4]) as inp:
    for line in inp:
        stuff = line.strip().split('\t')
        en = stuff[0].replace('|', '').replace('_', '')
        ph = stuff[1].replace('|', '').replace('_', '')
        correct = ph in gold2[en]

        if en not in inplist2:
            inplist2.append(en)
        inputs2[en].append([ph, correct, stuff])

#print("inputs2 = ")
#print(inputs2.items())


ftoi = {}
index = 1
fmin, fmax = [], []
feats = []
non01feats = set()


def pad(x):
    "Pad input sequence with special BoW and EoW markers."
    padded = ['^']
    padded.extend(x)
    padded.extend(['$'])

    return padded


def getContexts(x, i):
    "Get all contexts in sequence x at position i."
    ret = []
    padx = pad(x)
    # use i + 1 to account for the extra ^ at the beginning
    left = padx[max(0, i + 1 - CONTEXT):i + 1]
    window = left + padx[i + 1:i + 2 + CONTEXT]

    for c in range(0, len(window)):
        for n in range(1, len(window) + 1 - c):
            ret.append((c - len(left), c - len(left) + n - 1,
                        intern(':'.join(window[c:c + n]))))

    return ret


def getTransitions(y, i):
    ret = ''
    for j in range(TRANSITION, -1, -1):
        if i < j:
            ret += '^:'
        else:
            ret += y[i - j] + ':'

    return intern(ret[-1])


def getJointNgrams(x, y, i):
    "Get all joint n-grams up to length n before position i."
    ret = []
    xhistory = x[max(0, i + 1 - JOINT):i]
    yhistory = y[max(0, i + 1 - JOINT):i]

    x_i, y_i = intern(x[i]), intern(y[i])
    ret.append((0, 0, x_i, y_i))

    for c in range(0, len(xhistory)):
        for n in range(1, len(xhistory) + 1 - c):
            ret.append((c - len(xhistory), c - len(xhistory) + n - 1,
                        intern(':'.join(xhistory[c:c + n])),
                        intern(':'.join(yhistory[c:c + n])), x_i, y_i))

    return ret


def addFeat(featset, feat, val, countpass, min=None, max=None):
    global ftoi, index, fmin, fmax, feats

    if feat not in ftoi and countpass:
        ftoi[feat] = index
        fmin.append(min)
        fmax.append(max)
        feats.append(feat)
        if min != 0 or max != 1:
            non01feats.add(ftoi[feat])
        index += 1
    if feat in ftoi:
        i = ftoi[feat]
        j = i - 1
        if countpass:
            try:
                if val < fmin[j]:
                    fmin[j] = val
                if val > fmax[j]:
                    fmax[j] = val
            except TypeError:
                fmin[j] = val
                fmax[j] = val
        else:
            if i in non01feats:
                featset.add((i, (val - fmin[j]) / (fmax[j] - fmin[j])))
            else:
                featset.add((i, val))


def featLine(data):
    for i in non01feats - set(feat[0] for feat in data):
        j = i - 1
        data.add((i, (0 - fmin[j]) / (fmax[j] - fmin[j])))

    ret = ''
    for feat in sorted(data, key=itemgetter(0)):
        rounded = round(feat[1], 8)
        if rounded != 0:
            ret += '{}:{:.8g} '.format(feat[0], rounded)

    return ret[:-1]


def processData(ilist, inp, outp, countpass):
    qid = 0
    for en in ilist:
        if options.useMRR:
            rank = 1.0
            for ph, correct, stuff in inp[en]:
                stuff[2] = 1.0 / rank
                rank += 1.0

        qid += 1
        for ph, correct, stuff in inp[en]:
            featset = set()
            # score features
            smin, smax1, smax2 = None, None, None
            for p in range(2, len(stuff), 3):
                if options.scores or p == 2:
                    # the score itself
                    if stuff[p] == 'NULL':
                        f = -5000.0
                    else:
                        f = float(stuff[p])
                    if f < options.limit:
                        f = options.limit
                    addFeat(featset, (p,), f, countpass, smin, smax1)

                    # differences between this score and the others
                    if options.diffs:
                        s = 0
                        for ph2, correct2, stuff2 in inp[en]:
                            s += 1
                            if stuff2[p] == 'NULL':
                                f2 = -5000.0
                            else:
                                f2 = float(stuff2[p])
                            if f2 < options.limit:
                                f2 = options.limit
                            addFeat(featset, (p, s), f - f2, countpass, smin,
                                    smax2)

                    smin = float(options.limit)
                    smax1 = 0.0
                    smax2 = float(-options.limit)

            # n-gram based features
            if anyNGramFeatures:
                p_i = 0 if options.salign else 3
                for p in range(p_i, len(stuff), 3):
                    xsplit = stuff[p].replace('_', '')[:-1].split('|')
                    ysplit = stuff[p + 1].replace('_', '')[:-1].split('|')
                    if len(xsplit) != len(ysplit):
                        errordie('alignment mismatch: {}'.format(stuff))
                    # check for no-alignment
                    # note that above I chop off the last character so here I
                    # check for NALG instead of NALGN
                    if 'NALG' in xsplit or 'NALG' in ysplit:
                        if len(xsplit) != 1 or len(ysplit) != 1:
                            errordie('problem with NALGN: {}'.format(stuff))
                        addFeat(featset, (p, intern('NALGN')), 1, countpass, 0,
                                1)
                    # similarly, check for NUL instead of NULL
                    elif 'NUL' not in xsplit and 'NUL' not in ysplit:
                        for i in range(len(xsplit)):
                            if options.context or options.lchain:
                                xcontexts = getContexts(xsplit, i)

                            if options.rcontext or options.rlchain:
                                ycontexts = getContexts(ysplit, i)

                            # context features
                            if options.context:
                                for context in xcontexts:
                                    addFeat(featset, (p, intern(ysplit[i])) +
                                            context, 1, countpass, 0, 1)

                            # reverse context features
                            if options.rcontext:
                                for context in ycontexts:
                                    addFeat(featset, (p, intern(xsplit[i])) +
                                            context, 1, countpass, 0, 1)

                            # transition features
                            if options.transition:
                                addFeat(featset, (p, getTransitions(ysplit,
                                                                    i)), 1,
                                        countpass, 0, 1)

                            # linear chain features
                            if options.lchain:
                                for context in xcontexts:
                                    addFeat(featset,
                                            (p, getTransitions(ysplit, i)) +
                                            context, 1, countpass, 0, 1)

                            # reverse linear chain features
                            if options.rlchain:
                                for context in ycontexts:
                                    addFeat(featset,
                                            (p, getTransitions(xsplit, i)) +
                                            context, 1, countpass, 0, 1)

                            # joint n-gram features
                            if options.joint:
                                for joint in getJointNgrams(xsplit, ysplit, i):
                                    addFeat(featset, (p,) + joint, 1,
                                            countpass, 0, 1)

            if outp:
                rank = '2' if correct else '1'
                outset = (rank, 'qid:{}'.format(qid), featLine(featset), '#',
                          str(stuff))
                outp.write(' '.join(outset) + '\n')

processData(inplist, inputs, None, True)

with open(args[2], 'w') as out:
    processData(inplist, inputs, out, False)
with open(args[5], 'w') as out:
    processData(inplist2, inputs2, out, False)
