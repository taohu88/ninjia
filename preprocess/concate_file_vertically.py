import sys

ifile1 = sys.argv[1]
ifile2 = sys.argv[2]
ofile = sys.argv[3]

with open(ofile, 'w', encoding='utf-8') as out, \
        open(ifile1, encoding='utf-8') as f1, open(ifile2, encoding='utf-8') as f2:
    for line1, line2 in zip(f1, f2):
        out.write("%s\t%s\n" % (line1.rstrip(), line2.rstrip()))