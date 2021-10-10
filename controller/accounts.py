from flask import jsonify, request
from model.Account import AccountDAO

class BaseAccounts:
    #getting all the user accounts from the data base
    def getAllUsers(self):
        dao=AccountDAO()
        accountlist=dao.getAllUsers()
        result=[]
        for row in accountlist:
            obj=self.builtmapdict(row)
            result.append(obj)
        return jsonify(result)

    def builtmapdict(self,row):

        result={}
        result['uid']=row[0]
        result['email']=row[3]
        result['user_name']=row[5]
        result['password']=row[4]
        result['first_name']=row[1]
        result['last_name']=row[2]
        result['is_active']=row[6]


        return result

    def built_attr_dic(self,uid,email,user_name,password,first_name,last_name,is_active):
        result={}
        result['uid']=uid
        result['email']=email
        result['user_name']=user_name
        result['password']=password
        result['first_name']=first_name
        result['last_name']=last_name
        result['is_active']=is_active
        return result
    
    def built_attr_dic2(self,token,uid):
        result={}
        result['token']=token
        result['uid']=uid
        return result

    # return a user from the database that matches the given ID
    def getUser(self, uid):
        dao = AccountDAO()
        user_tuple = dao.getUser(uid)
        if not user_tuple:
            return jsonify('Not Found'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200


    # create a new user account and then it is added to the databasae
    def addUser(self, json):
    
        email = json['email']
        user_name = json['user_name']
        password = json['password']
        first_name = json['first_name']
        last_name = json['last_name']
        is_active = True
        dao = AccountDAO()
        ve = dao.emailExist(email)#verifies if the email is already in use
        if ve:
            return "this email is already taken"
        else:
            ue = dao.usernameExist(user_name) #verifies if the username is alreadt taken
            if ue:
                return "username is already taken, please try a different one"
            else:
                vp = dao.validPassword(password) #verifies if the password is valid
                if vp == False: # this is that the password is valid
                   uid = dao.addUser(email, user_name, password, first_name, last_name, is_active)
                   result = self.built_attr_dic(uid,email, user_name, password, first_name, last_name, is_active)
                   return jsonify(result), 201
                else: # this is when the password does not meet a requirement
                    return vp
                    

    # Update the information of an existing user, in this case the user can update the username, password, and the platform
    def UpdateUser(self, json, uid):
        dao = AccountDAO()
        user_name = json['user_name']
        password = json['password']
        user_tuple = dao.updateUser(user_name, password, uid)
        if not user_tuple:
            return jsonify('No such user'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200

    # delete an account from the database 
    def deleteUser(self, uid):
        dao = AccountDAO()
        user_tuple = dao.deleteUser(uid)
        if not user_tuple:
            return jsonify('No such user'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200

    # process which the user has to go through in order to gain access to their 
    # account and be able to utilize the features of the webapplication
    def Log_in(self,json):
        dao = AccountDAO()
        user_name = json['user_name']
        password = json['password']
        user_tuple = dao.validateUser(user_name, password)
        if user_tuple:
            result = self.builtmapdict(user_tuple)
            return result
        else:
            return False
            
    #process to search to whom the cookie belongs to
    def getCookieOwner(self, user):

        dao = AccountDAO()
        user_tuple = dao.getUser(user)
        result =self.builtmapdict(user_tuple)
      
        if(user_tuple):
            return jsonify(result)
        else:
            return None


