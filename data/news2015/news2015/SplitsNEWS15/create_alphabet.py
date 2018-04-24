import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

train_file = codecs.open(sys.argv[1], 'r', 'utf-8')
dev_file = codecs.open(sys.argv[2], 'r', 'utf-8')

src_file = codecs.open(sys.argv[3], 'w', 'utf-8')
trg_file = codecs.open(sys.argv[4], 'w', 'utf-8')

src = []
trg = []

lines = train_file.readlines()
for line in lines:
	s, t = line.strip().split('\t')
	for each_s in list(s):
		if each_s not in src:
			src.append(each_s)
	for each_t in list(t):
		if each_t not in trg:
			trg.append(each_t)

train_file.close()

lines = dev_file.readlines()
for line in lines:
	s, t = line.strip().split('\t')
	for each_s in list(s):
		if each_s not in src:
			src.append(each_s)
	for each_t in list(t):
		if each_t not in trg:
			trg.append(each_t)

dev_file.close()

for each in src:
	src_file.write(each + '\n')

for each in trg:
	trg_file.write(each + '\n')

src_file.close()
trg_file.close()
