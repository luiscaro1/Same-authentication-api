from flask import jsonify
from model.Account import AccountDAO

class BaseAccounts:
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
        result['id']=row[0]
        result['email']=row[1]
        return result
