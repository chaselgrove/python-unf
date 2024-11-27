# -*- coding: UTF-8 -*-

# See file COPYING distributed with python-unf for copyright and license.

# Many of the tests come from 
# https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
# and 
# https://github.com/IQSS/UNF/tree/master/src/test/resources/test.
# Tests are validated with help from https://github.com/leeper/UNF, 
# https://github.com/IQSS/UNF.git, 
# and http://guides.dataverse.org/en/latest/developers/unf/unf-v6.html.

import unittest.mock
import math

import unf

try:
    import numpy
except ImportError:
    numpy = None

try:
    import pandas
except ImportError:
    pandas = None

class IQSSTests(unittest.TestCase):

    # Tests from 
    # https://github.com/IQSS/UNF/tree/master/src/test/resources/test

    @unittest.skip('pending https://github.com/IQSS/UNF/issues/8')
    def test_boolean(self):
        val = [True, False, True]
        self.assertEqual(unf.unf(val), 'UNF:6:PMaEyvdvyMz7EJV4mr7aZg==')
        return

    def test_double(self):
        val = [6.6666666666666667, 75.216]
        self.assertEqual(unf.unf(val), 'UNF:6:+kc3wyGwZ6otDkZwpvswDw==')
        return

    def test_float(self):
        val = [654.32, 26736.232]
        self.assertEqual(unf.unf(val), 'UNF:6:V2clNd9rUmIG0mhGVmzmVA==')
        return

    def test_int(self):
        val = [32, 2024]
        self.assertEqual(unf.unf(val), 'UNF:6:R2Xa8BqKPRgj5EpnYEZQyw==')
        return

    def test_long(self):
        val = [22, 3892091]
        self.assertEqual(unf.unf(val), 'UNF:6:qu3+pyyv8y0FEhVQueuWuw==')
        return

    def test_short(self):
        val = [247, 34]
        self.assertEqual(unf.unf(val), 'UNF:6:GFy92enld/1lP8pcXq9L6w==')
        return

    def test_string(self):
        val = ['Hello World', 'Testing 123']
        self.assertEqual(unf.unf(val), 'UNF:6:r+FDbVC6fKdUjRS6ZIzP4w==')
        return

class UNFSpecificationTests(unittest.TestCase):

    # Tests from 
    # https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html

    def test_positive_zero_normalization(self):
        val = 0.0
        s = b'+0.e+\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_negative_zero_normalization(self):
        val = -0.0
        s = b'-0.e+\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_positive_inf_normalization(self):
        val = float('+Inf')
        s = b'+inf\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_negative_inf_normalization(self):
        val = float('-Inf')
        s = b'-inf\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_nan_normalization(self):
        val = float('NaN')
        s = b'+nan\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_1_normalization(self):
        val = 1
        s = b'+1.e+\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    # The example in the specification is incorrect.  It says '+3.1415+' 
    # but the '59' should be rounded up to get '+3.1416+'.
    def test_pi_5_digits_normalization(self):
        val = math.pi
        s = b'+3.1416e+\n\0'
        self.assertEqual(unf._normalize(val, 5), s)
        return

    def test_negative_300_normalization(self):
        val = -300
        s = b'-3.e+2\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_73em4_normalization(self):
        val = 0.00073 
        s = b'+7.3e-4\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_1t9_normalization(self):
        val = 1.23456789
        s = b'+1.234568e+\n\0'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_vector(self):
        val = [1.23456789, None, 0]
        s = b'+1.234568e+\n\000\000\000\000+0.e+\n\000'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf.unf(val), 'UNF:6:Do5dfAoOOFt4FSj0JcByEw==')
        return

    def test_1t9_unf(self):
        val = 1.23456789
        u = 'UNF:6:vcKELUSS4s4k1snF4OTB9A=='
        self.assertEqual(unf.unf(val), u)
        return

    def test_1t9_9_digits_unf(self):
        val = 1.23456789
        u = 'UNF:6:N9:IKw+l4ywdwsJeDze8dplJA=='
        self.assertEqual(unf.unf(val, 9), u)
        return

class ExamplesTests(unittest.TestCase):

    # Tests from 
    # https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt

    def test_0(self):
        val = 0
        s = b'+0.e+\n\000'
        d = 'YUvj33xEHnzirIHQyZaHow=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_1(self):
        val = 1
        s = b'+1.e+\n\000'
        d = 'tv3XYCv524AfmlFyVOhuZg=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_m300(self):
        val = -300
        s = b'-3.e+2\n\000'
        d = 'ZTXyg54FoMfRDWZl6oWmFQ=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_pi(self):
        val = 3.1415
        s = b'+3.1415e+\n\000'
        d = 'vOSZmXXXpKfQcqZ0Cuu5/w=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_73em4(self):
        val = 0.00073
        s = b'+7.3e-4\n\000'
        d = 'qhw3qzg3fEK0NNfoVxk4jQ=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    # See https://github.com/IQSS/UNF/pull/3
    def test_round_1(self):
        val = 1.2345675
        s = b'+1.234568e+\n\000'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    # See https://github.com/IQSS/UNF/pull/3
    def test_round_2(self):
        val = 1.2345685
        s = b'+1.234568e+\n\000'
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        return

    def test_nan(self):
        val = float('NaN')
        s = b'+nan\n\000'
        d = 'GNcR8/UCnImaPpw47gdPNg=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_positive_inf(self):
        val = float('+Inf')
        s = b'+inf\n\000'
        d = 'MdAI70WZdDHnu6qmkpqUQg=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_negative_inf(self):
        val = float('-Inf')
        s = b'-inf\n\000'
        d = 'A7orv3pgAhljFnGjQVLCog=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_simple_string(self):
        val = 'A character String'
        s = b'A character String\n\0'
        d = 'FYqU7uBl885eHMbpco1ooA=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_long_string(self):
        val = 'A quite long character string, so long that the ' \
              'number of characters in it happens to be more than ' \
              'the default cutoff limit of 128.'
        s = b'A quite long character string, so long that the number ' \
            b'of characters in it happens to be more than the default ' \
            b'cutoff limit of 1\n\0'
        d = '/BoSlfcIlsmQ+GHu5gxwEw=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_accented_string(self):
        val = 'på Færøerne'
        s = b'p\xc3\xa5 F\xc3\xa6r\xc3\xb8erne\n\0'
        d = 'KHM6bKVaVaxWDDsmyerfDA=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_empty_string(self):
        val = ''
        s = b'\n\0'
        d = 'ECtRuXZaVqPomffPDuOOUg=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

    def test_missing_value(self):
        val = None
        s = b'\0\0\0'
        d = 'cJ6AyISHokEeHuTfufIqhg=='
        self.assertEqual(unf._normalize(val, unf.DEFAULT_DIGITS), s)
        self.assertEqual(unf._digest(val, unf.DEFAULT_DIGITS), d)
        self.assertEqual(unf.unf(val), 'UNF:6:' + d)
        return

class TestUNFs(unittest.TestCase):

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

    def test_pos_zero(self):
        u = unf.unf(0.0)
        self.assertEqual(u, 'UNF:6:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_neg_zero(self):
        u = unf.unf(-0.0)
        self.assertEqual(u, 'UNF:6:qDM4PMUq1cMW+bqfBLBGZg==')
        return

    # See ROUNDING.md
    def test_round_1(self):
        u = unf.unf(1.2345635)
        self.assertEqual(u, 'UNF:6:auhsR5DIScLiAUb/SA2YVA==')
        return

    # See ROUNDING.md
    def test_round_2(self):
        u = unf.unf(1.2345645)
        self.assertEqual(u, 'UNF:6:auhsR5DIScLiAUb/SA2YVA==')
        return

    # See ROUNDING.md
    def test_round_3(self):
        u = unf.unf(12345635)
        self.assertEqual(u, 'UNF:6:qnKXlm182LZPFz9JzxTiNg==')
        return

    # See ROUNDING.md
    def test_round_4(self):
        u = unf.unf(12345645)
        self.assertEqual(u, 'UNF:6:qnKXlm182LZPFz9JzxTiNg==')
        return

    def test_large_exponent(self):
        u = unf.unf(1.234567e150)
        self.assertEqual(u, 'UNF:6:qcKO4c5rvHfQ3nHzqrAS/Q==')
        return

    def test_tiny_exponent(self):
        u = unf.unf(1.234567e-150)
        self.assertEqual(u, 'UNF:6:vbTNUOoynDv6UKxOn36WeQ==')
        return

    def test_compound_value(self):
        with self.assertRaises(TypeError):
            unf.unf([1, [1.23456789, None, 0]])
        return

class TestDigits(unittest.TestCase):

    # ---------------------------------------------------------
    # type and value checking

    def test_type_error(self):
        with self.assertRaises(TypeError):
            unf.unf('', '')
        return

    def test_value_error(self):
        with self.assertRaises(ValueError):
            unf.unf('', 0)
        return

    # ---------------------------------------------------------
    # the following should be unaffected by digits=2

    def test_missing(self):
        u = unf.unf(None, 2)
        self.assertEqual(u, 'UNF:6:N2:cJ6AyISHokEeHuTfufIqhg==')
        return

    def test_string(self):
        u = unf.unf('A character String', 2)
        self.assertEqual(u, 'UNF:6:N2:FYqU7uBl885eHMbpco1ooA==')
        return

    def test_nan(self):
        u = unf.unf(float('NaN'), 2)
        self.assertEqual(u, 'UNF:6:N2:GNcR8/UCnImaPpw47gdPNg==')
        return

    def test_positive_inf(self):
        u = unf.unf(float('+Inf'), 2)
        self.assertEqual(u, 'UNF:6:N2:MdAI70WZdDHnu6qmkpqUQg==')
        return

    def test_negative_inf(self):
        u = unf.unf(float('-Inf'), 2)
        self.assertEqual(u, 'UNF:6:N2:A7orv3pgAhljFnGjQVLCog==')
        return

    def test_positive_zero(self):
        u = unf.unf(0.0, 2)
        self.assertEqual(u, 'UNF:6:N2:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_negative_zero(self):
        u = unf.unf(-0.0, 2)
        self.assertEqual(u, 'UNF:6:N2:qDM4PMUq1cMW+bqfBLBGZg==')
        return

    def test_0(self):
        u = unf.unf(0, 2)
        self.assertEqual(u, 'UNF:6:N2:YUvj33xEHnzirIHQyZaHow==')
        return

    def test_1(self):
        u = unf.unf(1, 2)
        self.assertEqual(u, 'UNF:6:N2:tv3XYCv524AfmlFyVOhuZg==')
        return

    # ---------------------------------------------------------
    # value tests, including header checks

    def test_value_1(self):
        u = unf.unf(1.2345678, 6)
        self.assertEqual(u, 'UNF:6:N6:Z8pf0CubsQBVtRiOQLQNVA==')
        return

    # Default digits, so no N in header.
    def test_default_digits(self):
        u = unf.unf(1.2345678, unf.DEFAULT_DIGITS)
        self.assertEqual(u, 'UNF:6:vcKELUSS4s4k1snF4OTB9A==')
        return

    def test_value_2(self):
        u = unf.unf(1.2345678, 8)
        self.assertEqual(u, 'UNF:6:N8:TCfkDjJvqAJ7wy4sdQFRaw==')
        return

    # Should be the same as digits=8 since we run out of significant 
    # digits in the value.
    def test_value_3(self):
        u = unf.unf(1.2345678, 9)
        self.assertEqual(u, 'UNF:6:N9:TCfkDjJvqAJ7wy4sdQFRaw==')
        return

@unittest.skipIf(not numpy, 'numpy not installed')
class TestNumpy(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self._normalize_numpy = unf._normalize_numpy
        unf._normalize_numpy = unittest.mock.Mock(
            spec=self._normalize_numpy, 
            side_effect=self._normalize_numpy
        )
        return

    def tearDown(self):
        super().tearDown()
        unf._normalize_numpy = self._normalize_numpy
        return

    # ---------------------------------------------------------
    # error tests

    def test_heterogeneous(self):
        with self.assertRaises(ValueError):
            unf.unf(numpy.array([None, True, 2, 3.4, '5.6.7']))
        return

    # ---------------------------------------------------------
    # dimension tests

    def test_dim_0(self):
        with self.assertRaises(TypeError):
            unf.unf(numpy.int64(0))
        return

    def test_dim_1_single_value(self):
        u = unf.unf(1)
        self.assertFalse(unf._normalize_numpy.called)
        nu = unf.unf(numpy.array([1]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, nu)
        return

    def test_dim_2(self):
        a = numpy.array([[1.2345678, 2, 3], [4, 5, 6]])
        u = unf.unf(a)
        self.assertEqual(u, 'UNF:6:qs7MinjKNf+1+wy/RfVNvA==')
        a = numpy.array([[4, 5, 6], [1.2345678, 2, 3]])
        u = unf.unf(a)
        self.assertEqual(u, 'UNF:6:qs7MinjKNf+1+wy/RfVNvA==')
        return

    def test_dim_2_1a(self):
        a = numpy.array([[1.2345678, 2, 3]])
        u = unf.unf(a)
        self.assertEqual(u, 'UNF:6:Gu/iYw2g7MIfVrNo1t4+zQ==')
        return

    def test_dim_2_1b(self):
        a = numpy.array([[1.2345678], [2], [3]])
        u = unf.unf(a)
        self.assertEqual(u, 'UNF:6:2FSEGfhYpvPqVoY3AlpNrw==')
        return

    def test_dim_2_single_value(self):
        u = unf.unf(1)
        self.assertFalse(unf._normalize_numpy.called)
        nu = unf.unf(numpy.array([[1]]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, nu)
        return

    def test_dim_3(self):
        a = numpy.zeros((2, 3, 4))
        with self.assertRaises(ValueError):
            unf.unf(a)
        return

    # ---------------------------------------------------------
    # value tests -- as base tests above

    def test_vector(self):
        val = numpy.array([1.23456789, 0])
        u = 'UNF:6:0k7UOb0YlUtUQuA2Fyqy7Q=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_1t9_unf(self):
        val = numpy.array([1.23456789])
        u = 'UNF:6:vcKELUSS4s4k1snF4OTB9A=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_1t9_9_digits_unf(self):
        val = numpy.array([1.23456789])
        u = 'UNF:6:N9:IKw+l4ywdwsJeDze8dplJA=='
        self.assertEqual(unf.unf(val, 9), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_0(self):
        val = numpy.array([0])
        u = 'UNF:6:YUvj33xEHnzirIHQyZaHow=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_1(self):
        val = numpy.array([1])
        u = 'UNF:6:tv3XYCv524AfmlFyVOhuZg=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_m300(self):
        val = numpy.array([-300])
        u = 'UNF:6:ZTXyg54FoMfRDWZl6oWmFQ=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_pi(self):
        val = numpy.array([3.1415])
        u = 'UNF:6:vOSZmXXXpKfQcqZ0Cuu5/w=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_73em4(self):
        val = numpy.array([0.00073])
        u = 'UNF:6:qhw3qzg3fEK0NNfoVxk4jQ=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_nan(self):
        val = numpy.array([float('NaN')])
        u = 'UNF:6:GNcR8/UCnImaPpw47gdPNg=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_positive_inf(self):
        val = numpy.array([float('+Inf')])
        u = 'UNF:6:MdAI70WZdDHnu6qmkpqUQg=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_negative_inf(self):
        val = numpy.array([float('-Inf')])
        u = 'UNF:6:A7orv3pgAhljFnGjQVLCog=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_pos_zero(self):
        val = numpy.array([0.0])
        u = 'UNF:6:YUvj33xEHnzirIHQyZaHow=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_neg_zero(self):
        val = numpy.array([-0.0])
        u = 'UNF:6:qDM4PMUq1cMW+bqfBLBGZg=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_round_1(self):
        val = numpy.array([1.2345635])
        u = 'UNF:6:auhsR5DIScLiAUb/SA2YVA=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_round_2(self):
        val = numpy.array([1.2345645])
        u = 'UNF:6:auhsR5DIScLiAUb/SA2YVA=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_round_3(self):
        val = numpy.array([12345635])
        u = 'UNF:6:qnKXlm182LZPFz9JzxTiNg=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_round_4(self):
        val = numpy.array([12345645])
        u = 'UNF:6:qnKXlm182LZPFz9JzxTiNg=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_large_exponent(self):
        val = numpy.array([1.234567e150])
        u = 'UNF:6:qcKO4c5rvHfQ3nHzqrAS/Q=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_tiny_exponent(self):
        val = numpy.array([1.234567e-150])
        u = 'UNF:6:vbTNUOoynDv6UKxOn36WeQ=='
        self.assertEqual(unf.unf(val), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_digits_value_1(self):
        val = numpy.array([1.2345678])
        u = 'UNF:6:N6:Z8pf0CubsQBVtRiOQLQNVA=='
        self.assertEqual(unf.unf(val, 6), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_digits_value_2(self):
        val = numpy.array([1.2345678])
        u = 'UNF:6:N8:TCfkDjJvqAJ7wy4sdQFRaw=='
        self.assertEqual(unf.unf(val, 8), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    def test_digits_value_3(self):
        val = numpy.array([1.2345678])
        u = 'UNF:6:N9:TCfkDjJvqAJ7wy4sdQFRaw=='
        self.assertEqual(unf.unf(val, 9), u)
        self.assertTrue(unf._normalize_numpy.called)
        return

    # ---------------------------------------------------------
    # extra numpy value tests

    # Versions through 0.7.1 have an error where scaled values
    # lose leading zeros after the decimal point.  So 0.9005000798402081
    # normalizes to b'+9.5001e-1\n' rather than the correct
    # b'+9.005001e-1\n'.  This only happens with values in numpy
    # arrays.
    def test_0701_error(self):
        u = unf.unf(numpy.array([0.9005000798402081]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:8eqCT5VNEgqICh3FnZsImQ==')
        return

    # Our numpy optimization introduced some finicky operations in 
    # _normalize(), so we add some extra tests here.
    # Similar to the 0701 test, we introduce zeros in floating point 
    # values and in exponents.

    def test_exp_1(self):
        u = unf.unf(numpy.array([1e0]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_exp_2(self):
        u = unf.unf(numpy.array([1e1]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:o+nTsng0TLIV1N3Dqa2rRA==')
        return

    def test_exp_3(self):
        u = unf.unf(numpy.array([1e10]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:TeER1wBkwE+zvHLxSEmnZA==')
        return

    def test_exp_4(self):
        u = unf.unf(numpy.array([1e100]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:K67V/jah/5UTNdTqNfGNGQ==')
        return

    def test_exp_5(self):
        u = unf.unf(numpy.array([1e101]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:WxchK5DSjOC/vrznE6g5KA==')
        return

    def test_value_1(self):
        u = unf.unf(numpy.array([1.00000001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_value_2(self):
        u = unf.unf(numpy.array([1.10000001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:e7mRzE999g+XdbMRqdnCkA==')
        return

    def test_value_3(self):
        u = unf.unf(numpy.array([1.1]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:e7mRzE999g+XdbMRqdnCkA==')
        return

    def test_value_4(self):
        u = unf.unf(numpy.array([1.100001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:BZsaaf/5tFPpBmWgmIozJw==')
        return

    def test_value_5(self):
        u = unf.unf(numpy.array([1.1000001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:e7mRzE999g+XdbMRqdnCkA==')
        return

    def test_value_6(self):
        u = unf.unf(numpy.array([1.000001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:uTepcVWx1hT/FPAPcmNfzQ==')
        return

    def test_value_7(self):
        u = unf.unf(numpy.array([1.0000001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:tv3XYCv524AfmlFyVOhuZg==')
        return

    def test_value_8(self):
        u = unf.unf(numpy.array([1.00010001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:f2+uKERSm529tncALsUPpg==')
        return

    def test_value_9(self):
        u = unf.unf(numpy.array([1.10010001]))
        self.assertTrue(unf._normalize_numpy.called)
        self.assertEqual(u, 'UNF:6:+fmO4JH7/DXQI2ay8JUyow==')
        return

@unittest.skipIf(not pandas, 'pandas not installed')
class TestPandas(unittest.TestCase):

    def test_series(self):
        s = pandas.Series([1.2345678, 2, 3])
        u = unf.unf(s)
        self.assertEqual(u, 'UNF:6:Gu/iYw2g7MIfVrNo1t4+zQ==')
        return

    def test_series_2(self):
        s = pandas.Series([1.2345678, None, 3])
        u = unf.unf(s)
        self.assertEqual(u, 'UNF:6:t5y+wj7UWZB7PO0R+r6c3A==')
        return

    def test_series_dtype(self):
        s = pandas.Series(['a'])
        with self.assertRaises(ValueError):
            unf.unf(s)
        return

    def test_data_frame(self):
        df = pandas.DataFrame({'a': [1.2345678, 2, 3], 'b': [4, 5, 6]})
        u = unf.unf(df)
        self.assertEqual(u, 'UNF:6:qs7MinjKNf+1+wy/RfVNvA==')
        return

    def test_data_frame_2(self):
        df = pandas.DataFrame({'a': [4, 5, 6], 'b': [1.2345678, 2, 3]})
        u = unf.unf(df)
        self.assertEqual(u, 'UNF:6:qs7MinjKNf+1+wy/RfVNvA==')
        return

    def test_data_frame_3(self):
        df = pandas.DataFrame({'a': [1.2345678, 2, 3]})
        u = unf.unf(df)
        self.assertEqual(u, 'UNF:6:Gu/iYw2g7MIfVrNo1t4+zQ==')
        return

    def test_series_digits(self):
        s = pandas.Series([1.2345678, 2, 3])
        u = unf.unf(s, 6)
        self.assertEqual(u, 'UNF:6:N6:SoKpWA1mdIXyd/7/QAqdVQ==')
        return

    def test_series_2_digits(self):
        s = pandas.Series([1.2345678, None, 3])
        u = unf.unf(s, 6)
        self.assertEqual(u, 'UNF:6:N6:GMsD/Sf8VOarlClFV3r3HA==')
        return

    def test_data_frame_digits(self):
        df = pandas.DataFrame({'a': [1.2345678, 2, 3], 'b': [4, 5, 6]})
        u = unf.unf(df, 6)
        self.assertEqual(u, 'UNF:6:N6:FXXlk9tS02EIpobkfwDUgQ==')
        return

    def test_data_frame_2_digits(self):
        df = pandas.DataFrame({'a': [4, 5, 6], 'b': [1.2345678, 2, 3]})
        u = unf.unf(df, 6)
        self.assertEqual(u, 'UNF:6:N6:FXXlk9tS02EIpobkfwDUgQ==')
        return

    def test_data_frame_3_digits(self):
        df = pandas.DataFrame({'a': [1.2345678, 2, 3]})
        u = unf.unf(df, 6)
        self.assertEqual(u, 'UNF:6:N6:SoKpWA1mdIXyd/7/QAqdVQ==')
        return

class DocsTests(unittest.TestCase):

    # Test assertions and examples in the documentation.

    def test_basic(self):
        val = 1.23456789
        u = 'UNF:6:vcKELUSS4s4k1snF4OTB9A=='
        self.assertEqual(unf.unf(val), u)
        return

    def test_basic_digits(self):
        val = 1.23456789
        u = 'UNF:6:N9:IKw+l4ywdwsJeDze8dplJA=='
        self.assertEqual(unf.unf(val, 9), u)
        return

    def test_none(self):
        val = [1.23456789, None, 0]
        u = 'UNF:6:Do5dfAoOOFt4FSj0JcByEw=='
        self.assertEqual(unf.unf(val), u)
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy(self):
        val = numpy.array([1, 2, 3])
        u = 'UNF:6:AvELPR5QTaBbnq6S22Msow=='
        self.assertEqual(unf.unf(val), u)
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy_collection_of_vectors(self):
        val1 = numpy.array([[1, 2], [3, 4]])
        val2 = numpy.array([[3, 4], [1, 2]])
        self.assertEqual(unf.unf(val1), unf.unf(val2))
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy_collection_of_one_vector(self):
        val1 = numpy.array([[1, 2]])
        val2 = numpy.array([1, 2])
        self.assertEqual(unf.unf(val1), unf.unf(val2))
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy_collection_of_vectors_2(self):
        val1 = numpy.array([[1], [2]])
        val2 = numpy.array([[2], [1]])
        self.assertEqual(unf.unf(val1), unf.unf(val2))
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy_primitive(self):
        val = numpy.array([1])[0]
        with self.assertRaises(Exception):
            unf.unf(val)
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy_n_dim(self):
        val = numpy.zeros((2, 3, 4))
        with self.assertRaises(Exception):
            unf.unf(val)
        return

    @unittest.skipIf(not numpy, 'numpy not installed')
    def test_numpy_none(self):
        a = numpy.array([None], dtype=float)
        self.assertTrue(math.isnan(a[0]))
        return

    @unittest.skipIf(not pandas, 'pandas not installed')
    def test_pandas_series(self):
        value = pandas.Series([1, 2, 3])
        u = 'UNF:6:AvELPR5QTaBbnq6S22Msow=='
        self.assertEqual(unf.unf(value), u)
        return

    @unittest.skipIf(not pandas, 'pandas not installed')
    def test_pandas_data_frame(self):
        value = pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        u = 'UNF:6:Np0sj111a+rrJBgl6wNF9w=='
        self.assertEqual(unf.unf(value), u)
        return

    @unittest.skipIf(not pandas, 'pandas not installed')
    def test_pandas_na_object(self):
        s = pandas.Series([1, pandas.NA])
        self.assertEqual(s.dtype, 'O')
        return

    @unittest.skipIf(not pandas, 'pandas not installed')
    def test_pandas_none(self):
        s = pandas.Series([None], dtype=float)
        self.assertTrue(math.isnan(s[0]))
        return

# eof
