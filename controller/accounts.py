from flask import jsonify
from model.Account import AccountDAO

class BaseAccounts:
    #getting all the user accounts
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
        # result['uapassword']=row[3]
        # result['firstname']=row[4]
        # result['lastname']=row[5]
        # result['dob']=row[6]
        result['isActive']=row[3]
        # result['isCoach']=row[8]
        # result['uaplatform']=row[9]

        return result

    def built_attr_dic(self,uaid,uaemail,uausername,uapassword,firstname,lastname,dob,isActive,isCoach,uaplatform):
        result={}
        result['uaid']=uaid
        result['email']=uaemail
        result['username']=uausername
        result['password']=uapassword
        result['firstname']=firstname
        result['lastname']=lastname
        result['dob']=dob
        result['isActive']=isActive
        result['isCoach']=isCoach
        result['platform']=uaplatform
        return result

    def getUser(self, id):
        dao = AccountDAO()
        user_tuple = dao.getUser(id)
        if not user_tuple:
            return jsonify('Not Found'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200

    def deleteUser(self, id):
        dao = AccountDAO()
        user_tuple = dao.deleteUser(id)
        if not user_tuple:
            return jsonify('No such user'), 404
        else:
            result = self.builtmapdict(user_tuple)
            return jsonify(result), 200

    def addUser(self, json):
        uaemail = json['email']
        uausername = json['username']
        uapassword = json['password']
        firstname = json['first_name']
        lastname = json['lastname']
        dob = json['dob']
        isActive = True
        isCoach=False
        uaplatform=json['platform']

        dao = AccountDAO()
        id = dao.addUser(uaemail, uausername, uapassword, firstname, lastname, dob, isActive, isCoach,uaplatform)

        result = self.built_attr_dic(id,uaemail,uausername, uapassword, firstname, lastname, dob, isActive,isCoach,uaplatform)

        return jsonify(result), 201

    def UpdateUser(self, json, id):
        uaemail = json['email']
        uausername = json['username']
        uapassword = json['password']
        firstname = json['firstname']
        lastname = json['lastname']
        dob = json['dob']
        isActive = json['isActive']
        isCoach=json['isCoach']
        uaplatform=['platform']

        dao = AccountDAO()
        id = dao.updateUser(id, uaemail, uausername, uapassword, firstname, lastname, dob, isActive,isCoach,uaplatform)
        result = self.built_attr_dic(id, uaemail, uausername, uapassword, firstname, lastname, dob, isActive,isCoach,uaplatform)

        return jsonify(result), 200
