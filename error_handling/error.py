from flask import Flask, render_template, request, jsonify, make_response, abort
from flask.helpers import flash

#Customer error handling class specifically for Method not Allowed 405
class ErrorHandler(Exception):
    status_code=405
    def __init__(self,message,status_code=None):
        super().__init__()
        self.message=message
        if status_code is not None:
            self.status_code=status_code
    def to_dict(self):
        result=dict()
        result['message']=self.message
        return result

