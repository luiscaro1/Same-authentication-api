from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS,cross_origin
from controller.accounts import BaseAccounts
import jwt #needs to install the dependency, for some reason no me deja en mi laptop
import datetime
from functools import wraps

# verify if the example works

app = Flask(__name__)

#an example for basic authentication still needs work
app.config['SECRET_KEY']='thisisourauthkey' #temporary needs to be better

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

# Authentication routes basic examples
@app.route('/unprotected')
def unprotected():
    return jsonify({'message':'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only for people with valid tokens.'})

@app.route('/login')
def login():
    auth=request.authorization
    if auth and auth.username=='username' and auth.password=='password':
        token=jwt.encode({'user': auth.username,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})

    return make_response('Could not verify user!',401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__=="main":
    app.run(debug=1)

