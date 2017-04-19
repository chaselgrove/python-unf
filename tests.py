# -*- coding: UTF-8 -*-

# See file COPYING distributed with unf for copyright and license.

import unittest
import unf

# test source is 
# https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
# with help from the UNF R package (version 2.0.5)

class TestUNFs(unittest.TestCase):

    def test_missing(self):
        u = unf.UNF(None)
        self.assertEqual(u.unf, 'cJ6AyISHokEeHuTfufIqhg==')
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

# eof
