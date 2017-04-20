# See file COPYING distributed with unf for copyright and license.

import hashlib
import math

try:
    import numpy
except ImportError:
    numpy = None

class UNF:

    default_digits = 7

    def __init__(self, data, digits=default_digits):
        self.version = 6
        self.data = data
        if not isinstance(digits, int):
            raise TypeError('digits must be an integer')
        if digits < 1:
            raise ValueError('digits must be positive')
        self.digits = digits
        self.characters = 128
        self._string = self._normalize(self.data)
        h = hashlib.sha256(self._string)
        self.hash = h.digest()
        self.unf = self.hash[:16].encode('base64').rstrip('\n')
        if self.digits == self.default_digits:
            self.formatted = 'UNF:%d:%s' % (self.version, self.unf)
        else:
            fmt = 'UNF:%d:N%d:%s'
            self.formatted = fmt % (self.version, self.digits, self.unf)
        return

    def __str__(self):
        return self.formatted

    def _normalize(self, data):
        if numpy and isinstance(data, numpy.ndarray):
            # is the array all numeric?  if so, try to speed up the 
            # calculations
            if numpy.issubdtype(data.dtype, int) or \
                numpy.issubdtype(data.dtype, float):
                return self._normalize_ndarray(data)
            return ''.join([ self._normalize(el) for el in data ])
        if isinstance(data, (tuple, list)):
            return ''.join([ self._normalize(el) for el in data ])
        if data is None:
            return self._normalize_none(data)
        if isinstance(data, bool):
            return self._normalize_boolean(data)
        if isinstance(data, basestring):
            return self._normalize_basestring(data)
        if isinstance(data, (int, float, long)):
            return self._normalize_number(data)
        raise TypeError('unsupported type for data')

    def _normalize_none(self, data):
        return '\0\0\0'

    def _normalize_basestring(self, data):
        return data.encode('utf-8')[:self.characters] + '\n\0'

    def _normalize_boolean(self, data):
        if data:
            return self._normalize_number(1)
        return self._normalize_number(0)

    def _normalize_number(self, data):
        data = float(data)
        if math.isnan(data):
            return '+nan\n\0'
        if math.isinf(data):
            if data > 0:
                return '+inf\n\0'
            return '-inf\n\0'
        if data == 0.0:
            if math.copysign(1, data) > 0:
                return '+0.e+\n\0'
            else:
                return '-0.e+\n\0'
        return self._nn(data)

    def _nn(self, n):
        """normalization for a non-special number

        see README.rounding"""
        if n < 0:
            n_sign = '-'
            n = -n
        else:
            n_sign = '+'
        l10 = math.log10(n)
        exp = int(math.floor(l10))
        e10 = self.digits - 1 - exp
        # branch here to keep pow10 > 0 so exactly representable
        if e10 > 0:
            pow10 = math.pow(10, e10)
            n_int = rint(n*pow10)
        else:
            pow10 = math.pow(10, -e10)
            n_int = rint(n/pow10)
        n_int_s = str(n_int)
        i_part = n_int_s[0]
        f_part = n_int_s[1:].rstrip('0')
        if exp == 0:
            return '%s%s.%se+\n\0' % (n_sign, i_part, f_part)
        return '%s%s.%se%+d\n\0' % (n_sign, i_part, f_part, exp)

    def _normalize_ndarray(self, data):
        """normalize a numpy array with only numeric values

        this is meant to increase speed over calling _normalize_number() 
        for each element
        """
        nan_inds = numpy.isnan(data)
        inf_inds = numpy.isinf(data)
        zero_inds = data == 0.0
        signs = numpy.copysign(1, data)
        data_c = signs * data
        data_c[nan_inds | inf_inds | zero_inds] = 1.0
        l10 = numpy.log10(data_c)
        exp = numpy.floor(l10).astype(int)
        e10 = self.digits - 1 - exp

        pow10 = numpy.ndarray(e10.size, dtype=int)
        n_int = numpy.ndarray(e10.size, dtype=float)

        e10_pos_inds = e10 > 0
        e10_npos_inds = e10 <= 0
        n_int[e10_pos_inds] = data_c[e10_pos_inds] * 10**e10[e10_pos_inds]
        n_int[e10_npos_inds] = data_c[e10_npos_inds] / 10**-e10[e10_npos_inds]
        n_int = numpy.rint(n_int).astype(int)

        s = [None] * data.size
        for i in xrange(data.size):
            assert len(n_int[i].astype(str)) == self.digits
            if nan_inds[i]:
                s[i] = '+nan\n\0'
                continue
            if signs[i] > 0:
                sign = '+'
            else:
                sign = '-'
            if inf_inds[i]:
                s[i] = '%sinf\n\0' % sign
                continue
            if zero_inds[i]:
                s[i] = '%s0.e+\n\0' % sign
                continue
            sv = str(n_int[i])
            i_part = sv[0]
            f_part = sv[1:].rstrip('0')
            if exp[i] == 0:
                s[i] = '%s%s.%se+\n\0' % (sign, i_part, f_part)
            else:
                s[i] = '%s%s.%se%+d\n\0' % (sign, i_part, f_part, exp[i])
        return ''.join(s)

def rint(n):
    """rounds n to the nearest integer, towards even if a tie"""
    n_int = int(math.floor(n))
    if n == n_int + 0.5:
        if n_int % 2:
            return n_int + 1
        return n_int
    return int(round(n))

# eof
