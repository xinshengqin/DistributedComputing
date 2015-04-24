'''
Created on Dec 4, 2014

@author: shawn
'''
def create_database ():

    import sqlite3 as DBI
    import sys
    db = DBI.connect('table.db')
    with db:
        cursor = db.cursor()

#parameter
        cursor.execute("DROP TABLE IF EXISTS parameter;")    
        #cursor.execute("CREATE TABLE parameter(parameterid INT NOT NULL PRIMARY KEY, p1 FLOAT, p2 FLOAT);")
        cursor.execute("CREATE TABLE parameter(id INT NOT NULL PRIMARY KEY, statusid INT, p1 FLOAT, p2 FLOAT);")

#problemstatus
        cursor.execute("DROP TABLE IF EXISTS problemstatus;")    
        cursor.execute("CREATE TABLE problemstatus(id INT NOT NULL PRIMARY KEY, status TINYTEXT);")
        #1 is 'assigned', 0 is 'unassigned'
        cursor.execute("INSERT INTO problemstatus VALUES(0,'unassigned');")
        cursor.execute("INSERT INTO problemstatus VALUES(1,'assigned');")

#user
        cursor.execute("DROP TABLE IF EXISTS user;")
        cursor.execute("CREATE TABLE user(id INT NOT NULL PRIMARY KEY, name TINYTEXT, statusid INT);")

#userstatus
        cursor.execute("DROP TABLE IF EXISTS userstatus;")    
        cursor.execute("CREATE TABLE userstatus(id INT NOT NULL PRIMARY KEY, status TINYTEXT);")
        # 0 is 'lost connection', 1 is 'busy', 
        cursor.execute("INSERT INTO userstatus VALUES(0,'lost connection');")
        cursor.execute("INSERT INTO userstatus VALUES(1,'busy');")

#result
        cursor.execute("DROP TABLE IF EXISTS result;")    
        cursor.execute("CREATE TABLE result(id INT NOT NULL PRIMARY KEY, answer FLOAT);")


#contributor
        cursor.execute("DROP TABLE IF EXISTS contributor;")
        cursor.execute("CREATE TABLE contributor(userid INT, resultid INT);")

#jobstatus
        cursor.execute("DROP TABLE IF EXISTS jobstatus;")    
        cursor.execute("CREATE TABLE jobstatus(id INT NOT NULL PRIMARY KEY, status TINYTEXT);")
        #1 is 'waiting for results', 2 is 'right', 3 is 'wrong'
        cursor.execute("INSERT INTO jobstatus VALUES(0,'waiting for results');")
        cursor.execute("INSERT INTO jobstatus VALUES(1,'mission completed');")
        cursor.execute("INSERT INTO jobstatus VALUES(2,'mission failed');")
        
#joblist
        cursor.execute("DROP TABLE IF EXISTS joblist;")    
    #what is the TIME type????
        #cursor.execute("CREATE TABLE joblist(id INT NOT NULL PRIMARY KEY, parameterid INT, userid INT, jobstatusid INT, timestatus TIME);")
        cursor.execute("CREATE TABLE joblist(id INT NOT NULL PRIMARY KEY, parameterid INT, userid INT, jobstatusid INT, startingtime INT);") 


#Problem 1 is marked as assigned
        cursor.execute("INSERT INTO parameter VALUES(0,1,5,1);")
        cursor.execute("INSERT INTO parameter VALUES(1,1,2,0.25);")
        cursor.execute("INSERT INTO parameter VALUES(2,1,0,0.75);")
        cursor.execute("INSERT INTO parameter VALUES(3,0,0.5,0.1);")
        cursor.execute("INSERT INTO parameter VALUES(4,0,1.234,0.321);")

#for testing
        cursor.execute("INSERT INTO result VALUES(2,0.5);")
        cursor.execute("INSERT INTO joblist VALUES(0,3,0,0,1231242342);")
        cursor.execute("INSERT INTO user VALUES(0,'intel',0);")


    db.commit()
###############################################################################
#Testing if it worked
create_database()
import sqlite3 as DBI
db = DBI.connect('table.db')
print("table:")    
cursor = db.cursor()
cursor.execute("SELECT * FROM parameter")
query = cursor.fetchall()
print(query)