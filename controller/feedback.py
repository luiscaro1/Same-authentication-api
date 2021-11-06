from flask import jsonify, request
from model.Feedback import FeedbackDAO
from model.Account import AccountDAO
from werkzeug.security import DEFAULT_PBKDF2_ITERATIONS, generate_password_hash, check_password_hash

class BaseFeedback:
    

    def builtmapdict(self,row):

        result={}
        result['fid']=row[0]
        result['email']=row[1]
        result['websitedesign']=row[2]
        result['ratedesign']=row[3]
        result['websitefunctionality']=row[4]
        result['ratefuntionality']=row[5]
        result['gameavailable']=row[6]
        result['rategames'] = row[7]
        result['generalinformation']=row[8]
        result['rateoverall'] = row[9]

        return result

    def build_avg_dic(self, des, func, game, overall):
        result={}
        result['avg_rate_of_design']=des
        result['avg_rate_of_functionality']=func
        result['avg_rate_of_games']=game
        result['avg_rate_of_overall']=overall
        
        return result

    def built_attr_dic(self,fid,email,websitedesign, ratedesign, websitefunctionality, ratefunctionality, gameavailable, rategames, generalinformation, rateoverall):
        result={}
        result['fid'] = fid
        result['email'] = email
        result['websitedesign'] = websitedesign
        result['ratedesign'] = ratedesign
        result['websitefunctionality'] = websitefunctionality
        result['ratefuntionality'] = ratefunctionality
        result['gameavailable'] = gameavailable
        result['rategames'] = rategames
        result['generalinformation'] = generalinformation
        result['rateoverall'] = rateoverall
        
        return result


    #getting all the user accounts from the data base
    def getAllFeedback(self):
        dao=FeedbackDAO()
        feedbacklist=dao.getAllFeedback()
        result=[]
        for row in feedbacklist:
            obj=self.builtmapdict(row)
            result.append(obj)
        return jsonify(result)


    # create a new user account and then it is added to the databasae
    def addFeedback(self, json):
    
        email = json["email"]
        websitedesign = json['websitedesign']
        ratedesign = json["ratedesign"]
        websitefunctionality = json["websitefunctionality"]
        ratefunctionality = json["ratefunctionality"]
        gameavailable = json["gameavailable"]
        rategames = json["rategames"]
        generalinformation = json["generalinformation"]
        rateoverall = json["rateoverall"]
        
        dao = FeedbackDAO()
        adao = AccountDAO()
        ve = adao.emailExist(email)
        if ve:
            fid = dao.addFeedback(email,websitedesign, ratedesign, websitefunctionality, ratefunctionality, gameavailable, rategames, generalinformation, rateoverall)
            result = self.built_attr_dic(fid,email,websitedesign, ratedesign, websitefunctionality, ratefunctionality, gameavailable, rategames, generalinformation, rateoverall)
            return jsonify(result), 201
        else:
            return "this email is not registered"
                
                    
    def avgRatesFeedback(self):
        dao=FeedbackDAO()
        avgfeedbacklist=dao.getAvgRates()
        des = str(avgfeedbacklist[0]*10)+"%"
        func = str(avgfeedbacklist[1]*10)+"%"
        game = str(avgfeedbacklist[2]*10)+"%"
        overall = str(avgfeedbacklist[3]*10)+"%"
        result = self.build_avg_dic(des, func, game, overall)
        
        return result

    


