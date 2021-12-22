# -*- coding: UTF-8 -*-

# See file COPYING distributed with python-unf for copyright and license.

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
        u = unf.unf(None)
        self.assertEqual(u, 'UNF:6:cJ6AyISHokEeHuTfufIqhg==')
        return

    def test_true(self):
        u1 = unf.unf(True)
        u2 = unf.unf(1)
        self.assertEqual(u1, u2)
        return

    def test_false(self):
        u1 = unf.unf(False)
        u2 = unf.unf(0)
        self.assertEqual(u1, u2)
        return

    def test_string(self):
        u = unf.unf('A character String')
        self.assertEqual(u, 'UNF:6:FYqU7uBl885eHMbpco1ooA==')
        return

    def test_long_string(self):
        u = unf.unf('A quite long character string, so long that the ' + \
                    'number of characters in it happens to be more ' + \
                    'than the default cutoff limit of 128.')
        self.assertEqual(u, 'UNF:6:/BoSlfcIlsmQ+GHu5gxwEw==')
        return

    def test_unicode(self):
        u = unf.unf(u'på Færøerne')
        self.assertEqual(u, 'UNF:6:KHM6bKVaVaxWDDsmyerfDA==')
        return

    def test_empty_string(self):
        u = unf.unf('')
        self.assertEqual(u, 'UNF:6:ECtRuXZaVqPomffPDuOOUg==')
        return

    def test_nan(self):
        u = unf.unf(float('NaN'))
        self.assertEqual(u, 'UNF:6:GNcR8/UCnImaPpw47gdPNg==')
        return

    def test_pos_inf(self):
        u = unf.unf(float('+Inf'))
        self.assertEqual(u, 'UNF:6:MdAI70WZdDHnu6qmkpqUQg==')
        return

    def test_neg_inf(self):
        u = unf.unf(float('-Inf'))
        self.assertEqual(u, 'UNF:6:A7orv3pgAhljFnGjQVLCog==')
        return

    def test_pos_zero(self):
        u = unf.unf(0.0)
        self.assertEqual(u, 'UNF:6:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_neg_zero(self):
        u = unf.unf(-0.0)
        self.assertEqual(u, 'UNF:6:qDM4PMUq1cMW+bqfBLBGZg==')
        return

    def test_value_1(self):
        u = unf.unf(0)
        self.assertEqual(u, 'UNF:6:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_value_2(self):
        u = unf.unf(1)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_value_3(self):
        u = unf.unf(-300)
        self.assertEqual(u, 'UNF:6:ZTXyg54FoMfRDWZl6oWmFQ==')
        return

    def test_value_4(self):
        u = unf.unf(3.1415)
        self.assertEqual(u, 'UNF:6:vOSZmXXXpKfQcqZ0Cuu5/w==')
        return

    def test_value_5(self):
        u = unf.unf(0.00073)
        self.assertEqual(u, 'UNF:6:qhw3qzg3fEK0NNfoVxk4jQ==')
        return

    def test_value_6(self):
        u = unf.unf(1.2345675)
        self.assertEqual(u, 'UNF:6:vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_7(self):
        u = unf.unf(1.2345685)
        self.assertEqual(u, 'UNF:6:vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_8(self):
        # see README.rounding
        u = unf.unf(1.2345635)
        self.assertEqual(u, 'UNF:6:auhsR5DIScLiAUb/SA2YVA==')
        return

    def test_value_9(self):
        # see README.rounding
        u = unf.unf(1.2345645)
        self.assertEqual(u, 'UNF:6:auhsR5DIScLiAUb/SA2YVA==')
        return

    def test_value_10(self):
        # see README.rounding; this tests _nn() scaling down
        u = unf.unf(12345635)
        self.assertEqual(u, 'UNF:6:qnKXlm182LZPFz9JzxTiNg==')
        return

    def test_value_11(self):
        # see README.rounding; this tests _nn() scaling down
        u = unf.unf(12345645)
        self.assertEqual(u, 'UNF:6:qnKXlm182LZPFz9JzxTiNg==')
        return

    def test_vector(self):
        u = unf.unf((1.23456789, None, 0))
        self.assertEqual(u, 'UNF:6:Do5dfAoOOFt4FSj0JcByEw==')
        return

    def test_vector_2(self):
        u = unf.unf([1.23456789, None, 0])
        self.assertEqual(u, 'UNF:6:Do5dfAoOOFt4FSj0JcByEw==')
        return

    def test_vector_3(self):
        with self.assertRaises(TypeError):
            unf.unf([1, [1.23456789, None, 0]])
        return

class TestDigits(unittest.TestCase):

    # ---------------------------------------------------------
    # type and value checking

    def test_type(self):
        with self.assertRaises(TypeError):
            unf.unf('', digits='')
        return

    def test_value(self):
        with self.assertRaises(ValueError):
            unf.unf('', digits=0)
        return

    # ---------------------------------------------------------
    # the following should be unaffected by digits=2

    def test_missing(self):
        u = unf.unf(None, digits=2)
        self.assertEqual(u, 'UNF:6:N2:cJ6AyISHokEeHuTfufIqhg==')
        return

    def test_string(self):
        u = unf.unf('A character String', digits=2)
        self.assertEqual(u, 'UNF:6:N2:FYqU7uBl885eHMbpco1ooA==')
        return

    def test_nan(self):
        u = unf.unf(float('NaN'), digits=2)
        self.assertEqual(u, 'UNF:6:N2:GNcR8/UCnImaPpw47gdPNg==')
        return

    def test_pos_inf(self):
        u = unf.unf(float('+Inf'), digits=2)
        self.assertEqual(u, 'UNF:6:N2:MdAI70WZdDHnu6qmkpqUQg==')
        return

    def test_neg_inf(self):
        u = unf.unf(float('-Inf'), digits=2)
        self.assertEqual(u, 'UNF:6:N2:A7orv3pgAhljFnGjQVLCog==')
        return

    def test_pos_zero(self):
        u = unf.unf(0.0, digits=2)
        self.assertEqual(u, 'UNF:6:N2:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_neg_zero(self):
        u = unf.unf(-0.0, digits=2)
        self.assertEqual(u, 'UNF:6:N2:qDM4PMUq1cMW+bqfBLBGZg==')
        return

    def test_value_1(self):
        u = unf.unf(0, digits=2)
        self.assertEqual(u, 'UNF:6:N2:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_value_2(self):
        u = unf.unf(1, digits=2)
        self.assertEqual(u, 'UNF:6:N2:tv3XYCv524AfmlFyVOhuZg==')
        return

    # ---------------------------------------------------------
    # value tests, including header checks

    def test_value_3(self):
        u = unf.unf(1.2345678, digits=6)
        self.assertEqual(u, 'UNF:6:N6:Z8pf0CubsQBVtRiOQLQNVA==')
        return

    def test_value_4(self):
        # no N in UNF header (default digits)
        u = unf.unf(1.2345678, digits=7)
        self.assertEqual(u, 'UNF:6:vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_5(self):
        u = unf.unf(1.2345678, digits=8)
        self.assertEqual(u, 'UNF:6:N8:TCfkDjJvqAJ7wy4sdQFRaw==')
        return

    def test_value_6(self):
        # same as digits=8 (we've run out of siginficant digits in the data)
        u = unf.unf(1.2345678, digits=9)
        self.assertEqual(u, 'UNF:6:N9:TCfkDjJvqAJ7wy4sdQFRaw==')
        return

@unittest.skipIf(not numpy, 'numpy not installed')
class TestNumpy(unittest.TestCase):

    def test(self):
        t = (None, True, 2, 3.4, '5.6.7')
        u_b = unf.unf(t)
        u_n = unf.unf(numpy.array(t))
        self.assertEqual(u_n, u_b)
        return

    def test_speed(self):
        t = (float('NaN'), float('+Inf'), float('-Inf'), 
             0.0, -0.0, 0, 1, -300, 
             3.1415, 0.00073, 
             1.2345675, 1.2345685, 1.2345635, 1.2345645)
        u_b = unf.unf(t)
        u_n = unf.unf(numpy.array(t))
        self.assertEqual(u_n, u_b)
        return

    def test_matrix(self):
        a = numpy.array(((1, 2, 3), (4, 5, 6)))
        self.assertRaises(ValueError, unf.unf, a)
        return

@unittest.skipIf(not numpy, 'numpy not installed')
class Test071Errors(unittest.TestCase):

    """Versions through 0.7.1 have an error where scaled values
    lose leading zeros after the decimal point.  So 0.9005000798402081
    normalizes to b'+9.5001e-1\n' rather than the correct
    b'+9.005001e-1\n'.  This only happens with values in numpy
    arrays.
    """

    def test_value(self):
        u = unf.unf(numpy.array([0.9005000798402081]))
        self.assertEqual(u, 'UNF:6:8eqCT5VNEgqICh3FnZsImQ==')
        return

# eof
