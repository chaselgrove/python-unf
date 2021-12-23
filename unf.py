# See file COPYING distributed with python-unf for copyright and license.

import hashlib
import math
import base64

__version__ = '0.9.0'

try:
    import numpy
except ImportError:
    numpy = None

version = 6
default_digits = 7
characters = 128

def _normalize(data, digits):
    if numpy and isinstance(data, numpy.ndarray):
        if data.ndim > 1:
            raise ValueError('numpy arrays must be 1-D')
        # is the array all numeric?  if so, try to speed up the 
        # calculations
        if numpy.issubdtype(data.dtype, int) or \
            numpy.issubdtype(data.dtype, float):
            return _normalize_numpy_array(data, digits)
        return b''.join([ _normalize(el, digits) for el in data ])
    if isinstance(data, (tuple, list)):
        return b''.join([ _normalize_primitive(el, digits) for el in data ])
    return _normalize_primitive(data, digits)

def _normalize_primitive(data, digits):
    if data is None:
        return _normalize_none(data)
    if isinstance(data, bool):
        return _normalize_boolean(data)
    if isinstance(data, str):
        return _normalize_str(data)
    if isinstance(data, (int, float)):
        return _normalize_number(data, digits)
    raise TypeError('unsupported type for data')

def _normalize_none(data):
    return b'\0\0\0'

def _normalize_str(data):
    return data.encode()[:characters] + b'\n\0'

def _normalize_boolean(data):
    return b'+1.e+\n\0' if data else b'+0.e+\n\0'

def _normalize_number(data, digits):
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
    return _nn(data, digits)

def _nn(n, digits):
    """Normalize a non-special number.

    To match the behavior of the R UNF package, we don't round the
    original values but rather scale the value so all of the
    significant digits are to the left of the decimal point, then
    rounding to an integer, and then scaling back.

    See README.rounding for more information.
    """
    if n < 0:
        n_sign = '-'
        n = -n
    else:
        n_sign = '+'
    exp = int(math.floor(math.log10(n)))
    n_int = rint(n * 10**(digits-1-exp))
    n_int_s = str(n_int)
    i_part = n_int_s[0]
    f_part = n_int_s[1:].rstrip('0')
    if exp == 0:
        data = '{}{}.{}e+\n\0'.format(n_sign, i_part, f_part)
    else:
        data = '{}{}.{}e{:+d}\n\0'.format(n_sign, i_part, f_part, exp)
    return data.encode()

def _normalize_numpy_array(data, digits):

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
    exp = numpy.floor(numpy.log10(data_c)).astype(int)
    n_int = numpy.rint(data_c * 10**(digits-1-exp)).astype(int)

    # --- generate normalization strings
    dpow = 10**(digits-1)
    n_ipart = numpy.floor_divide(n_int, dpow).astype(str)
    n_fpart = n_int % dpow
    n_fpart = n_fpart.astype(str)
    n_fpart = numpy.char.rjust(n_fpart, digits-1, '0')
    n_fpart = numpy.char.rstrip(n_fpart, '0')
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

def unf(obj, digits=default_digits):
    if not isinstance(digits, int):
        raise TypeError('digits must be an integer')
    if digits < 1:
        raise ValueError('digits must be positive')
    string = _normalize(obj, digits)
    hash = hashlib.sha256(string).digest()
    encoded_hash = base64.b64encode(hash[:16]).decode()
    if digits == default_digits:
        rv = 'UNF:{}:{}'.format(version, encoded_hash)
    else:
        fmt = 'UNF:{}:N{}:{}'
        rv = fmt.format(version, digits, encoded_hash)
    return rv

# eof
