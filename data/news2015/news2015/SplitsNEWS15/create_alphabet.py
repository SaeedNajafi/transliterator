import sys

in_file = open(sys.argv[1], 'r')

src_file = open(sys.argv[2], 'w')
trg_file = open(sys.argv[3], 'w')

lines = in_file.readlines()

src = []
trg = []
for line in lines:
	s, t = line.strip().split('\t')
	for each_s in list(s.strip()):
		if each_s not in src:
			src.append(each_s)
	for each_t in list(t.strip()):
                if each_t not in trg:
                        trg.append(each_t)


in_file.close()

for each in src:
	src_file.write(each + '\n')

for each in trg:
	trg_file.write(each + '\n')

src_file.close()
trg_file.close()

