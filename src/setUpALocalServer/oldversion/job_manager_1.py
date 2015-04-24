#!/usr/bin/python
#some notes
#when a mission fails, do not for get to change the parameter.statusid back to 0


#from zeitgeist.datamodel import get_timestamp_for_now
from time import *
import sqlite3 as DBI


class job_manager(object):
    
    def __init__(self,database_path):
        #The class should be initialized with a path to the database.
        self.db = DBI.connect('table.db')
        self.cursor=self.db.cursor()
        self.links=""#This string links some tables.
        self.nlinks = 0#number of links

        self.add_link('parameter.statusid', 'problemstatus.id')
        self.add_link('result.id','parameter.id')
        self.add_link('user.statusid','userstatus.id')
        self.add_link('joblist.jobstatusid','jobstatus.id')
        #print "Now all the default links are:{}".format(self.links)
        
    
    def assign_a_job(self,userid,parameterid):
        #This function should take id of the client that request for a job and problem ID as input,
        #return a list of parameters or None,
        #and update some tables in the database.
        new_parameterid=self.get_new_parameterid()

        #if self.get_new_parameterid() return -1, there is no problem to be solved
        if new_parameterid == -1:
            return None
        else:
            #add new job to joblist table. 
            #The input arguments are jobid, parameterid, userid, jobstatusid=1, time stamp.
            jobstatusid=0#0 means 'waiting for result'

            #self.add_to_joblist(self.get_new_jobid(), new_parameterid, userid, jobstatusid, get_timestamp_for_now())
            self.add_to_joblist(self.get_new_jobid(), new_parameterid, userid, jobstatusid, int(time()))
            
            #change parameter.statusid
            self.cursor.execute('UPDATE parameter SET statusid = 1 WHERE id = {};'.format(new_parameterid))

            #change_userstatus
            self.cursor.execute('UPDATE user SET statusid = 1 WHERE id = {}'.format(userid))
            
            self.db.commit()

            #return a list of parameters for client to compute
            return self.get_parameters(new_parameterid)
       
   
#This function works and has been tested
    def add_to_joblist(self,jobid,parameterid,userid,jobstatusid,timestamp): #note the time stamp will be unix epoch time in huge integer type    
        #This function write something to the joblist 
        print jobid,parameterid,userid,jobstatusid,timestamp
        self.cursor.execute("INSERT INTO joblist VALUES({},{},{},{},{});".format(jobid,parameterid,userid,jobstatusid,timestamp))
        self.db.commit()
        
        
        
# get_new_jobid function works and being tested, new jobid is given by +1 of last jobid.          
    def get_new_jobid(self):
        #This function return a jobid that has never been assigned
        #the return type is integer
        self.cursor.execute("SELECT id FROM joblist")
        n=0 #n is post jobid
        #job_number start from 0
        for item in self.cursor.fetchall():
            n+=1
        return n
            
#This function works and has been tested
#It handle when there is no unassigned problems in the table
    def get_new_parameterid(self):
        #This function return a new No. of problems that has not been solved
        #This will return the id of problems that has not been solved
        self.cursor.execute('SELECT parameter.id FROM parameter,result WHERE parameter.statusid = 0;')
        newid=self.cursor.fetchone()
        if newid == None:#fetchone() can not fetch anything, which means there is no unassigned problem
            print 'There is no unassigned problem currently'
            return None 
        else:
            return id[0]

        
    def change_userstatus(self,userid):
        pass
        
    def add_link(self, id1, id2):
        self.links += " AND ({} = {})".format(id1,id2)
        self.nlinks += 1
        # print(self.links)

#This function works and has been tested
    def get_parameters(self,parameterid):
        #given parameter.id, this function will return a list of parameters like [p1,p2...]
        self.cursor.execute('SELECT p1,p2 FROM parameter WHERE parameter.id = {}'.format(parameterid))
        data = self.cursor.fetchone()
        return data
    
    #No matter the input username exists in database or not, this function return a user.id corresponding to that username
    def register_user(self,username):

        if username == 'Empty':#If username is specified as "Empty", we should always assign it a new user.id
            
            print 'The Client did not specify a username. The server made it as default: "Empty".\n'
            #Give this user a new user.id in user table
            self.cursor.execute('SELECT user.id FROM user')
            ids = self.cursor.fetchall()
            newid = len(ids)#user.id starts from 0
            self.cursor.execute('INSERT INTO user VALUES({},{},{})'.format(newid, '"Empty"', '0'))
            self.db.commit()
            return newid
            
        else:
            username="'"+username+"'"#give username a pair of extra quote so that it can be used in sqlite3 command
            self.cursor.execute('SELECT user.id FROM user WHERE user.name = {} '.format(username))
            results = self.cursor.fetchone()

            if results == None:
                print "The server did not find such a user in database. A new userID was assigned"
                #Give this user a new user.id in user table
                self.cursor.execute('SELECT user.id FROM user')
                ids = self.cursor.fetchall()
                newid = len(ids)#user.id starts from 0
                self.cursor.execute('INSERT INTO user VALUES({},{},{})'.format(newid, username, '0'))
                self.db.commit()
                return newid
            else:
                print "The server found this user in database and give it the old userID"
                oldid = results[0]
                return oldid

    #Display contents of table of user and parameter        
    def display_user(self):
        self.cursor.execute("SELECT * FROM user;")
        desc = self.cursor.description
        print("| {:<16} | {:<16} | {:<4} |".format(desc[0][0], desc[1][0],desc[2][0]))
        for item in self.cursor.fetchall(): 
            print("| {:<16} | {:<16} | {:<8} |".format(*item))
        
    def display_parameter(self):
        self.cursor.execute("SELECT * FROM parameter;")
        desc = self.cursor.description
        print("| {:<4} | {:<8} | {:<16} | {:<16} |".format(desc[0][0], desc[1][0],desc[2][0],desc[3][0]))
        for item in self.cursor.fetchall(): 
            print("| {:<4} | {:<8} | {:<16} | {:<16} |".format(*item))


        
#####testing PART
#manager=job_manager('./table.db')
#manager.get_new_parameterid()
#print manager.assign_a_job(3)
#manager.add_to_joblist(3, 3, 2, 0, 12312)
#print manager.get_parameters(4)
#username='Empty'
#print manager.register_user(username)
