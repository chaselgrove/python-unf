# See file COPYING distributed with python-unf for copyright and license.

try:
    import numpy
except ImportError:
    numpy = None

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

    n_fpart_s = numpy.empty((digits-1, n_fpart.size), dtype='uint8')
    for i in range(digits-1):
        n_fpart_s[i,:] = n_fpart % 10
        n_fpart //= 10
    n_fpart_s += 48
    n_fpart_s.dtype = 'S1'
    remove = numpy.full(n_fpart.size, True)
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
    exp_s = numpy.empty((3, exp.size), dtype='uint8')

    for i in range(3):
        exp_s[i,:] = exp % 10
        exp //= 10
    exp_s += 48
    exp_s.dtype = 'S1'
    remove = numpy.full(exp.size, True)
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

    data = b'\n\0'.join(s) + b'\n\0'

    return data

# eof