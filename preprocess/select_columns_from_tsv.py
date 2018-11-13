import sys
from .field_index import FieldIndex


def parse_field_index(fields_str):
    """"
    :param argv: the format of argv will look like 1,3,4-7, where 1, 3, 4-7 are column indexes
    :return: dictionary with {'Dummy':[(1), (3), (4, 7)]}
    """
    fields_str = ''.join(fields_str.split())

    name = 'Dummy'
    return FieldIndex.to_filed_index(name, fields_str)


def process_one_field(field, items):
    r = []
    for idx in field.values:
        start = idx[0]
        end = idx[1] if len(idx) > 1 else idx[0]
        while start <= end:
            r.append(items[start])
            start += 1
    return '\t'.join(r)


def process_line(line, field_index):
    items = line.split('\t')
    return process_one_field(field_index, items)


def process_file(ifile, ofile, field_index, num_line_print):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            items = process_line(line, field_index)
            if i % num_line_print == 0:
                print('Processing line %d' % i)
            out.write("%s\n" % items)


if __name__ == "__main__":
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    fields_str = sys.argv[3]
    num_line_print = int(sys.argv[4])

    field_index = parse_field_index(fields_str)
    print('field indexes are [%s]' % field_index)

    process_file(ifile, ofile, field_index, num_line_print)
