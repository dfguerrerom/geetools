"""Legacy tools for ``ee.Date``."""
from datetime import datetime

import ee
from deprecated.sphinx import deprecated


@deprecated(version="1.0.0", reason="Use ee.Date.geetools.toDateTime instead")
def toDatetime(date):
    """Convert from ee to ``datetime.datetime``."""
    return ee.Date(date).geetools.toDatetime()


@deprecated(version="1.0.0", reason="Epoch is the same for ee and python")
def millisToDatetime(millis):
    """Convert from milliseconds to ``datetime.datetime``."""
    return datetime.fromtimestamp(millis / 1000.0)


@deprecated(version="1.0.0", reason="Use ee.Date.geetools.unitSinceEpoch instead")
def unitSinceEpoch(date, unit="day"):
    """Get the number of units since epoch (1970-01-01)."""
    return ee.Date(date).geetools.unitSinceEpoch(unit)
