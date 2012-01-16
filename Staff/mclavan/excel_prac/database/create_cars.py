#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

try:
    con = lite.connect('rba_info.db')

    cur = con.cursor()  

    cur.executescript("""
        DROP TABLE IF EXISTS Cars;
        CREATE TABLE RBA(Id INT, FirstName TEXT, LastName TEXT, StudentNum TEXT, Class INT);
        INSERT INTO RBA VALUES(1, "Margaret", "Rhoads", "1322452", 1109);
        INSERT INTO RBA VALUES(2, "Daniel", "Berry", "1513568", 1109);
        INSERT INTO RBA VALUES(3, "Raymond", "Rodriguez", "2109916", 1109);
        INSERT INTO RBA VALUES(4, "James", "Sasu", "1401297", 1109);
        """)

    con.commit()
    
except lite.Error, e:
    
    if con:
        con.rollback()
        
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close() 