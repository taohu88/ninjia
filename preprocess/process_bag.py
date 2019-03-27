import sys
import json
from collections import Counter
from random import choice
import fire


def process_head(line, sep):
    items = line.split(sep)
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



def process_file(ifile, ofile, sep=';', has_header=1, print_freq=1000):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if has_header and i == 0:
                items = process_head(line, sep)
                items = ["Label"] + items[2:]
                out.write("%s\n" % sep.join(items))
            else:
                items = process_line(line, sep)
                tags = items[3].split("|")
                for tag in tags:
                    r = [str(1), items[2], tag] + items[4:]
                    out.write("%s\n" % sep.join(r))

            if i % print_freq == 0:
                print('Processing line %d' % i)


if __name__ == '__main__':
  fire.Fire(process_file)

