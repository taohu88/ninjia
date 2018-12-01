import sys
import json
from collections import Counter
from random import choice


def process_head(line, sep):
    items = line.split(sep)
    # items = ['Label'] + items
    return items


def process_line(line, sep):
    items = line.split(sep)
    return items


def load_term_dictionary(text_file):
    with open(text_file) as f:
        terms = [line.rstrip() for line in f]

    stoi = {v: k for k, v in enumerate(terms)}
    itos = terms
    return stoi, itos


def process_file(ifile, ofile, sep=',', has_header=1, print_freq=1000):
    stoi, itos = load_term_dictionary('d:/TextClassification/tag_20_term.txt')
    print(stoi, itos)

    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if has_header and i == 0:
                items = process_head(line, sep)
                out.write("%s\n" % sep.join(items))
            else:
                items = process_line(line, sep)
                tags = items[2].split("|")
                pos_tags = set(itos[0] if tag not in stoi else tag for tag in tags)
                for tag in pos_tags:
                    while True:
                        rand_tag = choice(itos)
                        if rand_tag not in pos_tags:
                            break;

                    rank_v = choice([3, 4])
                    r = [str(rank_v), items[1], tag] + items[2:]
                    out.write("%s\n" % sep.join(r))

                    rank_v = choice([0, 1])
                    r = [str(rank_v), items[1], rand_tag] + items[2:]

                    out.write("%s\n" % sep.join(r))

            if i % print_freq == 0:
                print('Processing line %d' % i)



if __name__ == "__main__":
    ifile = sys.argv[1]
    print('Input file is', ifile)

    ofile = sys.argv[2]
    print('output file is', ofile)

    has_header = True if int(sys.argv[3]) else False
    print('Tsv file has header %s' % has_header)

    sep = ','
    if len(sys.argv) > 4:
        sep = sys.argv[4]
    print('seperator is', sep)


    print_freq = 1000
    if len(sys.argv) > 5:
        print_freq = int(sys.argv[5])
    print('Print frequency is', print_freq)

    process_file(ifile, ofile, sep=sep, print_freq=print_freq)



