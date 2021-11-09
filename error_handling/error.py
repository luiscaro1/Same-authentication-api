
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request, jsonify, make_response, abort
from flask.helpers import flash

# Attempt 1.2
class ErrorTest(HTTPException):
    code=405
    description="Method not allowed"

#Attempt2
class ErrorHandler(Exception):
    status_code=405
    def __init__(self,err,status_code=None):
        super().__init__()
        self.err=err
        if status_code is not None:
            self.status_code=status_code
    def to_dict(self):
        result=dict()
        result['error']=self.err
        return jsonify(result)

    def login_error(e):
        if request.path.startswith('/Same/login'):
            error=e
            return jsonify(error), 405
    def email_error(e):
        if request.path.startswith('Same/signup'):
            error=e
            return jsonify(error), 405
    def username_error(e):
        if request.path.startswith('Same/signup'):
            error=e
            return jsonify(error), 405
    def password_error(e):
        if request.path.startswith('Same/signup'):
            error=e
            return jsonify(error), 405
    
     
