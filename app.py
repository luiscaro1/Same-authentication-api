from flask import Flask, render_template, request, jsonify, make_response, abort
from flask.helpers import flash
from flask_cors import CORS,cross_origin
from controller.accounts import BaseAccounts
from model.Account import AccountDAO
import jwt
import datetime
from functools import wraps
from config.db_config import pg_config
import psycopg2
import hashlib
import json
import uuid
import os


app = Flask(__name__)

#an example for basic authentication still needs work
app.config['SECRET_KEY']="\x05'\xb2W\xc0\xc8\xde\x95\x05\xa0\xc8\x05\x8b\x06\xb6\x8cTF\x02\xf0\x91V\xd96" 
#Routes
CORS(app,supports_credentials=True,origins=['https://same-client-ui.herokuapp.com','http://localhost:3000'])

@app.route('/')
def index():
   return "Hello Buddies!!"

#Custom error handlers
@app.errorhandler(405)
def no_valid_user(err):
    app.logger.exception(err)
    return "Username and password not valid, please try again",405
#need to avoid overriding , some switch case of something
@app.errorhandler(ValueError)
def email_already_taken(err):
    app.logger.exception(err)
    return "Email is already taken, please try a different one",405

def username_taken(err):
    app.logger.exception(err)
    return "Username is already taken, please try a different one",405

def password_error(err):
    app.logger.exception(err)
    return "Password must contain atleast 8 characters, one uppercase letter, one lowercase letter, one number, and one special character",405

#To get users or create them
@app.route('/Same/accounts',methods=['GET','POST'])
def users():
    if request.method=="GET":
        return BaseAccounts().getAllUsers()
    else:
        if  request.method=='POST':
            res=BaseAccounts().addUser(request.json)
            if res=="this email is already taken":
                return email_already_taken("error")
            elif res=="username is already taken, please try a different one":
                return username_taken("error")
            elif res=="password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character":
                return password_error("error")
            return res

#getting a user
@app.route('/Same/accounts/<uid>',methods=['GET', 'PUT', 'DELETE'])
def getSpecificUser(uid):
    if request.method == "GET":
        return BaseAccounts().getUser(uid)
    elif request.method == "PUT":
        return BaseAccounts().UpdateUser(request.json, uid)
    elif request.method == "DELETE":
        return BaseAccounts().deleteUser(uid)
    else:
        return jsonify('Method not allowed'), 405


# account login route
@app.route('/Same/login', methods=["POST"])
def login():
    if request.method=="POST":
        res = BaseAccounts().Log_in(request.json)
        if res:
            uid = res.get('uid')
            user_name = res.get('user_name')
            print(user_name)
            expire = 259200 
            # datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'user': uid}, app.config['SECRET_KEY'])
            cookie = make_response(res)
            cookie.set_cookie('access_token',token)

            return cookie

    return no_valid_user("error")
        
    # return abort(405, description="Username and password not valid, please try again")
    # return default_error("Username invalid")
 
#will be changed
@app.route('/Same/accounts/logout/<uid>',methods=["POST"])
def logout(uid):
    token=request.cookies.get('access_token')
    decode_token=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
    print(decode_token)
    if uid==decode_token.get('user'): 
        actual_time = datetime.datetime.utcnow()
        if  not decode_token.get("exp") == actual_time:
            decode_token.update({"exp":actual_time})
            cookie= make_response("cookie has expired")
            cookie.set_cookie('access_token','',expires=actual_time)

            return cookie
        
    return " "


@app.route('/Same/accounts/getCookieOwner',methods=["GET"])
def getCookie():
    cookie = request.cookies.get('access_token')

    if(cookie is None):
        return '',403

    decode_token = jwt.decode(cookie,app.config['SECRET_KEY'],algorithms=["HS256"])
    user = decode_token.get('user')

    account= BaseAccounts().getCookieOwner(user)

    if(account):
        return account
    else:
        return jsonify("ok"), 200
    

if __name__=="__main__":
    port=os.environ.get("PORT",5000)
    app.run(debug=False,host='0.0.0.0', port=port)

