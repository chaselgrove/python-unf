# python-unf

unf contains Python code for Universal Numeric Fingerprints (UNFs).

UNFs are defined at 
http://guides.dataverse.org/en/latest/developers/unf/index.html.

Usage:

    >>> import unf
    >>> unf.unf(1.23456789)
    'UNF:6:vcKELUSS4s4k1snF4OTB9A=='
    >>> unf.unf(1.23456789, 9)
    'UNF:6:N9:IKw+l4ywdwsJeDze8dplJA=='

## Basic usage

UNFs are calculated according to [UNF Version 6 (1)][1].

The number of rounding digits can be specified, but the string
truncation length and the hash truncation length are fixed to the
specification defaults (128 bytes and 128 bits, respectively).

`None` can be used to indicate a missing value, so to match the
example "Vector (numeric): {1.23456789, &lt;MISSING VALUE&gt;, 0}"
([1]), use:

    >>> unf.unf([1.23456789, None, 0])
    'UNF:6:Do5dfAoOOFt4FSj0JcByEw=='

Existing implementations include [IQSS/UNF (2)][2] and the [R UNF
package (3)][3].  The data structures supported by these implementations
require sequences containing values of a single data type.  Although
the UNF specification does not explicitly allow or forbid it, this
implementation does allow sequences containing multiple basic data
types.  Compound sequences (sequences containing sequences) are
forbidden for native Python data types.

## NumPy support

NumPy arrays are supported:

    >>> unf.unf(numpy.array([1, 2, 3]))
    'UNF:6:AvELPR5QTaBbnq6S22Msow=='

Only numeric NumPy data types are supported.

Note that 2-D NumPy arrays are interpreted as collections of vectors
and are subject to the digest-sort-digest rule for "higher-level
objects" ([1]).  So:

- `numpy.array([[1, 2], [3, 4]])` is treated as a collection of
  vectors `[1, 2]` and `[3, 4]` and will be evaluated the same way
  as a data frame with two variables.  This will therefore evaluate
  to the same UNF as `numpy.array([[3, 4], [1, 2]]))`, so the UNF is
  _not_ suitable for matrices.
- `numpy.array([[1, 2]])` is interpreted as a collection of one
  vector and evaluates to the same UNF as the vector itself,
  `numpy.array([1, 2])`.
- `numpy.array([[1], [2]])` is treated as a collection of two
  (one-element) vectors.

Primitives (non-arrays) with NumPy data types and arrays of greater
than two dimensions are not supported.

Note that NumPy does not have a special indicator for a missing
value.  If we try to use `None` as we did in the pure Python example,
we find that NumPy translates it to `nan`:

    >>> a = numpy.array([None], dtype=float)
    >>> a
    array([nan])

which is itself a special value (distinct from a missing value)
where UNFs are concerned.  NumPy arrays should therefore not be
used when data is missing.

## pandas support

pandas series and data frames are supported:

    >>> unf.unf(pandas.Series([1, 2, 3]))
    'UNF:6:AvELPR5QTaBbnq6S22Msow=='
    >>> unf.unf(pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]}))
    'UNF:6:Np0sj111a+rrJBgl6wNF9w=='

Only numeric data types are supported.

Behavior on multi-indexed data frames is undefined.

pandas does have an indicator for missing values (`pandas.NA`), but
its use requires a series of data type `object`, which is not
supported.  And like NumPy, pandas translates `None` to `NaN`, so
there is no unambiguous way to indicate missing data in pandas.
pandas objects should therefore not be used when data is missing.

## References

[1]: https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html
1: [https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html][1]

[2]: https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
2: [https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt][2]

[3]: https://github.com/leeper/UNF
3: [https://github.com/leeper/UNF][3]

## See also

Please see ROUNDING.md for a note about rounding.
