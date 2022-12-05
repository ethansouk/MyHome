from web_site.backend.config import config
from web_site.backend.database import db
from math import isclose
from datetime import datetime, timedelta

from web_site import app

def test_sensor_outside_temp():
    a = db()
    sensor_outside = a.select("select * from sensors where name = 'outside_temp'")
    assert len(sensor_outside) == 1

def test_load_config():
    a = config()
    a.getOrCreateStateTypes()
    assert a.getOrCreateOutsideSensor()[0]["name"] == "outside_temp"
    

