from datetime import datetime, timedelta
from web_site.backend.database import db
from uuid import uuid4

class config(object):
    def clearConfig(self):
        retval = True
        a = db(local=True)
        retval = a.checkdb() if retval == True else False
        retval = a.truncateTable("sensors") if retval == True else False
        retval = a.truncateTable("sensor_data") if retval == True else False
        retval = a.truncateTable("state_type") if retval == True else False
        retval = a.truncateTable("authorized_devices") if retval == True else False
        retval = a.truncateTable("usage_electricity") if retval == True else False
        retval = a.truncateTable("usage_water") if retval == True else False
        return retval

    def getOrCreateOutsideSensor(self):
        a = db()
        sensor_outside = a.select("select * from sensors where name = 'outside_temp'")
        if len(sensor_outside) == 0:
            i = {}
            i['sensor_id'] = str(uuid4())
            i['name'] = 'outside_temp'
            i['sensor_type'] = 'temp'
            i['location'] = 'outside'
            i['energy_uom'] = 'None'
            i['energy_value'] = 0
            a.insertRow(row= i,tblName='sensors')
            o = a.select("select * from sensors where sensor_id = '" + i['sensor_id'] + "' limit 1;")
            if len(o) == 0:
                raise Exception("Sensor not created!")
            return o
        else:
            return sensor_outside

    def getOrCreateStateTypes(self):
        a = db()
        state_types = a.select("select * from state_type;")
        if len(state_types) == 0:
            i = {}
            i["state_type_id"] = str(uuid4())
            i["name"] = "temperature"
            a.insertRow(row= i,tblName='state_type')
            i["state_type_id"] = str(uuid4())
            i["name"] = "on_off"
            a.insertRow(row= i,tblName='state_type')
            i["state_type_id"] = str(uuid4())
            i["name"] = "open_close"
            a.insertRow(row= i,tblName='state_type')
            o = a.select("select * from state_type;")
            if len(o) == 0:
                raise Exception("State Types not created")
            return o
        else:
            return state_types