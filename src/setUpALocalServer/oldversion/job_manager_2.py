#!/usr/bin/python

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
        #return a list of parameters,
        #and update some tables in the database.

        #add new job to joblist table. 
        #self.add_to_joblist(self.get_new_jobid(), new_parameterid, userid, jobstatusid, int(time()))
        self.add_to_joblist(userid, parameterid)
        self.change_problem_time(parameterid,int(time()))
        #return a list of parameters for client to compute
        return self.get_parameters(parameterid)
       
   
#This function works and has been tested
    def add_to_joblist(self,userid,parameterid):
        #This function write something to the joblist 
        new_jobid=self.get_new_jobid()
        self.cursor.execute("INSERT INTO joblist VALUES({},{},{});".format(new_jobid,parameterid,userid))
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
    
#tested
    def change_problem_time(self,parameterid,assigned_time):
        self.cursor.execute('UPDATE parameter SET last_assigned_time = {} WHERE id = {};'.format(assigned_time,parameterid))
        self.db.commit()
    
    def change_problem_status(self,parameterid,statusid):
        self.cursor.execute('UPDATE parameter SET statusid = {} WHERE id = {};'.format(statusid,parameterid))
        self.db.commit()

            
#This function works and has been tested
#It handle when there is no unassigned problems in the table
    def get_new_parameterid(self):
        #This will return the id of problems that has not been solved
        #And it will always return a parameterid that has the smallest time stamp, 
        #which means that problem has not been assigned or was assigned the longest time before
        current_time_in_second = int(time())
        #The sentence below select from where current_time - last_assign_time > 60,
        #and fetch the one that has the smallest last_assigned_time
        #If there is no proper candidate, fetchone() will get a tuple: (None,None)
        self.cursor.execute('SELECT id,min(parameter.last_assigned_time) FROM parameter WHERE ({}-parameter.last_assigned_time) > 60 AND parameter.statusid = 0;'.format(current_time_in_second))
        newid=self.cursor.fetchone()
        if ( newid[0] == None)  or ( newid == None) :#fetchone() can not fetch anything, which means there is no unassigned problem
            #print 'There is no unassigned problem currently'
            return None 
        else:
            return newid[0]
        
#tested
    def check_result(self,parameterid):
        #if problem with ID, parameterid, has a result in result table, this function return True. Or it return False.
        self.cursor.execute('SELECT result.id FROM result WHERE result.id = {}'.format(parameterid))
        result = self.cursor.fetchone()
        if result == None:
            return False
        else:
            return True
#tested
    def store_result(self,result,userid,parameterid):
        self.cursor.execute('SELECT result.id FROM result WHERE result.id = {}'.format(parameterid))
        item = self.cursor.fetchone()
        if item == None:
            self.cursor.execute("INSERT INTO result VALUES({},{});".format(parameterid,result))
            self.cursor.execute("INSERT INTO contributor VALUES({},{});".format(userid,parameterid))
        else:
            self.cursor.execute('UPDATE result SET answer = {} WHERE id = {};'.format(result,parameterid))
            self.cursor.execute('UPDATE contributor SET userid = {} WHERE resultid = {};'.format(userid,parameterid))
        self.db.commit()


        
    def add_link(self, id1, id2):
        self.links += " AND ({} = {})".format(id1,id2)
        self.nlinks += 1
        # print(self.links)
#tested
    def get_parameters(self,parameterid):
        #given parameter.id, this function will return a list of parameters like [p1,p2...]
        self.cursor.execute('SELECT p1,p2,p3,p4,p5 FROM parameter WHERE parameter.id = {}'.format(parameterid))
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
            self.cursor.execute('INSERT INTO user VALUES({},{})'.format(newid, '"Empty"'))
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
                self.cursor.execute('INSERT INTO user VALUES({},{})'.format(newid, username))
                self.db.commit()
                return newid
            else:
                print "The server found this user in database and give it the old userID"
                oldid = results[0]
                return oldid
#Display contents of table of user and parameter 
    def display_user(self):
        self.cursor.execute("SELECT * FROM user;") #Select everything in user table
        desc = self.cursor.description #titles of columns
        print("| {:<16} | {:<16} |".format(desc[0][0], desc[1][0])) #print the titlea of columns
        for item in self.cursor.fetchall(): #print contents of the table
            print("| {:<16} | {:<16} |".format(*item))
        
    def display_parameter(self):
        self.cursor.execute("SELECT parameter.id, problemstatus.status,parameter.last_assigned_time, parameter.p1, parameter.p2, parameter.p3, parameter.p4, parameter.p5 FROM parameter, problemstatus WHERE parameter.statusid=problemstatus.id;")
        #Select everything in parameter table as showing the status in text, not in id.
        desc = self.cursor.description #titles of columns
        print("| {:<4} | {:<16} | {:<18} | {:<16} | {:<16} | {:<16} | {:<16} | {:<16} |".format(desc[0][0], desc[1][0],desc[2][0],desc[3][0],desc[4][0],desc[5][0],desc[6][0],desc[7][0]))
        #print the titles of columns
        for item in self.cursor.fetchall(): #print contents of the table
            print("| {:<4} | {:<16} | {:<18} | {:<16} | {:<16} | {:<16} | {:<16} | {:<16} |".format(*item)) 

        
#####testing PART
#manager=job_manager('./table.db')
#manager.get_new_parameterid()
#manager.display_parameter()
#print manager.assign_a_job(3)
#manager.add_to_joblist(3, 3, 2, 0, 12312)
#print manager.get_parameters(4)
#username='Empty'
#print manager.register_user(username)
