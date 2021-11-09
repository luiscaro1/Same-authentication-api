from flask import jsonify
from model.Block import BlockedDAO
from model.Friends import FriendDAO


class BaseBlocked:

    def builtMapDict(self, row):
        result = {}
        result['uid'] = row
        #result['avatar_url'] = row[1]

        return result


    def built_attr_dict(self, bid, uid, uid2, isblocked):
        result = {}
        result['bid'] = bid
        result['uid'] = uid
        result['uid2'] = uid2
        result['isblocked'] = isblocked

        return result

    def blockUser(self, json):
        uid = json['uid']
        uid2 = json['uid2']
        isblocked = True
        dao = BlockedDAO()
        #checks if the users were friends, if they were this will unfriend them
        FriendDAO().unfriend(uid, uid2)
        if uid == uid2:
            return jsonify("Can't block yourself"), 500
        #check if users has already blocked the other beforehand
        pfe = dao.verifyIfBlocked(uid, uid2)
        if pfe == True:
            return "the user is already blocked"
        if pfe == False:
            dao.blockAgain(uid, uid2)
            return "user blocked successfully"
        
        bid = dao.blockUser(uid, uid2, isblocked)
        result = self.built_attr_dict(bid, uid, uid2, isblocked)
        
        return "user blocked successfully"  

    def unblockUser(self, json):
        uid = json['uid']
        uid2 = json['uid2']
        dao = BlockedDAO()
        if uid == uid2:
            return jsonify("Can't unblock yourself"), 500
        
        result = dao.unblock(uid, uid2)
        if not result:
            return jsonify("this user is not blocked"), 500
        else:
            return "user was unblocked"

    def getallBlocked(self, json):
        uid = json['uid']
        dao = BlockedDAO()
        result = dao.getallBlocked(uid)
        if len(result) == 0:
            return "user has blocked no one"
        else:
            res = []
            for row in result:
                res.append(self.builtMapDict(row))
            return jsonify(res)
    
    def getallBlockedBy(self, json):
        uid2 = json['uid2']
        dao = BlockedDAO()
        result = dao.getallBlockedBy(uid2)
        if len(result) == 0:
            return "user is blocked by no one"
        else:
            res = []
            for row in result:
                res.append(self.builtMapDict(row))
            return jsonify(res)