.. See file COPYING distributed with unf for copyright and license.

unf contains Python code for Universal Numeric Fingerprints (UNFs)

http://guides.dataverse.org/en/latest/developers/unf/index.html

Version 0.5.0 contains two important design decisions:

First, lists and tuples containing anything but primitives are not
allowed.  The UNF specification does not handle this case, presumably
since it was written with R in mind and nested vectors are not
allowed in R.  Versions of this package before 0.5.0 normalized
subsequences in place, but because normalized values are simply
concatenated in sequences, the normalization of (1, (2, 3)) would
then be the same as the normalization of (1, 2, 3) and the two would
have the same UNF.

Second, numpy arrays of greater than one dimension are handled the
same way that R data frames and matrices are handled, but without
the sorting step.  The UNFs for the components of an array are
calculated, the results are put in a list, and the UNF of the
resulting list is calculated.  numpy arrays with one dimension are
treated as simple sequences.
