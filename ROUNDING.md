The UNF specification (Version 6 ([1])) states that for numeric
elements, we "round each vector element to N significant digits
using the IEEE 754 'round towards nearest, ties to even' rounding
mode."  The specification does not tell us if the rounding should
be done on the exact value or the floating-point representation of
the number.

The examples provided with the specification ([2]) are no help in
this respect.  The two high-precision values, 1.2345675 and
1.2345685, round trivially to 1.234568 because the floating-point
representation of each is slightly closer than its exact value to
1.234568.  So the "ties to even" rule does not apply if we consider
the floating-point representations.

A better example for our purposes is 1.2345635 and 1.2345645.  Both
exact values should round to 1.234564 by the "ties to even" rule,
but the floating-point representations are slightly less than and
slightly greater than the exact values, respectively, so they round
to 1.234563 and 1.234565.

However, both Dataverse itself and the R UNF package ([3]) process
these values as if they are exact, seeing a tie and rounding to the
nearest even.

In this implementation, I have decided to follow the established
UNF implementations rather than following what I read to be the
correct interpretation of the specification.  There is some ambiguity
in the specification, and since the end result is an identifier, I
believe it is more important to be consistent across implementations
than to fight a technicality (during which time we set up the
scientific archive for future confusion: is that an R UNF or a
Python UNF?).

The R package UNF (Version 2.0.7) uses `signif()` to round numbers
in its numeric normalization code (`as.unfvector.numeric()`).  This
in turn calls `fprec()` in the C code, which rounds by scaling
numbers so that all of the significant digits are to the left of
the decimal point and then rounding to an integer using `rint()`.  So
in our case, 1.2345635 is scaled to 1234563.5 and 1.2345645 is
scaled to 1234564.5, and these, having exact floating-point
representations, both round to 1234564, which is then scaled back
to 1.234564.  This code (python-unf) follows this algorithm in order
to match the R UNF implementation.

It is interesting to note that in R (Version 4.1.2), `signif()` and
`round()` behave differently when handling this sort of value: `signif()`
uses the scheme described above to emulate exact values:

    > signif(1.2345635, 7)
    [1] 1.234564

while `round()` appears to use the floating-point representation:

    > round(1.2345635, 6)
    [1] 1.234563

This contradicts the assertion in the R documentation ([4]) that:

    signif(x, dig) is the same as round(x, dig - ceiling(log10(abs(x))))

[1]: https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html
1: [https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html][1]

[2]: https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
2: [https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt][2]

[3]: https://github.com/leeper/UNF
3: [https://github.com/leeper/UNF][3]

[4]: https://stat.ethz.ch/R-manual/R-devel/library/base/html/Round.html
4: [https://stat.ethz.ch/R-manual/R-devel/library/base/html/Round.html][4]
