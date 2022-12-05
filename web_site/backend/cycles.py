from web_site import app
from datetime import datetime, timedelta
import pytz
from web_site.backend.database import db
from uuid import uuid4
from random import randrange

"""
A 'cycle' is defined here as a set of activities that 
    occurs at a particular time. These activities are
    approximations of the sequence of events that 
    occur within the household.

Any given cycle may involve devices/sensors changing 
    state, usage of electricity, and/or usage of 
    water. Cycles include indirect usage, such as a
    hot water heater consuming electricity to heat
    water used during a shower or washing clothes.

The daily function is called externally to process all
    of the cycles for a given day per the project
    requirements.

"""

def daily(dtm: datetime):
    """
    Create sensor data for a given day
    """
    tz = pytz.timezone("America/Chicago")
    dtm = tz.localize(dtm)

    #everyday
    refrigerator(dtm.replace(hour=23,minute=59))

    if dtm.date().weekday() in range(0,5):
        # Monday-Friday
        shower(dtm.replace(hour=5,minute=randrange(59)),"bathroom_1_fan")
        shower(dtm.replace(hour=5,minute=randrange(59)),"bathroom_2_fan")
        bath(dtm.replace(hour=19,minute=randrange(59)),"bathroom_1_fan")
        bath(dtm.replace(hour=20,minute=randrange(59)),"bathroom_2_fan")
        microwave(dtm.replace(hour=18,minute=randrange(59)))
        tv_livingroom(dtm.replace(hour=22,minute=randrange(59)))
        tv_bedroom(dtm.replace(hour=22,minute=randrange(59)))
        for i in range(8):
            #morning front door
            front_door(dtm.replace(hour=7,minute=30+i))
            pass
        for i in range(4):
            #evening front door - children
            front_door(dtm.replace(hour=16,minute=0+i))
            pass
        for i in range(4):
            #evening front door - adults
            front_door(dtm.replace(hour=17,minute=30+i))
            pass
        pass
    else:
        #Saturday-Sunday
        shower(dtm.replace(hour=5,minute=randrange(59)),"bathroom_1_fan")
        shower(dtm.replace(hour=5,minute=randrange(59)),"bathroom_1_fan")
        shower(dtm.replace(hour=6,minute=randrange(59)),"bathroom_2_fan")
        bath(dtm.replace(hour=19,minute=randrange(59)),"bathroom_1_fan")
        bath(dtm.replace(hour=19,minute=randrange(59)),"bathroom_2_fan")
        bath(dtm.replace(hour=20,minute=randrange(59)),"bathroom_2_fan")
        microwave(dtm.replace(hour=13,minute=randrange(59)))
        tv_livingroom(dtm.replace(hour=22,minute=randrange(59)))
        tv_bedroom(dtm.replace(hour=22,minute=randrange(59)))
        for i in range(32):
            front_door(dtm.replace(hour=randrange(7,22),minute=0+i))
            pass
        pass
    if dtm.weekday() == 0:
        #Monday
        wash_clothes(dtm.replace(hour=randrange(17,21),minute=randrange(59)))
        pass
    if dtm.weekday() == 1:
        #Tuesday
        dishwasher(dtm.replace(hour=randrange(17,21),minute=randrange(59)))
        wash_clothes(dtm.replace(hour=randrange(17,21),minute=randrange(59)))
        pass
    if dtm.weekday() == 2:
        #Wednesday
        wash_clothes(dtm.replace(hour=randrange(17,21),minute=randrange(59)))
        pass
    if dtm.weekday() == 3:
        #Thursday
        dishwasher(dtm.replace(hour=randrange(17,21),minute=randrange(59)))
        pass
    if dtm.weekday() == 4:
        #Friday
        wash_clothes(dtm.replace(hour=randrange(17,21),minute=randrange(59)))
        pass
    if dtm.weekday() == 5:
        #Saturday
        dishwasher(dtm.replace(hour=randrange(8,21),minute=randrange(59)))
        pass
    if dtm.weekday() == 6:
        #Sunday
        dishwasher(dtm.replace(hour=randrange(8,21),minute=randrange(59)))
        pass

def front_door(dtm:datetime):
    set_state(id="front_door",state="open",dtm=dtm - timedelta(seconds=30))
    set_state(id="front_door",state="close",dtm=dtm)
    pass

def shower(dtm: datetime, fan_id: str):
    database = db()
    # water
    water_total = 25
    w = {}
    w["usage_water_id"] = str(uuid4())
    w["dtm"] = dtm
    w["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    w["gallons"] = water_total
    database.insertRow(w, "usage_water")
    del w

    #electricity - hot water heater refill
    hot_water=water_total*0.65
    hot_water_reheat_minpergallon = 4.0
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = hot_water * hot_water_reheat_minpergallon * 4500/60
    database.insertRow(e, "usage_electricity")
    del e

    #electricity - bath fan
    duration_min = 15
    watts = 60
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")
    del e

    set_state(id=fan_id,state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id=fan_id,state="off",dtm=dtm)
    pass
    
def bath(dtm: datetime, fan_id: str):
    database = db()
    # water
    water_total = 30
    hot_water=water_total*0.65
    hot_water_reheat_minpergallon = 4.0
    w = {}
    w["usage_water_id"] = str(uuid4())
    w["dtm"] = dtm
    w["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    w["gallons"] = water_total
    database.insertRow(w, "usage_water")
    del w

    #electricity - hot water heater refill
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = hot_water * hot_water_reheat_minpergallon * 4500/60
    database.insertRow(e, "usage_electricity")
    del e

    #electricity - bath fan
    duration_min = 15
    watts = 60
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")
    del e

    set_state(id=fan_id,state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id=fan_id,state="off",dtm=dtm)
    pass

def microwave(dtm: datetime):
    database = db()
    duration_min = 20.0 if dtm.date().weekday() < 5 else 30.0
    watts = 1100
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="microwave",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="microwave",state="off",dtm=dtm)
    pass

def oven(dtm: datetime):
    database = db()
    duration_min = 45.0 if dtm.date().weekday() < 5 else 60.0
    watts = 4000
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="oven",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="oven",state="off",dtm=dtm)
    pass

def stove(dtm: datetime):
    database = db()
    duration_min = 15.0 if dtm.date().weekday() < 5 else 30.0
    watts = 3500
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="stove",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="stove",state="off",dtm=dtm)
    pass

def washer(dtm: datetime):
    database = db()
    # water
    water_total = 20
    w = {}
    w["usage_water_id"] = str(uuid4())
    w["dtm"] = dtm
    w["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    w["gallons"] = water_total
    database.insertRow(w, "usage_water")
    del w

    #electricity - hot water heater refill
    hot_water=water_total*0.85
    hot_water_reheat_minpergallon = 4.0
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = hot_water * hot_water_reheat_minpergallon * 4500/60
    database.insertRow(e, "usage_electricity")
    del e

    #electricity - washer
    duration_min = 30.0
    watts = 500
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")
    del e

    set_state(id="washer",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="washer",state="off",dtm=dtm)
    pass

def dryer(dtm: datetime):
    database = db()
    duration_min = 30.0
    watts = 3000
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="dryer",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="dryer",state="off",dtm=dtm)
    pass

def wash_clothes(dtm: datetime):
    washer(dtm)
    dryer(dtm + timedelta(minutes=30))
    pass

def dishwasher(dtm: datetime):
    database = db()
    # water
    water_total = 6
    hot_water=water_total*1.0
    hot_water_reheat_minpergallon = 4.0
    w = {}
    w["usage_water_id"] = str(uuid4())
    w["dtm"] = dtm
    w["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    w["gallons"] = water_total
    database.insertRow(w, "usage_water")
    del w

    #electricity - hot water heater refill
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = hot_water * hot_water_reheat_minpergallon * 4500/60
    database.insertRow(e, "usage_electricity")
    del e

    #electricity - dishwasher
    duration_min = 45
    watts = 1800
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")
    del e

    set_state(id="dishwasher",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="dishwasher",state="off",dtm=dtm)
    pass

def tv_livingroom(dtm: datetime):
    database = db()
    duration_min = 4 * 60.0 if dtm.date().weekday() < 5 else 8 * 60.0
    watts = 636
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="living_tv",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="living_tv",state="off",dtm=dtm)
    pass

def tv_bedroom(dtm: datetime):
    database = db()
    duration_min = 2 * 60.0 if dtm.date().weekday() < 5 else 4 * 60.0
    watts = 100
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="master_bedroom_tv",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="master_bedroom_tv",state="off",dtm=dtm)
    pass

def refrigerator(dtm: datetime):
    database = db()
    duration_min = 24 * 60.0
    watts = 150
    e = {}
    e["usage_electricity_id"] = str(uuid4())
    e["dtm"] = dtm
    e["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    e["watts"] = duration_min/60 * watts
    database.insertRow(e, "usage_electricity")

    set_state(id="refrigerator",state="on",dtm=dtm - timedelta(minutes=duration_min))
    set_state(id="refrigerator",state="off",dtm=dtm)
    pass

def set_state(id: str, state: str, dtm: datetime):
    database = db()
    sensor = database.select("select sd.value, sd.dtm, sd.sensor_id, sd.state_type_id, s.name from sensor_data sd inner join sensors s on s.sensor_id = sd.sensor_id and s.name = '" + id + "' and sd.predicted = false and dtm <= now() order by sd.dtm desc limit 1 ")
    new = {}
    new["data_id"] = str(uuid4())
    new["sensor_id"] = sensor[0]['sensor_id']
    new["state_type_id"] = sensor[0]['state_type_id']
    new["predicted"] = True if dtm > pytz.timezone("America/Chicago").localize(datetime.now()) else False
    new["dtm"] = dtm
    new["value"] = state
    database.insertRow(new,"sensor_data")
    new["id"] = sensor[0]['name']
    
    return new

