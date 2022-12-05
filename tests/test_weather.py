from web_site.backend.weather import weather
import meteostat
from math import isclose
from datetime import datetime, timedelta

def test_nearestStation_BHM():
    #default is BHM
    a = weather()
    retval = a.nearestStation()
    assert retval.index.T[0] == '72228' #BHM Airport weather station
    
"""
# old, no need to override location anymore
def test_nearestStation_SFO():
    a = weather()
    retval = a.nearestStation(meteostat.Point(37.6213,-122.3790))
    assert retval.index.T[0] == '72494' #SFO Airport weather station
"""

def test_hourly():
    a = weather()
    retval = a.getHourlyTempData(datetime.now() - timedelta(days = 1))
    # should be a day's worth of data
    assert len(retval) == 24
    #oldest should be within two days
    assert retval[0]['datetime'] > datetime.now() - timedelta(days = 2)
    #newest should be in the past
    assert retval[len(retval)-1]['datetime'] < datetime.now()

def test_temp_conversion():
    a = weather()
    assert isclose(a.celsius_to_farenheit(0.0),32.0)
    assert isclose(a.celsius_to_farenheit(float(100)),212)
    assert isclose(a.celsius_to_farenheit(37.0),98.6)

"""
# DATA MODIFICATION, DO NOT RUN IN PROD!

def test_writeHourlyTempsToDB():
    a = weather()
    assert a.writeHourlyTempsToDB() == True

def test_writeHourlyTempsToDB__date_range():
    a = weather()
    daysback = 7
    for i in range(daysback,1,-1):
        start = datetime.now() - timedelta(days = i)
        end = start + timedelta(days = 1)
        a.writeHourlyTempsToDB(start=start, end=end)
"""