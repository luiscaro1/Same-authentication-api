from logging import error
from flask import Flask, render_template, request, jsonify, make_response,abort,flash
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException
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
from error_handling.error import ErrorHandler

# from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import MethodNotAllowed, NotFound,abort

# verify if the example works

app = Flask(__name__)

#an example for basic authentication still needs work
app.config['SECRET_KEY']="\x05'\xb2W\xc0\xc8\xde\x95\x05\xa0\xc8\x05\x8b\x06\xb6\x8cTF\x02\xf0\x91V\xd96" 
#Routes
CORS(app,supports_credentials=True,origins=['https://same-client-ui.herokuapp.com','http://localhost:3000'])

@app.route('/')
def index():
   return "Hello Buddies!!"

#Attempt 3
# @app.errorhandler(405)
# def not_allowed(err):
#     app.logger.exception(err)
#     return jsonify(error=str(err)), 405  

#Attempt 1.2
# @app.errorhandler(ErrorTest)
# def handle_custom_exception(err):
#     result={"error":err.description}
#     if len(err.args)>0:
#         result["message"]=err.args[0]
#     app.logger.error(f'{err.description}')
#     return jsonify(result),405

# @app.errorhandler(500)
# def handle_exception(err):
#     app.logger.error(f"Unknown Exception oops: {str(err)}")
#     return jsonify("oops"),500

#Attempt failed
# @app.errorhandler(ErrorHandler)
# def error(e):
#     app.logger.exception(e)
#     return e.to_dict().get('message'),405

#Attempt4
# @app.errorhandler(405)
# def method_not_allowed(e):
#     if request.path.startswith('/Same/login'):
#         e="Username and password not valid"
#         return jsonify(error=e), 405
    
#Attempt 5
# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     response.name=e.name
#     # replace the body with JSON
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
    
#     return response
#Failed
# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     response.data=json.dumps({"error":str(e)})
#     response.content_type = "application/json"
    
#     return response

# @app.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e
#Attempt 6

# @app.errorhandler(405)
# def default_error_handler(error):
#     '''Default error handler'''
#     return {'message': str(error)}, getattr(error, 'code', 405)

#Attempt 8
@app.errorhandler(405)
def not_allowed(err):
    app.logger.error(err)
    return jsonify(error="Username and password are not valid, please try again"),405 

# @app.errorhandler(ErrorHandler)
# def login_error(err):
#     app.logger.exception(err)
#     return jsonify(error=str(err)),405

# @app.errorhandler(ErrorTest)
# def not_allowed(err):
#     app.logger.error(err)
#     return jsonify(error=str(err)),405  
#Attempt 9
# @app.errorhandler(ErrorHandler)
# def error(e):
#      app.logger.exception(e)
#      return e

@app.route('/Same/accounts',methods=['GET','POST'])
def users():
    if request.method=="GET":
        return BaseAccounts().getAllUsers()
    
@app.route('/Same/signup',methods=['POST'])
def signup():
     if request.method=='POST':
        res=BaseAccounts().addUser(request.json)
        if res=="this email is already taken":
            return ErrorHandler.email_error("Email is already taken, please try a different one")
        elif res=="username is already taken, please try a different one":
            return ErrorHandler.username_error("Username is already taken, please try a different one")
        elif res=="password must contain atleast 8 characters, atleast one uppercase letter, atleast one lowercase letter, atleast one number, and atleast one special character":
            return ErrorHandler.password_error("Password must contain atleast 8 characters, one uppercase letter, one lowercase letter, one number, and one special character")
        else:
            return res

# need to work on this, for some reason the put is not working
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
    # try:
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
    # except HTTPException as e:
    #return ErrorHandler.login_error("Username and password not valid, please try again")
    #abort(405,description="Test") 
        #abort(Response('Username and password not valid, please try again'),405)

    #raise ErrorTest("Username and password are not valid, please try again")
    return not_allowed("Username and password are not valid, please try again")
    #return method_not_allowed("Username and password not valid, please try again")
    #raise ErrorHandler("Username and password not valid, please try again",status_code=405)
    #return handle_exception(error="Username and password are not valid, please try again"),405
  #return default_error_handler("Username and password not valid, please try again")

    #Attempt 7
    #return MethodNotAllowed(valid_methods=None,description="Method not allowed",response="Username and password not valid, please try again")
    #raise ErrorTest(description="Username and password not valid, please try again")
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

