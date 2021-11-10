from flask import jsonify
from model.Friends import FriendDAO


class BaseFriend:

    def builtMapDict(self, row):
        result = {}
        result['uid'] = row
        #result['avatar_url'] = row[1]

        return result


    def built_attr_dict(self, fid, uid, uid2, isfriend):
        result = {}
        result['fid'] = fid
        result['uid'] = uid
        result['uid2'] = uid2
        result['isfriend'] = isfriend

        return result

    def addFriend(self, json):
        uid = json['uid']
        uid2 = json['uid2']
        isfriend = True
        dao = FriendDAO()
        if uid == uid2:
            return jsonify("Can't add yourself as a friend"), 500
        #check if previous friendship has been established between users
        pfe = dao.verifyFriendship(uid, uid2)
        if pfe == True:
            return "you are already friends"
        if pfe == False:
            dao.beFriendsAgain(uid, uid2)
            return "friend added successfully"
        
        fid = dao.addFriend(uid, uid2, isfriend)
        result = self.built_attr_dict(fid, uid, uid2, isfriend)
        return "friend added successfully"  

    def unfriend(self, json):
        uid = json['uid']
        uid2 = json['uid2']
        dao = FriendDAO()
        if uid == uid2:
            return jsonify("Can't unfried yourself"), 500
        
        result = dao.unfriend(uid, uid2)
        if not result:
            return jsonify("you and this user werent frind"), 500
        else:
            return "user was unfriended"

    def getAllfriends(self, json):
        uid = json['uid']
        dao = FriendDAO()
        result = dao.getAllFriends(uid)
        if result is None:
            return "user has no friends"
        else:
            res = []
            for i in range(len(result)):
                if not result[i][0] == uid:
                    res.append(self.builtMapDict(result[i][0]))
                res.append(self.builtMapDict(result[i][1]))
            return jsonify(res)