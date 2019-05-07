import sys
from .field_dimension import FieldDimension


def parse_field_dimensions(field_dimensions_str):
    """"
    group column with same dimension together.
    :param argv: the format of field dimensions are "1,3,4-7=dim 2,5=dim", where 1, 3, 4-7 are column indexes
    :return: dictionary with [FieldDimension(dimension, indexes),...,FieldDimension(dimension, indexes)]
    """
    field_dimensions_list = field_dimensions_str.split()
    r = []
    for item in field_dimensions_list:
        indexes, dimension = item.split('=')
        r.append(FieldDimension.to_field_dimension(dimension, indexes))

    return r


def shift_dimension(sparse_vector_str, offset):
    # return immediately
    if offset == 0:
        return sparse_vector_str

    sparse_vector = sparse_vector_str.split()
    r = []
    for vect in sparse_vector:
        idx, value = vect.split(':')
        idx = int(idx) + offset
        item_str = '%s:%s' % (idx, value)
        r.append(item_str)
    return ' '.join(r)


def process_one_field(field, items):
    d = 0
    r = []
    for idx in field.indexes:
        start = idx[0]
        end = idx[1] if len(idx) > 1 else idx[0]
        while start <= end:
            r.append(shift_dimension(items[start], d))
            d += field.dimension
            start += 1
    return d, ' '.join(r)


def isIndexInFieldDimensions(i, field_dimensions):
    for f in field_dimensions:
        for idxes in f.indexes:
            end = idxes[1] if len(idxes) > 1 else idxes[0]
            if idxes[0] <= i <= end:
                return True
    return False


def find_unspecified_fields(line, field_dimensions):
    items = line.split('\t')
    dimension = 1
    last = -1
    start = -1
    r = []
    for i in range(len(items)):
        if isIndexInFieldDimensions(i, field_dimensions):
            continue

        if start < 0:
            start = i

        if last < 0:
            pass
        elif i == last + 1:
            pass
        else:
            if last >= start and last >= start:
                r.append((start, last))
            start = i
        last = i

    # add the last one
    if start >= 0 and last >= start:
        r.append((start, last))
    return FieldDimension(dimension, r)


def copy_fields(items, fields):
    r = []
    for idx in fields.indexes:
        start = idx[0]
        end = idx[1] if len(idx) > 1 else idx[0]
        while start <= end:
            r.append(items[start])
            start += 1

    return r


def process_line(line, field_dimensions, unspecified_fields):
    items = line.split('\t')

    result = copy_fields(items, unspecified_fields)

    d = 0
    r = []
    for f in field_dimensions:
        dimension, value = process_one_field(f, items)
        r.append(shift_dimension(value, d))
        d += dimension
    str_v = ' '.join(r)

    result.append(str_v)
    return result


def process_file(ifile, ofile, field_dimensions, print_freq):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if i == 0:
                unspecified_fields = find_unspecified_fields(line, field_dimensions)
                print('Unspecified fields are', unspecified_fields)
            items = process_line(line, field_dimensions, unspecified_fields)
            if i % print_freq == 0:
                print('Processing line %d' % i)
            out.write("%s\n" % '\t'.join(items))


if __name__ == "__main__":
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    field_dimensions_str = sys.argv[3]
    print('field dimension str are', sys.argv[3])

    print_freq = 1000
    if len(sys.argv) > 4:
        print_freq = int(sys.argv[4])
    print('Print frequency is', print_freq)

    field_dimensions = parse_field_dimensions(field_dimensions_str)
    print('field dimensions are [%s]' % ','.join([str(f) for f in field_dimensions]))

    process_file(ifile, ofile, field_dimensions, print_freq)
