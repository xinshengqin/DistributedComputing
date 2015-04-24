#!/usr/bin/python


from job_manager import *
import time
import numpy
import sqlite3 as DBI

manager=job_manager('./table.db')
# print manager.check_result(1)
# print manager.check_result(2)
#print manager.get_parameters(2)
#manager.store_result(3, 2, 1)
# manager.change_problem_status(1, 0)
# manager.change_problem_time(1,1418207807)
db = DBI.connect('table.db')
cursor=db.cursor()
cursor.execute('SELECT id,min(parameter.last_assigned_time) FROM parameter WHERE statusid>1;')
item=cursor.fetchone()
print item
db.commit()


