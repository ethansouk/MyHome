from web_site.backend.database import db as database
from math import isclose
from datetime import datetime, timedelta
from web_site import app
from uuid import uuid4


def most_recent_temp(dtm: datetime):
    dtm = datetime(2022,1,15,12,00)

    dtm = str(dtm)
    #inside_temp
    inside_temp = "3a103efe-db7f-4559-a187-237bb986418f"
    #outside_temp
    outside_temp = "c1bcc780-3296-4ce8-84f1-ce0f0274e8b6"
    #thermostat
    thermostat = "97d3f284-e9ed-46d7-9b08-6d31c6a17f62"

    db = database()
    sql = "select value from sensor_data where dtm <= '" + dtm + "' and sensor_id = '" + inside_temp + "' limit 1;"
    data = db.select(sql)
    for i in range(len(data)):
        inside = float(data[i]['value'])

    db = database()
    sql = "select value from sensor_data where dtm <= '" + dtm + "' and sensor_id = '" + outside_temp + "' limit 1;"
    data = db.select(sql)
    for i in range(len(data)):
        outside = float(data[i]['value'])

    db = database()
    sql = "select value from sensor_data where dtm <= '" + dtm + "' and sensor_id = '" + thermostat + "' limit 1;"
    data = db.select(sql)
    for i in range(len(data)):
        setpoint = float(data[i]['value'])

    delta = (outside-inside)/5
    if abs(delta) > 1.0:
        new_inside = inside + delta
    
    #write the new inside temp
    d = {}
    d["data_id"] = str(uuid4())
    d["sensor_id"] = "3a103efe-db7f-4559-a187-237bb986418f"
    d["state_type_id"] = "5b31f9cd-15ce-4a85-91c6-21651778b61b"
    d["value"] = new_inside
    db.insertRow(d,"sensor_data")
    
    pass