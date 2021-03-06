from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import hexlify, unhexlify
import datetime
import math
import sys


def _format_time(timespan, precision=3):
    """Formats the timespan in a human readable form
    
    >>> _format_time(0.35)
    '350 ms'

    >>> _format_time(35)
    '35 s'

    >>> _format_time(3500)
    '58min 20s'


    lovingly borrowed from
    https://github.com/ipython/ipython/blob/master/IPython/core/magics/execution.py

    """

    if timespan >= 60.0:
        # we have more than a minute, format that in a human readable form
        # Idea from http://snipplr.com/view/5713/
        parts = [("d", 60*60*24),("h", 60*60),("min", 60), ("s", 1)]
        time = []
        leftover = timespan
        for suffix, length in parts:
            value = int(leftover / length)
            if value > 0:
                leftover = leftover % length
                time.append(u'%s%s' % (str(value), suffix))
            if leftover < 1:
                break
        return " ".join(time)

    units = [u"s", u"ms", u"us", u"ns"]  # the save value   
    scaling = [1, 1e3, 1e6, 1e9]
        
    if timespan > 0.0:
        order = min(-int(math.floor(math.log10(timespan)) // 3), 3)
    else:
        order = 3
    return u"%.*g %s" % (precision, timespan * scaling[order], units[order])


def isoformat(o):
    """convert datetime.datetime to iso formatted timestamp

    >>> dt = datetime.datetime(2019, 10, 15, 10, 23, 41, 115927)
    >>> isoformat(dt)
    '2019-10-15T10:23:41.115927Z'

    """

    # stolen from connexion flask_app.py
    assert isinstance(o, datetime.datetime)
    if o.tzinfo:
        # eg: '2015-09-25T23:14:42.588601+00:00'
        return o.isoformat('T')
    # No timezone present - assume UTC.
    # eg: '2015-09-25T23:14:42.588601Z'
    return o.isoformat('T') + 'Z'


def hex_to_base64url(s):
    return urlsafe_b64encode(unhexlify(s)).decode("ascii")

def base64url_to_hex(s):
    return hexlify(urlsafe_b64decode(s)).decode("ascii")

