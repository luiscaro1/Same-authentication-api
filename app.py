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

# verify if the example works

app = Flask(__name__)

#an example for basic authentication still needs work
app.config['SECRET_KEY']="\x05'\xb2W\xc0\xc8\xde\x95\x05\xa0\xc8\x05\x8b\x06\xb6\x8cTF\x02\xf0\x91V\xd96" 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=request.args.get('token') #http://127.0.0.1:5000/route?token=alshffbsjj
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is invalid'}), 403

        return f(*args,**kwargs)
    return decorated
#Routes
CORS(app)
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
@app.route('/Same/accounts/<int:uaid>',methods=['GET', 'PUT', 'DELETE'])
def getSpecificUser(uaid):
    if request.method == "GET":
        return BaseAccounts().getUser(uaid)
    elif request.method == "PUT":
        return BaseAccounts().UpdateUser(request.json, uaid)
    elif request.method == "DELETE":
        return BaseAccounts().deleteUser(uaid)
    else:
        return jsonify('Method not allowed'), 405

# account login route
cross_origin()
@app.route('/Same/login', methods=["POST"])
def login():
    if request.method=="POST":
        res = BaseAccounts().Log_in(request.json)
        uaid = res[0]
        username = res[1]
        if res:
            token = jwt.encode({'user': username,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            cookie = make_response(uaid)
            cookie.set_cookie('access_token',token)
            cookie.set_cookie('uaid',uaid)

            return cookie

    return jsonify('Username and password not valid, please try again'), 405   

#will be changed   
@app.route('/Same/accounts/<int:uaid>/logout',methods=["POST"])
def logout(uaid):
    if request.method=="POST":
        res=BaseAccounts().add_token(request.json,uaid)
    return res


@app.route('/Same/accounts/getCookieOwner',methods=["GET"])
def getCookie():
    return BaseAccounts().getCookie()
    

if __name__=="main":
    app.run(debug=1)

