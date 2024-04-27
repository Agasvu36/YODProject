# -*- coding: cp1251 -*-
import sqlite3 as sq
 
def dataBaseCler():
    with sq.connect("WarehouseData.db") as con:
        cur = con.cursor()
        cur.execute("""DROP TABLE""")

def databaseCreate():
    with sq.connect("WarehouseData.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        day TEXT,
        time TEXT,
        peopleCount INTEGER,
        Event TEXT
        )""")



def databaseAdd(day, time, peopleCount, event):
    maxId = 0
    with sq.connect("WarehouseData.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT max(id) FROM logs""")
        for row in cur.fetchall():
            maxId = row[0]
        if(maxId is None):
            maxId = 0
        else:
            maxId += 1
        

    with sq.connect("WarehouseData.db") as con:
       cur = con.cursor()
       print(day, time, peopleCount, event)
       cur.execute(f"""INSERT INTO logs VALUES({maxId}, '{day}', '{time}', {str(peopleCount)}, '{event}')""")

def databaseSelect():
    with sq.connect("WarehouseData.db") as con:
        cur = con.cursor()
        cur.execute("""SELECT time, Event FROM logs""")
        result = cur.fetchall()
        return result

def currentDaysLogPepleCount(arg):
    with sq.connect("WarehouseData.db") as con:
        cur = con.cursor()
        cur.execute(f"""SELECT time, peopleCount FROM logs
            WHERE day = '{arg}'""")
        result = cur.fetchall()
        return result

def currentDaysLog(arg):
    with sq.connect("WarehouseData.db") as con:
        cur = con.cursor()
        cur.execute(f"""SELECT time, Event FROM logs
            WHERE day = '{arg}'""")
        result = cur.fetchall()
        return result