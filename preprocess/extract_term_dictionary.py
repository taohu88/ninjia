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


def process_one_column(item, sep, weight_sep):
    terms = item.split(sep)
    r = Counter()
    for t in terms:
        x = t.split(weight_sep)
        if len(x) > 1:
            r[x[0]] += float(x[1])
        else:
            r[x[0]] += 1
    return r


def process_line(line, field_indexes, sep, weight_sep):
    items = line.split('\t')

    cnt = Counter()
    for s, e in field_indexes.values:
        i = s
        while i <= e:
            new_cnt = process_one_column(items[i], sep, weight_sep)
            cnt.update(new_cnt)
            i += 1
    return cnt


def process_file(ifile, ofile, field_indexes, max_keep=5000, has_header=1,\
                 sep=',', weight_sep=':', unknown='<unknown>', print_freq=1000):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        cnt = Counter()
        for i, line in enumerate(f):
            line = line.rstrip()
            if has_header and i == 0:
                continue

            new_cnt = process_line(line, field_indexes, sep, weight_sep)
            if i % print_freq == 0:
                print('Processing line %d new terms %s' % (i, new_cnt))
            cnt.update(new_cnt)

        cnt_tuple = cnt.most_common(max_keep)
        if unknown not in cnt:
            out.write("%s\t%d\n" % (unknown, cnt_tuple[0][1] + 1))

        for k, c in cnt_tuple:
            if c < 0:
                continue
            if not k:
                continue
            out.write("%s\t%d\n" % (k, c))


if __name__ == "__main__":
    ifile = sys.argv[1]
    print('Input file is', ifile)

    ofile = sys.argv[2]
    print('output file is', ofile)

    fields = sys.argv[3]
    print('field args is', fields)
    field_indexes = parse_field_indexes(fields)
    print('field indexes are [%s]' % field_indexes)

    has_header = True if int(sys.argv[4]) else False
    print('Tsv file has header %s' % has_header)

    max_keep = int(sys.argv[5])
    print('Max term to keep is %d' % max_keep)

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

    process_file(ifile, ofile, field_indexes, max_keep=max_keep, has_header=has_header,\
                 sep=sep, weight_sep=weight_sep, unknown=unknown, print_freq=print_freq)



