import sys
import re
from dateutil.parser import parse


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_email_address(txt):
    return EMAIL_REGEX.match(txt)


def is_tax_flags(txt):
    return txt.endswith("NNNNNNN")


def is_date(txt):
    try:
        parse(txt)
        return True
    except ValueError:
        return False


def is_large_number(txt):
    try:
        f = float(txt)
        if f > 1.0e7:
            return True
    except ValueError:
        pass
    return False


COLUMNS_FOR_OFFSET = {
    'TaxFlags': is_tax_flags,
}

COL_IDX = {}

COLUMNS_TO_CHECK = {
    'Email': is_email_address,
    'DateOpened': is_date,
    'LastUpdate' : is_date,
    'ValidFrom': is_date,
    'ValidUntil': is_date,
}


def find_offset(items, cols_for_offset, col_idx, max_offset=5):
    for c, fun in cols_for_offset.items():
        idea_idx = col_idx[c]
        start = max(idea_idx - max_offset, 0)
        end = min(idea_idx+max_offset, len(items))
        for i in range(start, end):
            if fun(items[i]):
                return i - idea_idx
    raise Exception(f"Can't find valid item in {items}")


def is_valid_row(items, offset, cols_to_check, col_idx):
    for c, fun in cols_to_check.items():
        idea_idx = col_idx[c]
        true_idx = idea_idx + offset
        if not fun(items[true_idx]):
            raise Exception(f"Invalid item {items[true_idx]} at {true_idx} = {idx} - {offset}")
    return True


EXCLUDE_COLS = range(2, 13)


def process_header(line, sep=","):
    cols = line.split(sep=sep)
    new_cols = []
    for i, col in enumerate(cols):
        if i in EXCLUDE_COLS:
            continue
        COL_IDX[col] = i
        new_cols.append(col)
    print('BBB', COL_IDX)
    return new_cols


def process_line(line, sep=",", safe_cols=2):
    items = line.split(sep=sep)
    offset = find_offset(items, COLUMNS_FOR_OFFSET, COL_IDX)

    new_items = []
    for col, pos in COL_IDX.items():
        if pos < safe_cols:
            true_idx = pos
        else:
            true_idx = pos + offset
        item = items[true_idx]
        new_items.append(item)
        if col in COLUMNS_TO_CHECK:
            fun = COLUMNS_TO_CHECK[col]
            if not fun(item):
                raise Exception(f"Failed to pass validation at {true_idx} {offset} for {line}")
    return new_items


def process_file(ifile, ofile, num_line_print, out_sep='\t'):
    print('loading input data from file %s' % ifile)
    print('writing output to file %s' % ofile)
    with open(ofile, 'w', encoding='utf-8') as out, open(ifile, 'r', ) as f:
        for i, line in enumerate(f):
            try:
                line = line.rstrip()
                if i == 0:
                    items = process_header(line)
                else:
                    items = process_line(line)
                if i % num_line_print == 0:
                    print(f'Processing line {i}')
                out.write("%s\n" % out_sep.join(items))
            except Exception as e:
                print(f"Caught error at {i} {e}")


if __name__ == "__main__":
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    num_line_print = 1000

    process_file(ifile, ofile, num_line_print)
