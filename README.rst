.. See file COPYING distributed with python-unf for copyright and license.

unf contains Python code for Universal Numeric Fingerprints (UNFs).

http://guides.dataverse.org/en/latest/developers/unf/index.html

As of Version 0.6.0, N-dimensional numpy arrays are no longer
supported.  This was an ad-hoc addition to this package that is not
mentioned in the UNF specification.

Usage::

    >>> import unf
    >>> unf.unf(0.0)
    'UNF:6:YUvj33xEHnzirIHQyZaHow=='
