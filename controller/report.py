from flask import jsonify
from model.Report import ReportDAO


class BaseReport:

    def builtMapDict(self, row):
        result = {}
        result['rid']=row[0]
        result['uid'] =row[1]
        result['uid2']=row[2]
        result['stalking']=row[3]
        result['spamming']=row[4]
        result['offensive']=row[5]
        result['harrasment']=row[6]
        result['discrimination']=row[7]
        result['viruses']=row[8]
        result['violationofIp']=row[9]
        result['pretending']=row[10]

        return result


    def built_attr_dict(self, rid, uid, uid2,stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending):
        result = {}
        result['rid'] = rid
        result['uid'] = uid
        result['uid2'] = uid2
        result['stalking'] = stalking
        result['spamming']=spamming
        result['offensive']=offensive
        result['harrasment']=harrasment
        result['discrimination']=discrimination
        result['viruses']=viruses
        result['violationofIp']=violationofIp
        result['pretending']=pretending


        return result
#reporting based on all conditions
    def reportUser(self, json):
        uid = json['uid']
        uid2 = json['uid2']
        stalking=True
        spamming=True
        offensive=True
        harrasment=True
        discrimination=True
        viruses=True
        violationofIp=True
        pretending=True

        dao = ReportDAO()
        #checks if the users were friends, if they were this will unfriend them
        if uid == uid2:
            return jsonify("Can't report yourself"), 500
        #check if users has already blocked the other beforehand
        
        rid = dao.reportUser(uid, uid2,stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending)
        result = self.built_attr_dict(rid, uid, uid2,stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending)
        
        return "user reported successfully" 

#reporting based on specific conditions , temporary
    def reportUserSpecific(self, json):
        uid = json['uid']
        uid2 = json['uid2']
        stalking=json['stalking']
        spamming=json['spamming']
        offensive=json['offensive']
        harrasment=json['harrasment']
        discrimination=json['discrimination']
        viruses=json['viruses']
        violationofIp=json['violationofIp']
        pretending=json['pretending']

        dao = ReportDAO()
        #checks if the users were friends, if they were this will unfriend them
        if uid == uid2:
            return jsonify("Can't report yourself"), 500
        #check if users has already blocked the other beforehand
        
        rid = dao.reportUser(uid, uid2,stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending)
        result = self.built_attr_dict(rid, uid, uid2,stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending)
        
        return "user reported successfully"  
#Admin only
    def getallReported(self):
        dao = ReportDAO()
        reportlist = dao.getallReports()
        result=[]
        for row in reportlist:
            obj=self.builtMapDict(row)
            result.append(obj)
        return jsonify(result)