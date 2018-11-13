import sys
import json


def extract_json_from_str(obj, node_path):
    nodes = node_path.split('/')
    # we already parse the root, which is empty
    for node in nodes[1:]:
        j_str = obj[node]
        obj = json.loads(j_str, encoding='utf-8')
    return obj

def flatten_value_dictionary_to_str(valueMap):
    r = ['%s:%s' % (k, v['Count'][0]) for k, v in valueMap.items()]
    return ','.join(r)


def transform_json(json_str, transform_columns):
    obj = json.loads(json_str, encoding='utf-8')

    nodes = transform_columns
    r = []
    for node in nodes:
        topicObj = extract_json_from_str(obj, '/FeaturesMap/' + node)
        valueMap = topicObj["NumberDictionaryMapList"]
        topicStr = flatten_value_dictionary_to_str(valueMap)
        # print('AAA', node, topicStr)
        r.append(topicStr)
    return r


def process_line(line, input_column_idx, transform_columns, keep_old_column):
    items = line.split('\t')
    if keep_old_column:
        r = items
    else:
        r = items[:input_column_idx] + items[input_column_idx+1:]
    r = r + transform_json(items[input_column_idx], transform_columns)
    return '\t'.join(r)


def process_header(line, input_column_idx, transform_columns, keep_old_column):
    items = line.split('\t')
    if keep_old_column:
        r = items
    else:
        r = items[:input_column_idx] + items[input_column_idx+1:]
    r = r + transform_columns
    return '\t'.join(r)


def process_file(ifile, ofile, input_column_idx, transform_columns, has_header, keep_old_column, print_freq):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.rstrip()
            if has_header and i == 0:
                output_line = process_header(line, input_column_idx, transform_columns, keep_old_column)
            else:
                output_line = process_line(line, input_column_idx, transform_columns, keep_old_column)
            if i % print_freq == 0:
                print('Processing line %d' % i)
            out.write("%s\n" % output_line)


if __name__ == "__main__":
    ifile = sys.argv[1]
    print('Input file is', ifile)

    ofile = sys.argv[2]
    print('output file is', ofile)

    input_column_idx = int(sys.argv[3])
    print('column idex is %s' % input_column_idx)

    transform_columns = ''.join(sys.argv[4].split()).split(',')
    print('transform columns are %s' % transform_columns)

    has_header = True if int(sys.argv[5]) else False
    print('Tsv file has header %s' % has_header)

    keep_old_column = False
    print_freq = int(sys.argv[6])
    print('Prine frequency is', print_freq)

    process_file(ifile, ofile, input_column_idx, transform_columns, has_header, keep_old_column, print_freq)



