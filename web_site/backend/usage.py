from web_site import app
from datetime import datetime, timedelta
import pytz
import calendar
from web_site.backend.database import db as database

def getUsageData(start: datetime=pytz.timezone("America/Chicago").localize(datetime.now()) - timedelta(days=365), end: datetime = pytz.timezone("America/Chicago").localize(datetime.now()) + timedelta(days=30)):
    """
    get Usage data, default to previous year
    """
    retval = {}
    
    #auto group based on timespan
    delta = end - start
    if delta.days >= 180:
        grpby = "month"
    elif delta.days < 180 and delta.days >= 42:
        grpby = "week"
    elif delta.days < 42 and delta.days >= 8:
        grpby = "day"
    else:
        grpby = "hour"
    
    sqlElectricity = "select DATE_TRUNC('" + grpby + "', dtm) date, sum(watts)/1000 kw from usage_electricity where dtm >= '" + str(start) + "' and dtm <= '" + str(end) + "' group by DATE_TRUNC('" + grpby + "', dtm) order by DATE_TRUNC('" + grpby + "', dtm);"
    sqlWater = "select DATE_TRUNC('" + grpby + "', dtm) date, sum(gallons)/7.48 ft3 from usage_water where dtm >= '" + str(start) + "' and dtm <= '" + str(end) + "' group by DATE_TRUNC('" + grpby + "', dtm) order by DATE_TRUNC('" + grpby + "', dtm);"

    db = database()
    usageElectricity = db.select(sql = sqlElectricity)
    usageWater = db.select(sql = sqlWater)

    e = {}
    for i in range(len(usageElectricity)):
        e[str(usageElectricity[i]['date'])] = usageElectricity[i]['kw']

    w = {}
    for i in range(len(usageWater)):
        w[str(usageWater[i]['date'])] = usageWater[i]['ft3']

    cost_e = {}
    for i in range(len(usageElectricity)):
        cost_e[str(usageElectricity[i]['date'])] = usageElectricity[i]['kw'] * 0.12

    cost_w = {}
    for i in range(len(usageWater)):
        cost_w[str(usageWater[i]['date'])] = usageWater[i]['ft3'] * 0.0252

    retval["usage_electricity"] = e
    retval["usage_water"] = w
    retval["cost_electricity"] = cost_e
    retval["cost_water"] = cost_w

    return retval
