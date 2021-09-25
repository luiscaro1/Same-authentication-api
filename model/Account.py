from config.db_config import pg_config
import psycopg2

class AccountDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn=psycopg2.connect(connection_url)
#getting all the users from the db
    def getAllUsers(self):
        cursor=self.conn.cursor()
        query="select * from user_account;"
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(row)
        return result
#get a specific user by id
    def getUser(self,uaid):
        cursor=self.conn.cursor()
        query='select * from user_account where uaid=%s;'
        cursor.execute(query,(uaid,))
        result=cursor.fetchone()
        return result
#Creating a new user
    def addUser(self,uaemail, uausername, uapassword, firstname, lastname, dob, isActive, isCoach,uaplatform):
        cursor=self.conn.cursor()
        query='insert into user_account(uaemail,uausername,uapassword,firstname,lastname,dob,isActive,isCoach,uaplatform) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) returning uaid'
        cursor.execute(query,(uaemail, uausername, uapassword, firstname, lastname, dob, isActive, isCoach,uaplatform,))
        uaid=cursor.fetchone()
        self.conn.commit()
        return uaid
#updating a user
    def updateUser(self,uausername,uapassword,uaplatform, uaid):
        cursor=self.conn.cursor()
        query="update user_account set uausername=%s, uapassword=%s,"\
        "uaplatform=%s where uaid=%s returning *"
        cursor.execute(query,(uausername,uapassword,uaplatform, uaid))
        uausername=cursor.fetchone()
        self.conn.commit()
        return uausername
#deleting a user, by deleting a user the isActive will turn to false
    def deleteUser(self,uaid):
        cursor=self.conn.cursor()
        query='update user_account set isActive=false where uaid=%s returning *'
        cursor.execute(query,(uaid,))
        result=cursor.fetchone()
        self.conn.commit()
        return result

    def validateUser(self, uausername, uapassword):
        cursor=self.conn.cursor()
        query="""select uausername
        from user_account
        where uausername=%s and uapassword=%s """
        cursor.execute(query,(uausername, uapassword))
        result=cursor.fetchone()
        return result
#check if a token has been blacklisted
    def check_blacklist(self,token):
        query="select count(*) from blacklist where token=%s"
        # print(query)
        cursor=self.conn.cursor()
        cursor.execute(query,(token,))
        result=cursor.fetchone()
        if result:
           return True
        else:
            return False

#used token is blacklisted
    def blacklist(self,token,uaid):
        cursor=self.conn.cursor()
        query="insert into blacklist(token,uaid) values (%s,%s)"
        cursor.execute(query,(token,uaid,))
        self.conn.commit()
        return "Token has been blacklisted"
       


    
