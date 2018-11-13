import re
from collections import Counter


TRANSLATE_TABLE = {
    ord('–'): '-',
    ord('‘'): '`',
    ord('’'): "'",
    ord('“'): '"',
    ord('”'): '"',
    ord('…'): '...'
}


def normalize(text):
    if not isinstance(text, str):
        return text

    # use re is a different way to do it
    # re.sub(r'\s+', ' ', t)
    t = ' '.join(text.split())
    return t.translate(TRANSLATE_TABLE)


def tri_gram(text):
    """
    :param text:
    :return: return counter of trigram of text
    """
    grams = (''.join(t) for t in zip(text, text[1:], text[2:]))
    return Counter(grams)


def counter_sum(counter):
    """
    :param counter:
    :return: total value from a counter
    """
    return sum(counter.values())


def jaccard(a, b, transform):
    """
    :param a:
    :param b:
    :param transform:
    :return: jaccard distance
    """
    x = transform(a)
    y = transform(b)
    return counter_sum(x & y) / counter_sum(x | y)


def dedupe(a_list):
    """
    :param a_list:
    :return: dedupe of the list with the same order
    """
    r = []
    seen_set = set()
    for t in a_list:
        if t not in seen_set:
            r.append(t)
            seen_set.add(t)
    return r


def clean_docs_and_uniquify(docs):
    """
    normalize docs and uniquify the doc
    :param docs:
    :return:
    """
    docs = [normalize(t) for t in docs if isinstance(t, str)]
    docs = dedupe(docs)
    return docs  

