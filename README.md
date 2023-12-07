# python-unf

unf contains Python code for Universal Numeric Fingerprints (UNFs).

UNFs are defined at 
http://guides.dataverse.org/en/latest/developers/unf/index.html.

Usage:

    >>> import unf
    >>> unf.unf(1.23456789)
    'UNF:6:vcKELUSS4s4k1snF4OTB9A=='
    >>> unf.unf(1.23456789, digits=9)
    'UNF:6:N9:IKw+l4ywdwsJeDze8dplJA=='

Please see ROUNDING.md for a note about rounding.
