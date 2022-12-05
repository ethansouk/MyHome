from web_site import app
import psycopg2
from urllib.parse import urlparse
from psycopg2.extensions import AsIs
import psycopg2.extras
from uuid import uuid4
import socket

"""
## Database module for project

# Overriden class instantiator:
Default to connect to the production (UAB-hosted) database,
 optional parameter local = True for testing
Confirms connectivity (UAB-hosted db requires be on campus or on VPN)

# getConn():
Reusable to get a new connection to the db

# checkdb():
Confirms a simple sql command can be executed against the db.

# select():
Execute arbitary sql and return a dictionary with the results

# truncate():
Truncate a table

# insertRow():
Insert a single row. Row is a dictionary with keys = db field names
Example:
 row['Field1'] = 'ValueA'
 row['Field2'] = 'ValueB'
 row['Field3'] = 'ValueC'

# insertRowDict():
Insert multiple rows. Each row is a dictionary with keys = db field names, nested.
Example: 
 row[0]['Field1'] = 'ValueA'
 row[0]['Field2'] = 'ValueB'
 row[0]['Field3'] = 'ValueC'
 row[1]['Field1'] = 'ValueD'
 row[1]['Field2'] = 'ValueE'
 row[1]['Field3'] = 'ValueF'

"""



class db():
    def __init__(self) -> None:
        local = app.config["DB_LOCAL"]
        if local == True:
            self._uri = app.config["DB_LOCAL_URI"]
            self._dblocation = 'Local'
        else:
            self._uri = app.config["DB_REMOTE_URI"]
            self._dblocation = 'Remote'
        self._dbconn = urlparse(self._uri)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            result_of_check = s.connect_ex((self._dbconn.hostname,self._dbconn.port))
            if result_of_check != 0:
                raise Exception("ERROR: Could not reach " + str(self._dblocation).upper() + " " + str(self._dbconn.hostname + '\n Are you on the right network?'))    
        except Exception as e:
            raise Exception("ERROR: Could not reach " + str(self._dblocation).upper() + " " + str(self._dbconn.hostname + '\n Are you on the right network?'))
        finally:    
            s.close()

    def getConn(self):
        conn = None
        try:
            conn = psycopg2.connect(
                database = self._dbconn.path[1:],
                user = self._dbconn.username,
                password = self._dbconn.password,
                host = self._dbconn.hostname,
                port = self._dbconn.port
            )
            return conn
        except Exception as e:
            print("ERROR in getConn: ")
            print(e)
            return None

    def checkdb(self):
        try:
            conn = self.getConn()
            sql = "SELECT version();"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            conn.rollback()
            return False

    def insertRow(self,row,tblName):
        try:
            conn = self.getConn()
            cur = conn.cursor()
            columns = row.keys()
            values = [row[column] for column in columns]
            sql = "insert into " + tblName + ' (%s) values %s'
            cur.execute(sql, (AsIs(','.join(columns)), tuple(values)))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("ERROR in insertRow() triggered ROLLBACK: ")
            print(e)
            print()
            print(row)
            conn.rollback()
            return False
    
    def insertRowDict(self,rowDict,tblName):
        try:
            conn = self.getConn()
            cur = conn.cursor()
            columns = rowDict[0].keys()
            
            values = []
            for i in rowDict:
                values.append(list(rowDict[i].values()))

            sql = "insert into " + tblName + ' (%s) values %%s' % (AsIs(','.join(columns)))
            psycopg2.extras.execute_values(cur,sql, tuple(values))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("ERROR in insertRowDict() triggered ROLLBACK: ")
            print(e)
            print()
            conn.rollback()
            return False
    
    def truncateTable(self, tblName):
        try:
            conn = self.getConn()
            sql = "truncate table " + tblName + ' cascade;'
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("ERROR in truncateTable(" + tblName + ") triggered ROLLBACK: ")
            print(e)
            conn.rollback()
            return False

    def select(self, sql: str):
        try:
            if sql is None:
                return None
            if len(sql) < 8 or sql.lower().startswith('select') == False:
                return None
            conn = self.getConn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(sql)
            returnDict = cur.fetchall()
            return returnDict
        except Exception as e:
            print(e)
            return None

