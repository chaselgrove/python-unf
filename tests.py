# -*- coding: UTF-8 -*-

# See file COPYING distributed with unf for copyright and license.

import unittest
import unf

try:
    import numpy
except ImportError:
    numpy = None

# test source is 
# https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
# with help from the UNF R package (version 2.0.5)
# and http://guides.dataverse.org/en/latest/developers/unf/unf-v6.html

class TestUNFs(unittest.TestCase):

    def test_missing(self):
        u = unf.UNF(None)
        self.assertEqual(u.unf, 'cJ6AyISHokEeHuTfufIqhg==')
        return

    def test_true(self):
        u_t = unf.UNF(True)
        u_1 = unf.UNF(1)
        self.assertEqual(u_t.unf, u_1.unf)
        return

    def test_false(self):
        u_f = unf.UNF(False)
        u_0 = unf.UNF(0)
        self.assertEqual(u_f.unf, u_0.unf)
        return

    def test_string(self):
        u = unf.UNF('A character String')
        self.assertEqual(u.unf, 'FYqU7uBl885eHMbpco1ooA==')
        return

    def test_long_string(self):
        u = unf.UNF('A quite long character string, so long that the ' + \
                    'number of characters in it happens to be more ' + \
                    'than the default cutoff limit of 128.')
        self.assertEqual(u.unf, '/BoSlfcIlsmQ+GHu5gxwEw==')
        return

    def test_unicode(self):
        u = unf.UNF(u'på Færøerne')
        self.assertEqual(u.unf, 'KHM6bKVaVaxWDDsmyerfDA==')
        return

    def test_empty_string(self):
        u = unf.UNF('')
        self.assertEqual(u.unf, 'ECtRuXZaVqPomffPDuOOUg==')
        return

    def test_nan(self):
        u = unf.UNF(float('NaN'))
        self.assertEqual(u.unf, 'GNcR8/UCnImaPpw47gdPNg==')
        return

    def test_pos_inf(self):
        u = unf.UNF(float('+Inf'))
        self.assertEqual(u.unf, 'MdAI70WZdDHnu6qmkpqUQg==')
        return

    def test_neg_inf(self):
        u = unf.UNF(float('-Inf'))
        self.assertEqual(u.unf, 'A7orv3pgAhljFnGjQVLCog==')
        return

    def test_pos_zero(self):
        u = unf.UNF(0.0)
        self.assertEqual(u.unf, 'YUvj33xEHnzirIHQyZaHow==')
        return

    def test_neg_zero(self):
        u = unf.UNF(-0.0)
        self.assertEqual(u.unf, 'qDM4PMUq1cMW+bqfBLBGZg==')
        return

    def test_value_1(self):
        u = unf.UNF(0)
        self.assertEqual(u.unf, 'YUvj33xEHnzirIHQyZaHow==')
        return

    def test_value_2(self):
        u = unf.UNF(1)
        self.assertEqual(u.unf, 'tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_value_3(self):
        u = unf.UNF(-300)
        self.assertEqual(u.unf, 'ZTXyg54FoMfRDWZl6oWmFQ==')
        return

    def test_value_4(self):
        u = unf.UNF(3.1415)
        self.assertEqual(u.unf, 'vOSZmXXXpKfQcqZ0Cuu5/w==')
        return

    def test_value_5(self):
        u = unf.UNF(0.00073)
        self.assertEqual(u.unf, 'qhw3qzg3fEK0NNfoVxk4jQ==')
        return

    def test_value_6(self):
        u = unf.UNF(1.2345675)
        self.assertEqual(u.unf, 'vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_7(self):
        u = unf.UNF(1.2345685)
        self.assertEqual(u.unf, 'vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_8(self):
        # see README.rounding
        u = unf.UNF(1.2345635)
        self.assertEqual(u.unf, 'auhsR5DIScLiAUb/SA2YVA==')
        return

    def test_value_9(self):
        # see README.rounding
        u = unf.UNF(1.2345645)
        self.assertEqual(u.unf, 'auhsR5DIScLiAUb/SA2YVA==')
        return

    def test_vector(self):
        u = unf.UNF((1.23456789, None, 0))
        self.assertEqual(u.unf, 'Do5dfAoOOFt4FSj0JcByEw==')
        return

    def test_vector_2(self):
        u = unf.UNF([1.23456789, None, 0])
        self.assertEqual(u.unf, 'Do5dfAoOOFt4FSj0JcByEw==')
        return

    def test_vector_3(self):
        with self.assertRaises(TypeError):
            unf.UNF([1, [1.23456789, None, 0]])
        return

class TestDigits(unittest.TestCase):

    # ---------------------------------------------------------
    # type and value checking

    def test_type(self):
        with self.assertRaises(TypeError):
            unf.UNF('', digits='')
        return

    def test_value(self):
        with self.assertRaises(ValueError):
            unf.UNF('', digits=0)
        return

    # ---------------------------------------------------------
    # the following should be unaffected by digits=2

    def test_missing(self):
        u = unf.UNF(None, digits=2)
        self.assertEqual(u.unf, 'cJ6AyISHokEeHuTfufIqhg==')
        return

    def test_string(self):
        u = unf.UNF('A character String', digits=2)
        self.assertEqual(u.unf, 'FYqU7uBl885eHMbpco1ooA==')
        return

    def test_nan(self):
        u = unf.UNF(float('NaN'), digits=2)
        self.assertEqual(u.unf, 'GNcR8/UCnImaPpw47gdPNg==')
        return

    def test_pos_inf(self):
        u = unf.UNF(float('+Inf'), digits=2)
        self.assertEqual(u.unf, 'MdAI70WZdDHnu6qmkpqUQg==')
        return

    def test_neg_inf(self):
        u = unf.UNF(float('-Inf'), digits=2)
        self.assertEqual(u.unf, 'A7orv3pgAhljFnGjQVLCog==')
        return

    def test_pos_zero(self):
        u = unf.UNF(0.0, digits=2)
        self.assertEqual(u.unf, 'YUvj33xEHnzirIHQyZaHow==')
        return

    def test_neg_zero(self):
        u = unf.UNF(-0.0, digits=2)
        self.assertEqual(u.unf, 'qDM4PMUq1cMW+bqfBLBGZg==')
        return

    def test_value_1(self):
        u = unf.UNF(0, digits=2)
        self.assertEqual(u.unf, 'YUvj33xEHnzirIHQyZaHow==')
        return

    def test_value_2(self):
        u = unf.UNF(1, digits=2)
        self.assertEqual(u.unf, 'tv3XYCv524AfmlFyVOhuZg==')
        return

    # ---------------------------------------------------------
    # value tests, including header checks

    def test_value_3(self):
        u = unf.UNF(1.2345678, digits=6)
        self.assertEqual(u.unf, 'Z8pf0CubsQBVtRiOQLQNVA==')
        self.assertEqual(u.formatted, 'UNF:6:N6:Z8pf0CubsQBVtRiOQLQNVA==')
        return

    def test_value_4(self):
        # no N in UNF header (default digits)
        u = unf.UNF(1.2345678, digits=7)
        self.assertEqual(u.unf, 'vcKELUSS4s4k1snF4OTB9A==')
        self.assertEqual(u.formatted, 'UNF:6:vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_5(self):
        u = unf.UNF(1.2345678, digits=8)
        self.assertEqual(u.unf, 'TCfkDjJvqAJ7wy4sdQFRaw==')
        self.assertEqual(u.formatted, 'UNF:6:N8:TCfkDjJvqAJ7wy4sdQFRaw==')
        return

    def test_value_6(self):
        # same as digits=8 (we've run out of siginficant digits in the data)
        u = unf.UNF(1.2345678, digits=9)
        self.assertEqual(u.unf, 'TCfkDjJvqAJ7wy4sdQFRaw==')
        self.assertEqual(u.formatted, 'UNF:6:N9:TCfkDjJvqAJ7wy4sdQFRaw==')
        return

@unittest.skipIf(not numpy, 'numpy not installed')
class TestNumpy(unittest.TestCase):

    def test(self):
        t = (None, True, 2, 3.4, '5.6.7')
        u_b = unf.UNF(t)
        u_n = unf.UNF(numpy.array(t))
        self.assertEqual(u_n.unf, u_b.unf)
        return

    def test_speed(self):
        t = (float('NaN'), float('+Inf'), float('-Inf'), 
             0.0, -0.0, 0, 1, -300, 
             3.1415, 0.00073, 
             1.2345675, 1.2345685, 1.2345635, 1.2345645)
        u_b = unf.UNF(t)
        u_n = unf.UNF(numpy.array(t))
        self.assertEqual(u_n.unf, u_b.unf)
        return

    def test_matrix(self):
        a = numpy.array(((1, 2, 3), (4, 5, 6)))
        self.assertRaises(ValueError, unf.UNF, a)
        return

# eof
