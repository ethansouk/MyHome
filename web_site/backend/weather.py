from web_site import app
from datetime import datetime, timedelta
import meteostat
from web_site.backend.database import db
from uuid import uuid4

class weather:
    def __init__(self) -> None:
        pass
    
    def celsius_to_farenheit(self, c: float = 0.0):
        if c is None:
            raise Exception("Celsius value must not be None")
        if type(c) is not float:
            raise Exception("Celsius value must be a Float")
        f = float(c * 1.8 + 32)
        return round(f,4)
    
    def nearestStation(self):
        location = meteostat.Point(app.config["HOME_LOCATION"][0],app.config["HOME_LOCATION"][1])
        return meteostat.Stations().nearby(location._lat, location._lon).fetch(1)

    def getHourlyTempData(self,start: datetime = datetime(2022,1,1,0,0), end: datetime = datetime.now()):
        station = self.nearestStation().index.T[0]
        data = meteostat.Hourly(station,start,end).fetch()
        retval = {}
        for i in data:
            if i == 'temp':
                ctr = 0
                for j in data.temp.axes[0]:
                    k = {}
                    k['datetime'] = data.temp.axes[0][ctr].to_pydatetime()
                    k['temp_c'] = float(data.temp.values[ctr])
                    k['temp_f'] = self.celsius_to_farenheit(float(data.temp.values[ctr]))
                    retval[ctr] = k
                    ctr += 1
            return retval

    def writeHourlyTempsToDB(self, start: datetime=datetime.now() - timedelta(days = 1),end:datetime=datetime.now()):
        data = self.getHourlyTempData(start=start,end=end)
        a = db()
        sensor_outside = a.select("select * from sensors where name = 'outside_temp'")
        state_type_temp = a.select("select * from state_type where name = 'temperature'")
        for i in data:
            chk = a.select("select * from sensor_data where dtm = '" + str(data[i]["datetime"]) + "' and sensor_id = '" + sensor_outside[0]["sensor_id"] + "'")
            if len(chk) > 0:
                continue
            o = {}
            o["data_id"] = str(uuid4())
            o["dtm"] = data[i]["datetime"]
            o["sensor_id"] = sensor_outside[0]["sensor_id"]
            o["state_type_id"] = state_type_temp[0]["state_type_id"]
            o["value"] = data[i]["temp_f"]
            a.insertRow(o,tblName="sensor_data")
        return True

    def getlastYearTempData(self,start: datetime = datetime(2021,1,1), end: datetime = datetime(2021,12,31)):
        station = self.nearestStation().index.T[0]
        data = meteostat.Monthly(station,start,end).fetch()
        retval = {}
        for i in data:
            if i == 'tavg':
                ctr = 0
                for j in data.axes[0]:
                    k = {}
                    k['datetime'] = data.axes[0][ctr].to_pydatetime()
                    k['temp_c'] = float(data.tavg.values[ctr])
                    k['temp_f'] = self.celsius_to_farenheit(float(data.tavg.values[ctr]))
                    retval[ctr] = k
                    ctr += 1
            return retval
        
    def getcurrentYearMonthlyTempData(self,start: datetime = datetime(2022,1,1), end: datetime = datetime.now()):
        station = self.nearestStation().index.T[0]
        data = meteostat.Monthly(station,start,end).fetch()
        retval = {}
        for i in data:
            if i == 'tavg':
                ctr = 0
                for j in data.axes[0]:
                    k = {}
                    k['datetime'] = data.axes[0][ctr].to_pydatetime()
                    k['temp_c'] = float(data.tavg.values[ctr])
                    k['temp_f'] = self.celsius_to_farenheit(float(data.tavg.values[ctr]))
                    retval[ctr] = k
                    ctr += 1
            return retval