import web_site.backend.usage as u
from web_site.backend.database import db
from math import isclose
from datetime import datetime, timedelta
from web_site import app


def test_getUsage():
    d = u.getUsageData(start=datetime(2022,1,1), end=datetime(2022,6,30))
    assert len(d["usage_electricity"]) == 6
    assert len(d["usage_water"]) == 6
    assert len(d["cost_electricity"]) == 6
    assert len(d["cost_water"]) == 6
    pass

