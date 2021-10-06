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
 #check that the credential for the username and password belong to a user already in the database
    def validateUser(self, uausername, uapassword):
        cursor=self.conn.cursor()
        query="""select uaid, uausername
        from user_account
        where uausername=%s and uapassword=%s """
        cursor.execute(query,(uausername, uapassword))
        result=cursor.fetchone()
        return result

    #query to verify if email is already in use
    def emailExist(self, uaemail):
        cursor = self.conn.cursor()
        query = """ select uaemail
        from user_account
        where uaemail = %s"""
        cursor.execute(query,(uaemail,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    
    #query to verify if username is already taken
    def usernameExist(self, uausername):
        cursor = self.conn.cursor()
        query = """ select uausername
        from user_account
        where uausername = %s"""
        cursor.execute(query,(uausername,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    #verifies if the password is valid
    def validPassword(self, uapassword):
        length = len(uapassword)
        upper = False
        lower = False
        num = False
        sc = False
        if length < 8:
            return "Password must have 8 characters or more. password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"
        else:
            for i in uapassword:
                if upper == False:
                  if i.isupper():
                      upper = True
                elif lower == False:
                    if i.islower():
                        lower = True
                elif num == False:
                    if i.isnumeric():
                        num = True
                else:
                    if not i.isalnum():
                        sc = True
                if upper == True and lower == True and num == True and sc == True:
                    break
            if upper == False:
                return "Password does not contain upper case letter. password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"
            elif lower == False:
                return "Password does not contain lower case letter. password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"
            elif num == False:
                return "Password does not contain a number. password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"
            elif sc == False:
                return "Password does not contain a special character. password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"
            else:
                return False

    
