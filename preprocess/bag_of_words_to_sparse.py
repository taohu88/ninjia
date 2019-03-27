import sys
import json
from .field_index import FieldIndex
from collections import Counter


def parse_field_indexes(fields):
    """"
    :param argv: the format of argv will look like 1,3,4-7, where 1, 3, 4-7 are column indexes
    :return: FieldIndex(name, (1), (3), (4, 7))
    """
    name = 'Dummy'
    return FieldIndex.to_filed_index(name, fields)


def process_one_column(item, dictionary, unknown, sep, weight_sep):
    terms = item.split(sep)
    r = []
    for i, t in enumerate(terms):
        x = t.split(weight_sep)
        if not x[0]:
            continue

        k = x[0] if x[0] in dictionary else unknown
        k = dictionary[k]
        if len(x) > 1:
            r.append('%s:%s' % (k, x[1]))
        else:
            r.append('%s:%s' % (k, 1))
    return ' '.join(r)


def process_line(line, dictionary, unknown, field_indexes, sep, weight_sep):
    items = line.split('\t')
    # copy the result first
    r = items[:]
    for s, e in field_indexes.values:
        i = s
        while i <= e:
            item = process_one_column(items[i], dictionary, unknown, sep, weight_sep)
            r[i] = item
            i += 1
    return '\t'.join(r)


def process_file(ifile, ofile, dictionary, field_indexes, has_header=1,\
                 sep=',', weight_sep=':', unknown='<unknown>', print_freq=1000):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if has_header and i == 0:
                continue

            new_line = process_line(line, dictionary, unknown, field_indexes, sep, weight_sep)
            if i % print_freq == 0:
                print('Processing line %d' % i)

            out.write("%s\n" % new_line)


def load_dictionary(dictionary_file):
    dictionary = {}
    with open(dictionary_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            term, _ = line.split('\t')
            dictionary[term] = i
    return dictionary


if __name__ == "__main__":
    ifile = sys.argv[1]
    print('Input file is', ifile)

    dictionary_file = sys.argv[2]
    print('Input dictionary is', dictionary_file)
    dictionary = load_dictionary(dictionary_file)
    print('Dictionary is', dictionary)

    ofile = sys.argv[3]
    print('output file is', ofile)

    fields = sys.argv[4]
    print('field args is', fields)
    field_indexes = parse_field_indexes(fields)
    print('field indexes are [%s]' % field_indexes)

    has_header = True if int(sys.argv[5]) else False
    print('Tsv file has header %s' % has_header)

    sep = ','
    if len(sys.argv) > 6:
        sep = sys.argv[6]
    print('seperator is', sep)

    weight_sep = ':'
    if len(sys.argv) > 7:
        weight_sep = sys.argv[7]
    print('weigth seperator is', weight_sep)

    unknown = '<unknown>'
    if len(sys.argv) > 8:
        unknown = sys.argv[8]
    print('unknown term is', unknown)

    print_freq = 1000
    if len(sys.argv) > 9:
        print_freq = int(sys.argv[9])
    print('Print frequency is', print_freq)

    process_file(ifile, ofile, dictionary, field_indexes, has_header=has_header,\
                 sep=sep, weight_sep=weight_sep, unknown=unknown, print_freq=print_freq)



