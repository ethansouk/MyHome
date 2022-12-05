import web_site.backend.cycles as cycle
from web_site.backend.database import db
from math import isclose
from datetime import datetime, timedelta
from web_site import app

"""
# DESTRUCTIVE TESTS, DO NOT RUN IN PROD!
def test_run_cycle():
    cycle.daily(dtm=datetime.now() - timedelta(days=2))

def test_generate_all_cycles():
    daysback = 365
    daysforward = 30
    for i in range(daysback,1,-1):
        start = datetime.now() - timedelta(days = i)
        cycle.daily(dtm=start)
    for i in range(0,daysforward,1):
        start = datetime.now() + timedelta(days = i)
        cycle.daily(dtm=start)
"""