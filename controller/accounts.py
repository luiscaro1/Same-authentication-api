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
        result['uaid']=row[0]
        result['uaemail']=row[1]
        result['uausername']=row[2]
        result['uapassword']=row[3]
        result['firstname']=row[4]
        result['lastname']=row[5]
        result['dob']=row[6]
        result['isActive']=row[7]
        result['isCoach']=row[8]
        result['uaplatform']=row[9]

        return result

    def built_attr_dic(self,uaid,uaemail,uausername,uapassword,firstname,lastname,dob,isActive,isCoach,uaplatform):
        result={}
        result['uaid']=uaid
        result['uaemail']=uaemail
        result['uausername']=uausername
        result['uapassword']=uapassword
        result['firstname']=firstname
        result['lastname']=lastname
        result['dob']=dob
        result['isActive']=isActive
        result['isCoach']=isCoach
        result['uaplatform']=uaplatform
        return result
    
    def built_attr_dic2(self,token,uaid):
        result={}
        result['token']=token
        result['uaid']=uaid
        return result

    # return a user from the database that matches the given ID
    def getUser(self, id):
        dao = AccountDAO()
        user_tuple = dao.getUser(id)
        if not user_tuple:
            return jsonify('Not Found'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200


    # create a new user account and then it is added to the databasae
    def addUser(self, json):
        uaemail = json['uaemail']
        uausername = json['uausername']
        uapassword = json['uapassword']
        firstname = json['firstname']
        lastname = json['lastname']
        dob = json['dob']
        isActive = True
        isCoach=False
        uaplatform=json['uaplatform']

        dao = AccountDAO()
        ve = dao.emailExist(uaemail)#verifies if the email is already in use
        if ve:
            return "this email is already taken"
        else:
            ue = dao.usernameExist(uausername) #verifies if the username is alreadt taken
            if ue:
                return "username is already taken, please try a different one"
            else:
                vp = dao.validPassword(uapassword) #verifies if the password is valid
                if vp == False: # this is that the password is valid
                   id = dao.addUser(uaemail, uausername, uapassword, firstname, lastname, dob, isActive, isCoach,uaplatform)
                   result = self.built_attr_dic(id,uaemail,uausername, uapassword, firstname, lastname, dob, isActive,isCoach,uaplatform)
                   return jsonify(result), 201
                else: # this is when the password does not meet a requirement
                    return vp
                    

    # Update the information of an existing user, in this case the user can update the username, password, and the platform
    def UpdateUser(self, json, id):
        dao = AccountDAO()
        uausername = json['uausername']
        uapassword = json['uapassword']
        uaplatform=json['uaplatform']
        user_tuple = dao.updateUser(uausername, uapassword, uaplatform, id)
        if not user_tuple:
            return jsonify('No such user'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200
    # delete an account from the database 
    def deleteUser(self, id):
        dao = AccountDAO()
        user_tuple = dao.deleteUser(id)
        if not user_tuple:
            return jsonify('No such user'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200
    # process which the user has to go through in order to gain access to their 
    # account and be able to utilize the features of the webapplication
    def Log_in(self,json):
        dao = AccountDAO()
        uausername = json['uausername']
        uapassword = json['uapassword']
        user_tuple = dao.validateUser(uausername, uapassword)

        if user_tuple:
            return str(user_tuple[0]), user_tuple[1]
        else:
            return False

    def getCookie(self):
        cookie = request.cookies.get('uaid')
        return cookie


