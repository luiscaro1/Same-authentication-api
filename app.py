from flask import Flask, render_template, request, jsonify, make_response
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

# verify if the example works

app = Flask(__name__)

#an example for basic authentication still needs work
app.config['SECRET_KEY']="\x05'\xb2W\xc0\xc8\xde\x95\x05\xa0\xc8\x05\x8b\x06\xb6\x8cTF\x02\xf0\x91V\xd96" 
#Routes
CORS(app,supports_credentials=True,origins=['https://same-client-ui.herokuapp.com'])

@app.route('/')
def index():
   return "Hello Buddies!!"

@app.route('/Same/accounts',methods=['GET','POST'])
def users():
    if request.method=="GET":
        return BaseAccounts().getAllUsers()
    else:
        return BaseAccounts().addUser(request.json)
# need to work on this, for some reasson the put is not working
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

    return jsonify('Username and password not valid, please try again'), 405   

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
    

if __name__=="main":
    app.run(debug=1,host='0.0.0.0')

