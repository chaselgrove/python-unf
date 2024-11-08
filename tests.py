# -*- coding: UTF-8 -*-

# See file COPYING distributed with python-unf for copyright and license.

import unittest.mock
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

    def test_large_exponent(self):
        # test a multi-digit exponent
        u = unf.unf(1.234567e150)
        self.assertEqual(u, 'UNF:6:qcKO4c5rvHfQ3nHzqrAS/Q==')
        return

    def test_tiny_exponent(self):
        # test a multi-digit negative exponent
        u = unf.unf(1.234567e-150)
        self.assertEqual(u, 'UNF:6:vbTNUOoynDv6UKxOn36WeQ==')
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

class TestNormalize(unittest.TestCase):

    # These tests match those for unf() above.

    def test_missing(self):
        s = unf.normalize(None)
        self.assertEqual(s, b'\x00\x00\x00')
        return

    def test_true(self):
        s1 = unf.normalize(True)
        s2 = unf.normalize(1)
        self.assertEqual(s1, b'+1.e+\n\x00')
        self.assertEqual(s1, s2)
        return

    def test_false(self):
        s1 = unf.normalize(False)
        s2 = unf.normalize(0)
        self.assertEqual(s1, b'+0.e+\n\x00')
        self.assertEqual(s1, s2)
        return

    def test_string(self):
        s = unf.normalize('A character String')
        self.assertEqual(s, b'A character String\n\x00')
        return

    def test_long_string(self):
        s = unf.normalize('A quite long character string, so long that the ' + \
                    'number of characters in it happens to be more ' + \
                    'than the default cutoff limit of 128.')
        self.assertEqual(s, b'A quite long character string, so long that the number of characters in it happens to be more than the default cutoff limit of 1\n\x00')
        return

    def test_unicode(self):
        s = unf.normalize(u'på Færøerne')
        self.assertEqual(s, b'p\xc3\xa5 F\xc3\xa6r\xc3\xb8erne\n\x00')
        return

    def test_empty_string(self):
        s = unf.normalize('')
        self.assertEqual(s, b'\n\x00')
        return

    def test_nan(self):
        s = unf.normalize(float('NaN'))
        self.assertEqual(s, b'+nan\n\x00')
        return

    def test_pos_inf(self):
        s = unf.normalize(float('+Inf'))
        self.assertEqual(s, b'+inf\n\x00')
        return

    def test_neg_inf(self):
        s = unf.normalize(float('-Inf'))
        self.assertEqual(s, b'-inf\n\x00')
        return

    def test_pos_zero(self):
        s = unf.normalize(0.0)
        self.assertEqual(s, b'+0.e+\n\x00')
        return

    def test_neg_zero(self):
        s = unf.normalize(-0.0)
        self.assertEqual(s, b'-0.e+\n\x00')
        return

    def test_value_1(self):
        s = unf.normalize(0)
        self.assertEqual(s, b'+0.e+\n\x00')
        return

    def test_value_2(self):
        s = unf.normalize(1)
        self.assertEqual(s, b'+1.e+\n\x00')
        return

    def test_value_3(self):
        s = unf.normalize(-300)
        self.assertEqual(s, b'-3.e+2\n\x00')
        return

    def test_value_4(self):
        s = unf.normalize(3.1415)
        self.assertEqual(s, b'+3.1415e+\n\x00')
        return

    def test_value_5(self):
        s = unf.normalize(0.00073)
        self.assertEqual(s, b'+7.3e-4\n\x00')
        return

    def test_value_6(self):
        s = unf.normalize(1.2345675)
        self.assertEqual(s, b'+1.234568e+\n\x00')
        return

    def test_value_7(self):
        s = unf.normalize(1.2345685)
        self.assertEqual(s, b'+1.234568e+\n\x00')
        return

    def test_value_8(self):
        # see README.rounding
        s = unf.normalize(1.2345635)
        self.assertEqual(s, b'+1.234564e+\n\x00')
        return

    def test_value_9(self):
        # see README.rounding
        s = unf.normalize(1.2345645)
        self.assertEqual(s, b'+1.234564e+\n\x00')
        return

    def test_value_10(self):
        # see README.rounding; this tests _nn() scaling down
        s = unf.normalize(12345635)
        self.assertEqual(s, b'+1.234564e+7\n\x00')
        return

    def test_value_11(self):
        # see README.rounding; this tests _nn() scaling down
        s = unf.normalize(12345645)
        self.assertEqual(s, b'+1.234564e+7\n\x00')
        return

    def test_large_exponent(self):
        # test a multi-digit exponent
        s = unf.normalize(1.234567e150)
        self.assertEqual(s, b'+1.234567e+150\n\x00')
        return

    def test_tiny_exponent(self):
        # test a multi-digit negative exponent
        s = unf.normalize(1.234567e-150)
        self.assertEqual(s, b'+1.234567e-150\n\x00')
        return

    def test_vector(self):
        s = unf.normalize((1.23456789, None, 0))
        self.assertEqual(s, b'+1.234568e+\n\x00\x00\x00\x00+0.e+\n\x00')
        return

    def test_vector_2(self):
        s = unf.normalize([1.23456789, None, 0])
        self.assertEqual(s, b'+1.234568e+\n\x00\x00\x00\x00+0.e+\n\x00')
        return

    def test_vector_3(self):
        with self.assertRaises(TypeError):
            unf.normalize([1, [1.23456789, None, 0]])
        return

class TestNormalizeDigits(unittest.TestCase):

    # ---------------------------------------------------------
    # type and value checking

    def test_type(self):
        with self.assertRaises(TypeError):
            unf.normalize('', digits='')
        return

    def test_value(self):
        with self.assertRaises(ValueError):
            unf.normalize('', digits=0)
        return

    # ---------------------------------------------------------
    # the following should be unaffected by digits=2

    def test_missing(self):
        s = unf.normalize(None, digits=2)
        self.assertEqual(s, b'\x00\x00\x00')
        return

    def test_string(self):
        s = unf.normalize('A character String', digits=2)
        self.assertEqual(s, b'A character String\n\x00')
        return

    def test_nan(self):
        s = unf.normalize(float('NaN'), digits=2)
        self.assertEqual(s, b'+nan\n\x00')
        return

    def test_pos_inf(self):
        s = unf.normalize(float('+Inf'), digits=2)
        self.assertEqual(s, b'+inf\n\x00')
        return

    def test_neg_inf(self):
        s = unf.normalize(float('-Inf'), digits=2)
        self.assertEqual(s, b'-inf\n\x00')
        return

    def test_pos_zero(self):
        s = unf.normalize(0.0, digits=2)
        self.assertEqual(s, b'+0.e+\n\x00')
        return

    def test_neg_zero(self):
        s = unf.normalize(-0.0, digits=2)
        self.assertEqual(s, b'-0.e+\n\x00')
        return

    def test_value_1(self):
        s = unf.normalize(0, digits=2)
        self.assertEqual(s, b'+0.e+\n\x00')
        return

    def test_value_2(self):
        s = unf.normalize(1, digits=2)
        self.assertEqual(s, b'+1.e+\n\x00')
        return

    # ---------------------------------------------------------
    # value tests, including header checks

    def test_value_3(self):
        s = unf.normalize(1.2345678, digits=6)
        self.assertEqual(s, b'+1.23457e+\n\x00')
        return

    def test_value_4(self):
        # no N in UNF header (default digits)
        s = unf.normalize(1.2345678, digits=7)
        self.assertEqual(s, b'+1.234568e+\n\x00')
        return

    def test_value_5(self):
        s = unf.normalize(1.2345678, digits=8)
        self.assertEqual(s, b'+1.2345678e+\n\x00')
        return

    def test_value_6(self):
        # same as digits=8 (we've run out of siginficant digits in the data)
        s = unf.normalize(1.2345678, digits=9)
        self.assertEqual(s, b'+1.2345678e+\n\x00')
        return

@unittest.skipIf(not numpy, 'numpy not installed')
class TestNumpy(unittest.TestCase):

    def test_attr(self):
        pass

    def setUp(self):
        super().setUp()
        self._normalize_numpy_array = unf._base._normalize_numpy_array
        unf._base._normalize_numpy_array = unittest.mock.Mock(
            spec=self._normalize_numpy_array, 
            side_effect=self._normalize_numpy_array
        )
        return

    def tearDown(self):
        super().tearDown()
        unf._base._normalize_numpy_array = self._normalize_numpy_array
        return

    def test(self):
        # This is a heterogeneous array so we don't check that numpy 
        # normalization is used, but we do still make sure that the 
        # UNF of the numpy array is correct.
        t = (None, True, 2, 3.4, '5.6.7')
        u_b = unf.unf(t)
        u_n = unf.unf(numpy.array(t))
        self.assertEqual(u_n, u_b)
        return

    def test_speed(self):
        t = (float('NaN'), float('+Inf'), float('-Inf'), 
             0.0, -0.0, 0, 1, -300, 
             3.1415, 0.00073, 
             1.2345675, 1.2345685, 1.2345635, 1.2345645, 
             1.234567e150, 1.234567e-150)
        u_b = unf.unf(t)
        u_n = unf.unf(numpy.array(t))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u_n, u_b)
        return

    def test_matrix(self):
        a = numpy.array(((1, 2, 3), (4, 5, 6)))
        self.assertRaises(ValueError, unf.unf, a)
        return

    # Versions through 0.7.1 have an error where scaled values
    # lose leading zeros after the decimal point.  So 0.9005000798402081
    # normalizes to b'+9.5001e-1\n' rather than the correct
    # b'+9.005001e-1\n'.  This only happens with values in numpy
    # arrays.
    def test_0701_error(self):
        u = unf.unf(numpy.array([0.9005000798402081]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:8eqCT5VNEgqICh3FnZsImQ==')
        return

    # Our numpy optimization introduced some finicky operations in 
    # _normalize_numpy_array(), so we add some extra tests here.
    # Similar to the 0701 test, we introduce zeros in floating point 
    # values and in exponents.

    def test_exp_1(self):
        u = unf.unf(numpy.array([1e0]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_exp_2(self):
        u = unf.unf(numpy.array([1e1]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:o+nTsng0TLIV1N3Dqa2rRA==')
        return

    def test_exp_3(self):
        u = unf.unf(numpy.array([1e10]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:TeER1wBkwE+zvHLxSEmnZA==')
        return

    def test_exp_4(self):
        u = unf.unf(numpy.array([1e100]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:K67V/jah/5UTNdTqNfGNGQ==')
        return

    def test_exp_5(self):
        u = unf.unf(numpy.array([1e101]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:WxchK5DSjOC/vrznE6g5KA==')
        return

    def test_value_1(self):
        u = unf.unf(numpy.array([1.00000001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_value_2(self):
        u = unf.unf(numpy.array([1.10000001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:e7mRzE999g+XdbMRqdnCkA==')
        return

    def test_value_3(self):
        u = unf.unf(numpy.array([1.1]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:e7mRzE999g+XdbMRqdnCkA==')
        return

    def test_value_4(self):
        u = unf.unf(numpy.array([1.100001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:BZsaaf/5tFPpBmWgmIozJw==')
        return

    def test_value_5(self):
        u = unf.unf(numpy.array([1.1000001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:e7mRzE999g+XdbMRqdnCkA==')
        return

    def test_value_6(self):
        u = unf.unf(numpy.array([1.000001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:uTepcVWx1hT/FPAPcmNfzQ==')
        return

    def test_value_7(self):
        u = unf.unf(numpy.array([1.0000001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_value_8(self):
        u = unf.unf(numpy.array([1.00010001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:f2+uKERSm529tncALsUPpg==')
        return

    def test_value_9(self):
        u = unf.unf(numpy.array([1.10010001]))
        self.assertTrue(unf._base._normalize_numpy_array.called)
        self.assertEqual(u, 'UNF:6:+fmO4JH7/DXQI2ay8JUyow==')
        return

# eof
