import datetime
from uuid import uuid4
from flask import render_template, url_for, flash, redirect, request
from web_site import app
from web_site.backend.database import db as database
from web_site.backend.weather import weather as w
from web_site.backend.cycles import *
import web_site.backend.usage as u



@app.route("/")
@app.route("/index")
def home():
    try:
        db = database()
        data = {}
        
        temp = db.select("select sensor_id,sensor_type,name from sensors where name = 'washer';")
        
        # for each sensor id in temp insert a value into sensor_data
        # date = datetime.datetime.now() - datetime.timedelta(days=90)
        # for i in temp:
        #     for j in range(2):
        #         new2 = {}
        #         new2["data_id"] = str(uuid4())
        # #         # date 1 year ago
        #         new2["dtm"] = date + datetime.timedelta(days=j*30)
        #         new2["sensor_id"] = i["sensor_id"]
        #         if i["sensor_type"] == "on_off":
        #             new2["state_type_id"] = "70d066af-ffa0-4d25-8cb9-963656c590a6"
        #         if i["sensor_type"] == "open_close":
        #             new2["state_type_id"] = "6814bcbf-e054-49b6-bd13-ac9a7b75bede"
        #         if i["sensor_type"] == "temp" or i["sensor_type"] == "thermostat":
        #             new2["state_type_id"] = "5b31f9cd-15ce-4a85-91c6-21651778b61b"
        #         if new2['state_type_id'] == "70d066af-ffa0-4d25-8cb9-963656c590a6":
        #             new2["value"] = "off"
        #         if new2['state_type_id'] == "5b31f9cd-15ce-4a85-91c6-21651778b61b":
        #             new2["value"] = "90.00"
        #         if new2['state_type_id'] == "6814bcbf-e054-49b6-bd13-ac9a7b75bede":
        #             new2["value"] = "close"
        #         new2["predicted"] = False
        #         db.insertRow(new2,"sensor_data")
        #         new3 = {}
        #         new3["data_id"] = str(uuid4())
        # #         # date 1 year ago
        #         new3["dtm"] = date + datetime.timedelta(days=j*30) + datetime.timedelta(minutes=30)
        #         new3["sensor_id"] = i["sensor_id"]
        #         if i["sensor_type"] == "on_off":
        #             new3["state_type_id"] = "70d066af-ffa0-4d25-8cb9-963656c590a6"
        #         if i["sensor_type"] == "open_close":
        #             new3["state_type_id"] = "6814bcbf-e054-49b6-bd13-ac9a7b75bede"
        #         if i["sensor_type"] == "temp" or i["sensor_type"] == "thermostat":
        #             new3["state_type_id"] = "5b31f9cd-15ce-4a85-91c6-21651778b61b"
        #         if new3['state_type_id'] == "70d066af-ffa0-4d25-8cb9-963656c590a6":
        #             new3["value"] = "off"
        #         if new3['state_type_id'] == "5b31f9cd-15ce-4a85-91c6-21651778b61b":
        #             new3["value"] = "90.00"
        #         if new3['state_type_id'] == "6814bcbf-e054-49b6-bd13-ac9a7b75bede":
        #             new3["value"] = "close"
        #         new3["predicted"] = False
        #         db.insertRow(new3,"sensor_data")
                
        #     print("inserted for sensor id: " + i["name"])


        
        
        
        data["temp"] = {}
        temp_outside = db.select("SELECT sd.value, sd.dtm FROM sensor_data sd INNER JOIN sensors s ON s.sensor_id = sd.sensor_id AND s.name = 'outside_temp' AND sd.predicted = FALSE ORDER BY sd.dtm DESC LIMIT 1")
        data["temp"]["outside"] = int(float(temp_outside[0]['value']))
        temp_inside = db.select("SELECT sd.value, sd.dtm FROM sensor_data sd INNER JOIN sensors s ON s.sensor_id = sd.sensor_id AND s.name = 'inside_temp' AND sd.predicted = FALSE ORDER BY sd.dtm DESC LIMIT 1")
        data["temp"]["inside"] = int(float(temp_inside[0]['value']))
        thermostat = db.select("select sd.value, sd.dtm from sensor_data sd inner join sensors s on s.sensor_id = sd.sensor_id and s.name = 'thermostat' and sd.predicted = false order by sd.dtm desc limit 1")
        data["temp"]["thermostat"] = int(float(thermostat[0]['value']))
        
        temp = db.select("select x.sensor_id, x.value, x.dtm , x.name from (select sd.sensor_id, sd.value, sd.dtm, s.name ,row_number() OVER (PARTITION BY sd.sensor_id ORDER BY sd.dtm DESC)from sensor_data sd inner join sensors s on s.sensor_id = sd.sensor_id and sd.predicted = false) x where row_number = 1")
        
        # for each sensor id in temp create a data entry in data with the sensor id as the key and the value as the last value in sensor_data
        
        for i in temp:
            data[i['name']] = i['value']

        app.config['data'] = data
            
        print(data)
    except Exception as e:
        data = {}
        data["temp"] = {}
        data["temp"]["outside"] = 69
        data["temp"]["inside"] = 69
        data["temp"]["thermostat"] = 72
    finally:
        return render_template('index.html',title="Home",data=data)


@app.route("/usage")
def usage():
    data = app.config['data']
    return render_template('usage.html',title="Usage", data = data)

@app.route("/getusagedata")
def getUsageData():
    tz = pytz.timezone("America/Chicago")
    start = datetime.strptime(request.args.get('start'),"%Y-%m-%d")
    end = datetime.strptime(request.args.get('end'),"%Y-%m-%d")
    start = tz.localize(start)
    end = tz.localize(end)
    return u.getUsageData(start=start, end=end)


@app.route("/testing")
def testing():
    data = app.config['data']
    return render_template('testing.html',title="Testing", data = data)

@app.route("/test1")
def test1():
    
    tz = pytz.timezone("America/Chicago")
    dtm = tz.localize(datetime.now())
    
    # run oven 5 times and wait on success
    try:
        for i in range(5):
            print("run oven")
            oven(dtm)
        
    except Exception as e:
        return "error", 500
    
    finally:
        print("success")
        data = app.config['data']
        return redirect(url_for('usage'))
    

@app.route("/test2")
def test2():
    tz = pytz.timezone("America/Chicago")
    dtm = tz.localize(datetime.now())
    
    # run washer 5 times and wait on success
    try:
        for i in range(5):
            print("run washer")
            washer(dtm)
        
    except Exception as e:
        return "error", 500
    
    finally:
        print("success")
        data = app.config['data']
        return redirect(url_for('usage'))
    
    
    


