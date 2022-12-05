from datetime import datetime, timedelta
from web_site.backend.database import db as database
from uuid import uuid4
from web_site import app
from flask import request

@app.route("/api")
def api_main():
    r = {}
    r["status"] = "Done"
    return r

@app.route("/api/toggle")
def toggle_device():
    db = database()
    last_value = db.select("select sd.value, sd.dtm, sd.sensor_id, sd.state_type_id, s.name from sensor_data sd inner join sensors s on s.sensor_id = sd.sensor_id and s.name = '" + request.args.get('id') + "' and sd.predicted = false and dtm <= now() order by sd.dtm desc limit 1 ")
    new = {}
    new["data_id"] = str(uuid4())
    new["sensor_id"] = last_value[0]['sensor_id']
    new["state_type_id"] = last_value[0]['state_type_id']
    new["predicted"] = False
    if last_value[0]['value'] == "close":
        new["value"] = "open"
    if last_value[0]['value'] == "open":
        new["value"] = "close"
    if last_value[0]['value'] == "on":
        new["value"] = "off"
    if last_value[0]['value'] == "off":
        new["value"] = "on"
    db.insertRow(new,"sensor_data")
    new["id"] = last_value[0]['name']
    new["dtm"] = last_value[0]['dtm']
        
    return new

@app.route("/api/thermostat_increase")
def increase():
    db = database()
    last_value = db.select("select sd.value, sd.dtm, sd.sensor_id, sd.state_type_id, s.name from sensor_data sd inner join sensors s on s.sensor_id = sd.sensor_id and s.name = '" + request.args.get('id') + "' and sd.predicted = false order by sd.dtm desc limit 1 ")
    new = {}
    new["data_id"] = str(uuid4())
    new["sensor_id"] = last_value[0]['sensor_id']
    new["state_type_id"] = last_value[0]['state_type_id']
    new["predicted"] = False
    new["value"] = int(float(last_value[0]['value'])) + 1
    db.insertRow(new,"sensor_data")
    new["id"] = last_value[0]['name']
    new["dtm"] = last_value[0]['dtm']
    return new

@app.route("/api/thermostat_decrease")
def decrease():
    db = database()
    last_value = db.select("select sd.value, sd.dtm, sd.sensor_id, sd.state_type_id, s.name from sensor_data sd inner join sensors s on s.sensor_id = sd.sensor_id and s.name = '" + request.args.get('id') + "' and sd.predicted = false order by sd.dtm desc limit 1 ")
    new = {}
    new["data_id"] = str(uuid4())
    new["sensor_id"] = last_value[0]['sensor_id']
    new["state_type_id"] = last_value[0]['state_type_id']
    new["predicted"] = False
    new["value"] = int(float(last_value[0]['value'])) - 1
    db.insertRow(new,"sensor_data")
    new["id"] = last_value[0]['name']
    new["dtm"] = last_value[0]['dtm']
    return new