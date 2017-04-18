# See file COPYING distributed with unf for copyright and license.

import hashlib
import math

class UNF:

    def __init__(self, data, digits=7):
        self.version = 6
        self.data = data
        self.digits = digits
        self.characters = 128
        if data is None:
            self._string = self._normalize_none(self.data)
        elif isinstance(data, basestring):
            self._string = self._normalize_basestring(self.data)
        elif isinstance(data, (int, float, long)):
            self._string = self._normalize_number(self.data)
        else:
            raise TypeError('unsupported type for data')
        h = hashlib.sha256(self._string)
        self.hash = h.digest()
        self.unf = self.hash[:16].encode('base64').rstrip('\n')
        self.formatted = 'UNF:%d:%s' % (self.version, self.unf)
        return

    def __str__(self):
        return self.formatted

    def _normalize_none(self, data):
        return '\0\0\0'

    def _normalize_basestring(self, data):
        return data.encode('utf-8')[:self.characters] + '\n\0'

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
        print n_int, e10
        n_int_s = str(n_int)
        i_part = n_int_s[0]
        f_part = n_int_s[1:].rstrip('0')
        if exp == 0:
            return '%s%s.%se+\n\0' % (n_sign, i_part, f_part)
        return '%s%s.%se%+d\n\0' % (n_sign, i_part, f_part, exp)

def rint(n):
    """rounds n to the nearest integer, towards even if a tie"""
    n_int = int(math.floor(n))
    if n == n_int + 0.5:
        if n_int % 2:
            return n_int + 1
        return n_int
    return int(round(n))

# eof
