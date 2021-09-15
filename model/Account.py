from config.db_config import pg_config
import psycopg2

class AccountDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn=psycopg2.connect(connection_url)
#getting all the users
    def getAllUsers(self):
        cursor=self.conn.cursor()
        query="select * from user_account;"
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(row)
        return result
#get user by id
    def getUser(self,uaid):
        cursor=self.conn.cursor()
        query='select uaid,uaemail,uausername,isActive from user_account where uaid=%s;'
        cursor.execute(query,(uaid,))
        result=cursor.fetchone()
        return result
#adding a new user
    def addUser(self,uaemail,uausername,uapassword,firstname,lastname,dob,isActive):
        cursor=self.conn.cursor()
        query='insert into user_account(uaemail,uausername,uapassword,fistname,lastname,dob,isActive,isCoach,uaplatform) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) returning uaid'
        cursor.execute(query,(uaemail,uausername,uapassword,firstname,lastname,dob,isActive,))
        uaid=cursor.fetchone()
        self.conn.commit()
        return uaid
#updating a user
    def updateUser(self,uaid,uaemail,uausername,uapassword,firstname,lastname,dob,isActive,isCoach,uaplatform):
        cursor=self.conn.cursor()
        query="update user_account set"\
              "uaemail=%s," \
              "uausername=%s, uapassword=%s," \
              "firstname=%s,lastname=%s," \
              "dob=%s, isActive=%s" \
              "isCoach=%s, uaplatform=%s" \
              "where uaid=%s" \
              "returnin username"
        cursor.execute(query,(uaid,uaemail,uausername,uapassword,firstname,lastname,dob,isActive,isCoach,uaplatform))
        uausername=cursor.fetchone()
        self.conn.commit()
        return uausername
#deleting a user
    def deleteUser(self,uaid):
        cursor=self.conn.cursor()
        query='update user_account set isActive=false where uaid=%s returning uiad, uaemail,uausername,isActive;'
        cursor.execute(query,(uaid,))
        result=cursor.fetchone()
        return result
        


    
    
