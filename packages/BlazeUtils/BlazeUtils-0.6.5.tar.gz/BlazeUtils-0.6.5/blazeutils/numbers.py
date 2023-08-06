from __future__ import absolute_import
from __future__ import unicode_literals

from decimal import Decimal

from six.moves import map
from six.moves import range


# from http://docs.python.org/library/decimal.html#recipes
def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    if not isinstance(value, Decimal):
        if isinstance(value, float):
            value = str(value)
        value = Decimal(value)
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    if places > 0:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))
decimalfmt = moneyfmt  # noqa: E305


def round_down_to_n(x, rounder=5):
    return (x // rounder) * rounder


def convert_int(value):
    try:
        return int(value)
    except ValueError as e:
        if 'invalid literal for int()' not in str(e):
            raise
    except TypeError as e:
        # TypeError message is slightly different in Python 3
        msg = 'int() argument must be a string{0} or a number'
        msg2 = msg.format('')
        msg3 = msg.format(', a bytes-like object')
        if msg2 not in str(e) and msg3 not in str(e):
            raise
    return None


def ensure_int(value):
    retval = convert_int(value)
    if retval is None:
        return 0
    return retval
