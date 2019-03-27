import sys
from field_index import FieldIndex


def parse_field_index(fields):
    """"
    :param argv: the format of argv will look like name=1,3,4-7, where 1, 3, 4-7 are column indexes
    :return: dictionary with {name:[(1), (3), (4, 7)]}
    """
    r = []
    for item in fields:
        name, v = item.split('=')
        r.append(FieldIndex.to_filed_index(name, v))

    return r


def process_one_field(field, items):
    r = [field.name]
    for idx in field.values:
        start = idx[0]
        end = idx[1] if len(idx) > 1 else idx[0]
        while start <= end:
            r.append(items[start])
            start += 1
    return '\t'.join(r)


def process_line(line, field_indexes):
    items = line.split('\t')
    return [process_one_field(f, items) for f in field_indexes]


def process_file(ifile, ofile, field_indexes, num_line_print):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            items = process_line(line, field_indexes)
            if i % num_line_print == 0:
                print('Processing line %d' % i)
            out.write("|%s\n" % '\t|'.join(items))


if __name__ == "__main__":
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    fields = sys.argv[3].split()
    num_line_print = int(sys.argv[4])

    field_indexes = parse_field_index(fields)
    print('field indexes are [%s]' % ','.join([str(f) for f in field_indexes]))

    process_file(ifile, ofile, field_indexes, num_line_print)
