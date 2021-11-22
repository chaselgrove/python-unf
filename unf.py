# See file COPYING distributed with unf for copyright and license.

import hashlib
import math
import base64

__version__ = '0.6.0'

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
        self.unf = base64.b64encode(self.hash[:16]).decode()
        if self.digits == self.default_digits:
            self.formatted = 'UNF:{}:{}'.format(self.version, self.unf)
        else:
            fmt = 'UNF:{}:N{}:{}'
            self.formatted = fmt.format(self.version, self.digits, self.unf)
        return

    def __str__(self):
        return self.formatted

    def _normalize(self, data):
        if numpy and isinstance(data, numpy.ndarray):
            if data.ndim > 1:
                raise ValueError('numpy arrays must be 1-D')
            # is the array all numeric?  if so, try to speed up the 
            # calculations
            if numpy.issubdtype(data.dtype, int) or \
                numpy.issubdtype(data.dtype, float):
                return self._normalize_numpy_array(data)
            return b''.join([ self._normalize(el) for el in data ])
        if isinstance(data, (tuple, list)):
            return b''.join([ self._normalize_primitive(el) for el in data ])
        return self._normalize_primitive(data)

    def _normalize_primitive(self, data):
        if data is None:
            return self._normalize_none(data)
        if isinstance(data, bool):
            return self._normalize_boolean(data)
        if isinstance(data, str):
            return self._normalize_str(data)
        if isinstance(data, (int, float)):
            return self._normalize_number(data)
        raise TypeError('unsupported type for data')

    def _normalize_none(self, data):
        return b'\0\0\0'

    def _normalize_str(self, data):
        return data.encode()[:self.characters] + b'\n\0'

    def _normalize_boolean(self, data):
        if data:
            return self._normalize_number(1)
        return self._normalize_number(0)

    def _normalize_number(self, data):
        data = float(data)
        if math.isnan(data):
            return b'+nan\n\0'
        if math.isinf(data):
            if data > 0:
                return b'+inf\n\0'
            return b'-inf\n\0'
        if data == 0.0:
            if math.copysign(1, data) > 0:
                return b'+0.e+\n\0'
            else:
                return b'-0.e+\n\0'
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
            data = '{}{}.{}e+\n\0'.format(n_sign, i_part, f_part)
        else:
            data = '{}{}.{}e{:+d}\n\0'.format(n_sign, i_part, f_part, exp)
        return data.encode()

    def _normalize_numpy_array(self, data):

        """normalize a numpy array with only numeric values

        this is meant to increase speed over calling _normalize_number() 
        for each element
        """

        # --- find special values and record signs, make all values positive, 
        # --- then replace special values with dummy numbers
        nan_inds = numpy.isnan(data)
        inf_inds = numpy.isinf(data)
        zero_inds = data == 0.0
        signs = numpy.copysign(1, data)
        data_c = signs * data
        data_c[nan_inds | inf_inds | zero_inds] = 1.0

        # --- shift the decimal points and round
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

        # --- generate normalization strings
        dpow = 10**(self.digits-1)
        n_ipart = numpy.floor_divide(n_int, dpow).astype(str)
        n_fpart = n_int % dpow
        n_fpart = numpy.char.rstrip(n_fpart.astype(str), '0')
        sign_arr = numpy.full(n_int.shape, '+', dtype='U')
        sign_arr[signs < 0] = '-'
        exp_arr = exp.astype(str)
        exp_arr[exp == 0] = ''
        # minus signs will come from the exponent itself
        exp_sign_arr = numpy.full(n_int.shape, '', dtype='U')
        exp_sign_arr[exp >= 0] = '+'
        s = numpy.char.add(sign_arr, n_ipart)
        s = numpy.char.add(s, '.')
        s = numpy.char.add(s, n_fpart)
        s = numpy.char.add(s, 'e')
        s = numpy.char.add(s, exp_sign_arr)
        s = numpy.char.add(s, exp_arr)

        # --- set normalization strings for special values
        s[nan_inds] = '+nan'
        s[numpy.logical_and(inf_inds, signs > 0)] = '+inf'
        s[numpy.logical_and(inf_inds, signs < 0)] = '-inf'
        s[numpy.logical_and(zero_inds, signs > 0)] = '+0.e+'
        s[numpy.logical_and(zero_inds, signs < 0)] = '-0.e+'

        data = '\n\0'.join(s) + '\n\0'
        return data.encode()

def rint(n):
    """rounds n to the nearest integer, towards even if a tie"""
    n_int = int(math.floor(n))
    if n == n_int + 0.5:
        if n_int % 2:
            return n_int + 1
        return n_int
    return int(round(n))

# eof
