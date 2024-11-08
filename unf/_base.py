# See file COPYING distributed with python-unf for copyright and license.

import hashlib
import math
import base64

try:
    import numpy
except ImportError:
    numpy = None

from ._constants import *
from ._numpy import (
    _normalize_numpy_array
)

def normalize(data, digits=default_digits):
    if not isinstance(digits, int):
        raise TypeError('digits must be an integer')
    if digits < 1:
        raise ValueError('digits must be positive')
    if numpy and isinstance(data, numpy.ndarray):
        if data.ndim > 1:
            raise ValueError('numpy arrays must be 1-D')
        # is the array all numeric?  if so, try to speed up the 
        # calculations
        if numpy.issubdtype(data.dtype, int) or \
            numpy.issubdtype(data.dtype, float):
            return _normalize_numpy_array(data, digits)
        return b''.join([ normalize(el, digits) for el in data ])
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
    original values but rather scale the values so all of the
    significant digits are to the left of the decimal point, then
    round to integers, and then scale back.

    See README.rounding for more information.
    """
    if n < 0:
        n_sign = '-'
        n = -n
    else:
        n_sign = '+'
    exp = int(math.floor(math.log10(n)))
    n_int = _rint(n * 10**(digits-1-exp))
    n_int_s = str(n_int)
    i_part = n_int_s[0]
    f_part = n_int_s[1:].rstrip('0')
    if exp == 0:
        data = '{}{}.{}e+\n\0'.format(n_sign, i_part, f_part)
    else:
        data = '{}{}.{}e{:+d}\n\0'.format(n_sign, i_part, f_part, exp)
    return data.encode()

def _rint(n):
    """rounds n to the nearest integer, towards even if a tie"""
    n_int = int(math.floor(n))
    if n == n_int + 0.5:
        if n_int % 2:
            return n_int + 1
        return n_int
    return int(round(n))

def unf(obj, digits=default_digits):
    string = normalize(obj, digits)
    hash = hashlib.sha256(string).digest()
    encoded_hash = base64.b64encode(hash[:16]).decode()
    if digits == default_digits:
        rv = 'UNF:{}:{}'.format(version, encoded_hash)
    else:
        fmt = 'UNF:{}:N{}:{}'
        rv = fmt.format(version, digits, encoded_hash)
    return rv

# eof
