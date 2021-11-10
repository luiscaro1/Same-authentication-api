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
        query='select * from "User";'
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(row)
        return result
#get a specific user by id
    def getUser(self,uid):
        cursor=self.conn.cursor()
        query='select * from "User" where uid=%s;'
        cursor.execute(query,(uid,))
        result=cursor.fetchone()
        return result
    
#Creating a new user
    def addUser(self,email, user_name, password, first_name, last_name, is_active):
        cursor=self.conn.cursor()
        query='insert into "User"(email, user_name, password, first_name, last_name, is_active) values (%s,%s,%s,%s,%s,%s) returning uid'
        cursor.execute(query,(email, user_name, password, first_name, last_name, is_active,))
        uid=cursor.fetchone()
        self.conn.commit()
        return uid

#updating a user
    def updateUser(self,user_name,password, uid):
        cursor=self.conn.cursor()
        query='update "User" set user_name=%s, password=%s,'\
        "where uid=%s returning *"
        cursor.execute(query,(user_name,password, uid))
        user_name=cursor.fetchone()
        self.conn.commit()
        return user_name

#deleting a user, by deleting a user the isActive will turn to false
    def deleteUser(self,uid):
        cursor=self.conn.cursor()
        query='update "User" set is_active=false where uid=%s returning *'
        cursor.execute(query,(uid,))
        result=cursor.fetchone()
        self.conn.commit()
        return result

 #check that the credential for the username and password belong to a user already in the database
    def validateUser(self, user_name):
        cursor=self.conn.cursor()
        query="""select *
        from "User"
        where user_name=%s """
        cursor.execute(query,(user_name,))
        result=cursor.fetchone()
        return result

    #query to verify if email is already in use
    def emailExist(self, email):
        cursor = self.conn.cursor()
        query = """ select email
        from "User"
        where email = %s"""
        cursor.execute(query,(email,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    
    #query to verify if username is already taken
    def usernameExist(self, user_name):
        cursor = self.conn.cursor()
        query = """ select user_name
        from "User"
        where user_name = %s"""
        cursor.execute(query,(user_name,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    # query to get the uaid from the user_name, used for the token and cookie portion of the authentication portion of the webapp
    def getUid(self, user):
        cursor = self.conn.cursor()
        query = 'select uid from "User" where uid = %s;'
        cursor.execute(query,(user,))
        result = cursor.fetchone()
        return result

    #verifies if the password is valid
    def validPassword(self, password):
        length = len(password)
        upper = False
        lower = False
        num = False
        sc = False
        if length < 8:
            return "password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"
        else:
            for i in password:
                if lower == False:
                    if i.islower():
                        lower = True
                if upper == False:
                    if i.isupper():
                        upper = True
                if num == False:
                    if i.isnumeric():
                        num = True
                if sc == False:
                    if not i.isalnum():
                        sc = True
                if upper == True and lower == True and num == True and sc == True:
                    break
            if upper == True and lower == True and num == True and sc == True:
                return False
            else: 
                return "password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character"

    
