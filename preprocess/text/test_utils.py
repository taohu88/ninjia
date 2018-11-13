'''
unit test for utils
'''
import unittest
from collections import Counter
from .utils import tri_gram, counter_sum, normalize, jaccard


class TestUtilsMethods(unittest.TestCase):

    def test_normalize(self):
        a = '–‘’“”…abc    .'
        b = normalize(a)
        self.assertEqual(b, '-`\'""...abc .')

    def test_tri_gram(self):
        txt = 'Hello world'
        x = tri_gram(txt.lower())
        expected = Counter({'orl': 1, 'llo': 1, 'ell': 1, 'wor': 1, 'rld': 1, 'o w': 1, ' wo': 1, 'hel': 1, 'lo ': 1})
        self.assertAlmostEqual(x, expected)

    def test_counter_sum(self):
        s = counter_sum({'a': 1, 'b': 2})
        self.assertAlmostEqual(s, 3)

    def test_counter_sum(self):
        x = jaccard('abcd', 'abcdef', tri_gram)
        self.assertAlmostEqual(x, 0.5)


suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilsMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
