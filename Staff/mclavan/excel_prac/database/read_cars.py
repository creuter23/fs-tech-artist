#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys


con = lite.connect('rba_info.db')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM RBA")

    rows = cur.fetchall()

    for row in rows:
        print row