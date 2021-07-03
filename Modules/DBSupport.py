from settings.AppSettings import *
from Modules.AppLogging import *

import sqlite3
import pymysql
import base64
import os

logger = Logging("DBHELPER")

#context manager local
class DbOpenlocal():
  def __init__(self):
    self.conn = sqlite3.connect(os.path.join(ROOT_APP_PATH,APP_FILES,DB_NAME))
  def __enter__(self):
    return self.conn
  def __exit__(self,exc_type,exc_val,traceback):
    self.conn.close()

#context manager
class DbOpenServer():
  def __init__(self,*,host,port,username,dbname,passwd):
    self.conn = None
    self.host = host
    self.port = port
    self.username = username
    self.dbname = dbname
    self.passwd = passwd
  def __enter__(self):
    self.conn = pymysql.connect(host=self.host,port=self.port,passwd = self.passwd,database=self.dbname,user=self.username)
    return self
  def __exit__(self,exc_type,exc_value,exc_traceback):
    self.conn.close()

class DbInit():
    def __init__(self,conn,updatebar):
        logger.info("Running Init Database")
        self.updatebar = updatebar
        self.updatebar.update_bar(10,"Init Data Sequence..")
        self.Quelist = ['What was your childhood nickname?', 'What is the name of your favorite childhood friend?', 'What school did you attend for sixth grade?', 'What was the name of your first pet animal?', 'In what city does your nearest sibling live?', 'In what city or town was your first job?', 'What was your favorite sport in high school?', "What is your pet's name?", 'In what year was your father born?', 'In what year was your mother born?', "What is your mother’s (father's) first name?", 'What was the color of your first car?', "What is your father's middle name?", 'In what county where you born?', 'How many bones have you broken?', 'On which wrist do you wear your watch?', 'What is the color of your eyes?', 'What is your favorite animal?', 'What was the last name of your favorite teacher?', 'What is your favorite team?', 'What is your favorite movie?', "What is your favorite teacher's nickname?", 'What is your favorite TV program?', 'What is your least favorite nickname?', 'What is your favorite sport?', 'What is the name of your hometown?', 'What is the color of your father’s eyes?', 'What is the color of your mother’s eyes?', 'What was the name of your first pet?', 'What sports team do you love to see lose?', 'In what city were you born?', 'What is your favorite color?', 'What was your hair color as a child?', 'What is your work address?', 'What is your address, phone number?']
        self.updatebar.update_bar(10,"Creating References..")
        logger.info("Creating Relations")
        self.createTables(conn=conn)
        logger.info("Successfully Created")
    def createTables(self,*,conn):
        conn.execute("create table if not exists QUESTIONS(id integer primary key, Question)")
        conn.execute("create table if not exists USERS(Username text, Password text, Email text, RecoveryQue text,RecoveryAns text,Uniqueid int primary key)")
        conn.execute("create table if not exists DATA (Id integer primary key, Userid integer not null,site text,username text, credentials text, icon text,FOREIGN KEY (Userid) REFERENCES USERS (Uniqueid))")
        conn.commit()
        self.updatebar.update_bar(10,"Init Relations Done..")
        cursor = conn.cursor()
        self.updatebar.update_bar(10,"Managing Encryption")
        if cursor.execute("select count(*) from QUESTIONS").fetchone()[0] == 0:
            count = 0
            for Que in self.Quelist:
                count += 1
                cursor.execute("insert into QUESTIONS values(?,?)",[count,Que])
                self.updatebar.update_bar(1,str(50+count)+"%")
        conn.commit()

class DBHelper():
    def create_user(self,*,conn,user,passs,email,que,ans):
        cursor = conn.cursor()
        uniquekey = len(cursor.execute("select * from USERS").fetchall()) + 1
        ans = base64.b64encode(ans.encode("ascii")).decode("utf-8")
        cursor.execute("insert into USERS values (?,?,?,?,?,?)",[user.upper(),passs,email,que,ans,uniquekey])
        conn.commit()
        logger.info("New User Created Successfully")
    def check_user(self,*,conn,user):
        cursor = conn.cursor()
        if len(cursor.execute("select * from USERS where Username ='{}'".format(user.upper())).fetchall()) > 0:
            return True
        else:
            return False
    def get_password(self,*,conn,user,passs):
        cursor = conn.cursor()
        data = cursor.execute("select Password from USERS where Username='{}'".format(user.upper())).fetchone()
        if data[0] == passs:
            return True        
        else:
            return False
    def getemail(self,*,conn,user,passs):
        cursor = conn.cursor()
        data = cursor.execute("select Email,Uniqueid from USERS where Username='{}' and Password='{}'".format(user.upper(),passs)).fetchone()
        if data[0]:
            return data[0],data[1]
        else:
            return "Email not provided" , data[1]
    def getQuestion(self,*,conn,user):
        cursor = conn.cursor()
        que , ans  = cursor.execute("select RecoveryQue ,RecoveryAns from USERS where Username='{}'".format(user.upper())).fetchone()
        if que and ans:
            return que , base64.b64decode(ans.encode("ascii")).decode("utf-8")
        
        else:
            return None , None
    def update_pass(self,*,conn,user,passs):
        cursor = conn.cursor()
        cursor.execute("update USERS set Password ='{}' where Username = '{}'".format(passs,user.upper()))
        conn.commit()
    def add_credentials(self,*,conn,userid,site,username,credentials,icon):
        cursor = conn.cursor()
        data =  cursor.execute("select * from DATA").fetchall()
        if len(data) == 0:
            id = 1
        else:
            id = data[-1][0] + 1 
        cursor.execute("insert into DATA (Id,Userid,site,username, credentials, icon) values (?,?,?,?,?,?) ",[id,userid,site,username,credentials,icon])
        conn.commit()
        logger.info("Credentials Commited")
    def get_all_credentials(self,*,conn,userid):
        data = None
        cursor = conn.cursor()
        data = cursor.execute(f"select * from DATA where Userid={userid}").fetchall()
        return data
    def delete_credentials(self,*,conn,id,userid):
        cursor = conn.cursor()
        cursor.execute(f"delete from DATA  where Id={id} and Userid={userid}").fetchall()
        conn.commit()
        logger.info("Credentials Deleted")


