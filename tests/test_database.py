from web_site import app
from web_site.backend.database import db
from pytest import raises
from uuid import uuid4

"""
SQL to populate initial state for all sensors:

insert into sensor_data 
(data_id, dtm, sensor_id, state_type_id, value, predicted)

select uuid_generate_v4(), '2020-01-01 00:00:00'::timestamptz
, s.sensor_id, st.state_type_id 
, case 
	when st.name = 'on_off' then 'off'
	when st.name = 'open_close' then 'close'
end
,false 
from sensors s 
inner join state_type st on st.name = s.sensor_type 
where s.sensor_id not in (select sensor_id from sensor_data sd)

"""


def test_checkdb():
    a = db()
    assert a.checkdb() == True

"""
# DESTRUCTIVE TESTS, NOT FOR USE IN PROD!!!

def test_insertOneRow_blind():
    i = {}
    i['sensor_id'] = str(uuid4())
    i['name'] = 'test alpha'
    i['sensor_type'] = 'window'
    i['location'] = 'kitchen'
    i['energy_uom'] = 'None'
    i['energy_value'] = 0
    a = db()
    assert a.insertRow(row=i,tblName='sensors') == True

def test_truncate_sensors_blind():
    a = db()
    assert a.truncateTable('sensors')

def test_insertOneRow_confirm():
    i = {}
    i['sensor_id'] = str(uuid4())
    i['name'] = 'test alpha'
    i['sensor_type'] = 'window'
    i['location'] = 'kitchen'
    i['energy_uom'] = 'None'
    i['energy_value'] = 0
    a = db()
    assert a.insertRow(row= i,tblName='sensors') == True
    o = a.select("select * from sensors where sensor_id = '" + i['sensor_id'] + "'")
    assert o[0] == i

def test_truncate_sensors_confirm():
    a = db()
    o = a.select("select count(*) from sensors")
    assert int(o[0]['count']) > 0
    assert a.truncateTable('sensors')
    o = a.select("select count(*) from sensors")
    assert int(o[0]['count']) == 0

def test_insertTwoRows_blind():
    rowDict = {}
    i = {}
    i['sensor_id'] = str(uuid4())
    i['name'] = 'test alpha'
    i['sensor_type'] = 'window'
    i['location'] = 'kitchen'
    i['energy_uom'] = 'None'
    i['energy_value'] = 0
    rowDict[0] = i
    i = {}
    i['sensor_id'] = str(uuid4())
    i['name'] = 'test bravo'
    i['sensor_type'] = 'window'
    i['location'] = 'kitchen'
    i['energy_uom'] = 'None'
    i['energy_value'] = 0
    rowDict[1] = i
    a = db()
    assert a.insertRowDict(rowDict=rowDict,tblName="sensors") == True
    test_truncate_sensors_confirm()

def test_insertTwoRows_confirm():
    rowDict = {}
    i = {}
    i['sensor_id'] = str(uuid4())
    i['name'] = 'test alpha'
    i['sensor_type'] = 'window'
    i['location'] = 'kitchen'
    i['energy_uom'] = 'None'
    i['energy_value'] = 0
    rowDict[0] = i
    i = {}
    i['sensor_id'] = str(uuid4())
    i['name'] = 'test bravo'
    i['sensor_type'] = 'window'
    i['location'] = 'kitchen'
    i['energy_uom'] = 'None'
    i['energy_value'] = 0
    rowDict[1] = i
    a = db()
    assert a.insertRowDict(rowDict=rowDict,tblName="sensors") == True
    o = a.select("select * from sensors where sensor_id = '" + rowDict[0]['sensor_id'] + "'")
    assert o[0] == rowDict[0]
    o = a.select("select * from sensors where sensor_id = '" + rowDict[1]['sensor_id'] + "'")
    assert o[0] == rowDict[1]
    test_truncate_sensors_confirm()

"""
    

