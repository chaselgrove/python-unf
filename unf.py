# See file COPYING distributed with python-unf for copyright and license.

import hashlib
import math
import base64

try:
    import numpy
except ImportError:
    numpy = None

try:
    import pandas
except ImportError:
    pandas = None

__version__ = '0.10.0'

UNF_VERSION = 6
DEFAULT_DIGITS = 7
STRING_CHARACTERS = 128
HASH_BYTES = 16

# --- public functions --------------------------------------------------

def unf(obj, digits=DEFAULT_DIGITS):
    """Calculate the UNF of an object.

    The returned UNF is the full UNF with headers (UNF:6: and an optional 
    digits indicator).  Non-standard string truncations and hash 
    truncations are not supported.
    """
    encoded_hash = _digest(obj, digits)
    if digits == DEFAULT_DIGITS:
        rv = f'UNF:{UNF_VERSION}:{encoded_hash}'
    else:
        rv = f'UNF:{UNF_VERSION}:N{digits}:{encoded_hash}'
    return rv

# --- utilities ---------------------------------------------------------

def _digest(obj, digits):
    """Calculate the digest of an object."""
    string = _normalize(obj, digits)
    hash = hashlib.sha256(string).digest()
    return base64.b64encode(hash[:HASH_BYTES]).decode()

def _normalize(data, digits):
    """Normalize an object to a byte string."""
    if not isinstance(digits, int):
        raise TypeError('digits must be an integer')
    if digits < 1:
        raise ValueError('digits must be positive')
    if numpy and isinstance(data, numpy.ndarray):
        return _normalize_numpy(data, digits)
    if pandas and isinstance(data, (pandas.Series, pandas.DataFrame)):
        return _normalize_pandas(data, digits)
    if isinstance(data, (tuple, list)):
        return b''.join([ _normalize_primitive(el, digits) for el in data ])
    return _normalize_primitive(data, digits)

def _normalize_primitive(data, digits):
    """Normalize a value of a simple data type."""
    if data is None:
        return b'\0\0\0'
    if isinstance(data, bool):
        return b'+1.e+\n\0' if data else b'+0.e+\n\0'
    if isinstance(data, str):
        return data.encode()[:STRING_CHARACTERS] + b'\n\0'
    if isinstance(data, (int, float)):
        return _normalize_number(data, digits)
    raise TypeError('unsupported type for data')

def _normalize_number(data, digits):
    """Normalize a numeric (integer or floating point) value."""
    data = float(data)
    if math.isnan(data):
        return b'+nan\n\0'
    if math.isinf(data):
        return b'+inf\n\0' if data > 0 else b'-inf\n\0'
    if data == 0.0:
        return b'+0.e+\n\0' if math.copysign(1, data) > 0 else b'-0.e+\n\0'
    # At this point we have a non-special number.  To match the
    # behavior of the R UNF package (and, as far as I can tell, the
    # IQSS code), we don't round the original values but rather scale
    # the values so all of the significant digits are to the left of
    # the decimal point, then round to integers, and then scale back.
    # See ROUNDING.md for more information.
    if data < 0:
        sign = '-'
        data = -data
    else:
        sign = '+'
    exp = int(math.floor(math.log10(data)))
    data_s = str(_rint(data * 10**(digits-1-exp)))
    i_part = data_s[0]
    f_part = data_s[1:].rstrip('0')
    if exp == 0:
        data = f'{sign}{i_part}.{f_part}e+\n\0'
    else:
        data = f'{sign}{i_part}.{f_part}e{exp:+d}\n\0'
    return data.encode()

def _rint(n):
    """Round n to the nearest integer, towards even if a tie."""
    n_int = int(math.floor(n))
    if n == n_int + 0.5:
        return n_int + 1 if n_int % 2 else n_int
    return int(round(n))

# --- numpy functionality -----------------------------------------------

def _normalize_numpy(data, digits):
    """Normalize a numpy array.

    The array must have a numeric data type.
    """

    if not numpy.issubdtype(data.dtype, int) \
            and not numpy.issubdtype(data.dtype, float):
        raise ValueError('data type must be integer or floating point')

    if data.ndim == 2:
        if data.shape[0] == 1:
            data = data.ravel()
    elif data.ndim != 1:
        raise ValueError('numpy arrays must be 1- or 2-D')

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
    # These values shouldn't be possible since we check for data subtypes 
    # of int or float before we use this function.  We therefore can't 
    # test this without calling this function directly.  But we leave 
    # this in place for unanticipated paths to get here.
    if (exp > 999).any():
        raise ValueError('value overflow (exponent too large)')
    if (exp < -999).any():
        raise ValueError('value underflow (exponent too small)')
    n_int = numpy.rint(
        data_c * numpy.float_power(10, (digits-1-exp))
    ).astype(int)

    # --- generate normalization strings

    s = numpy.full(n_int.shape, '+', dtype='S{}'.format(digits+7))
    s[signs < 0] = b'-'

    dpow = 10**(digits-1)
    n_ipart = numpy.floor_divide(n_int, dpow)
    n_fpart = n_int % dpow

    n_ipart = n_ipart.astype('uint8') + 48
    n_ipart.dtype = 'S1'

    s += n_ipart + b'.'

    n_fpart_s = numpy.empty((digits-1, *n_fpart.shape), dtype='uint8')
    for i in range(digits-1):
        n_fpart_s[i,:] = n_fpart % 10
        n_fpart //= 10
    n_fpart_s += 48
    n_fpart_s.dtype = 'S1'
    remove = numpy.full(n_fpart.shape, True)
    for i in range(digits-1):
        remove &= n_fpart_s[i,:] == b'0'
        n_fpart_s[i,remove] = b''
    for i in range(digits-2, -1, -1):
        s += n_fpart_s[i,]

    # minus signs will come from the exponent itself
    exp_sign_arr = numpy.full(n_int.shape, '+', dtype='S1')
    exp_sign_arr[exp < 0] = b'-'
    exp = numpy.abs(exp)

    s += b'e' + exp_sign_arr

    # TODO check exp range
    exp_s = numpy.empty((3, *exp.shape), dtype='uint8')

    for i in range(3):
        exp_s[i,:] = exp % 10
        exp //= 10
    exp_s += 48
    exp_s.dtype = 'S1'
    remove = numpy.full(exp.shape, True)
    for i in range(2, -1, -1):
        remove &= exp_s[i,:] == b'0'
        exp_s[i,remove] = b''

    s += exp_s[2,:]+exp_s[1,:]+exp_s[0,:]

    # --- set normalization strings for special values
    s[nan_inds] = b'+nan'
    s[numpy.logical_and(inf_inds, signs > 0)] = b'+inf'
    s[numpy.logical_and(inf_inds, signs < 0)] = b'-inf'
    s[numpy.logical_and(zero_inds, signs > 0)] = b'+0.e+'
    s[numpy.logical_and(zero_inds, signs < 0)] = b'-0.e+'

    if s.ndim == 1:
        data = b'\n\0'.join(s) + b'\n\0'
    else:
        digests = [ _digest(b'\n\0'.join(row).decode(), digits) for row in s ]
        digests.sort()
        return _normalize(digests, digits)

    return data

# --- pandas functionality ----------------------------------------------

def _normalize_pandas(data, digits):
    if isinstance(data, pandas.Series):
        # None comes out of a series as nan, so we map that back here.
        # We would want to map pandas.NA to None as well, but pandas.NA 
        # requires a series of data type object, so its use is unsupported 
        # due to our data type requirements.
        if data.dtype.kind in ['i', 'u']:
            vals = [ None if math.isnan(v) else int(v) for v in data ]
        elif data.dtype.kind == 'f':
            vals = [ None if math.isnan(v) else float(v) for v in data ]
        else:
            raise ValueError(f'unsupported pandas data type {data.dtype}')
        return _normalize(vals, digits)
    elif isinstance(data, pandas.DataFrame):
        # Special case: 
        #     UNF of a data frame (datafile) with 1 variable:
        #     The UNF of the data frame is the same as the UNF of the variable.
        # https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html
        names = list(data)
        if len(names) == 1:
            return _normalize(data[names[0]], digits)
        digests = [ _digest(data[name], digits) for name in data ]
        digests.sort()
        return _normalize(digests, digits)
    else:
        msg = 'pandas normalize requires a pandas Series or DataFrame'
        raise TypeError(msg)
    return b''

# eof
