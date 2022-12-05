from web_site.backend.database import db as database
from math import isclose
from datetime import datetime, timedelta
from web_site import app
import web_site.backend.hvac as hvac


def test_most_recent_temp():
    hvac.most_recent_temp(datetime(2022,1,15,12,00))
    pass

