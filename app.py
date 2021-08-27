from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
from controller.accounts import BaseAccounts

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():

   return "Hello Buddies!!"

@app.route('/test2/accounts',methods=['GET'])
def users():
    if request.method=="GET":
        return BaseAccounts().getAllUsers()

if __name__=="main":
    app.run(debug=1)

