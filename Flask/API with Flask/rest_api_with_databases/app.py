from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from security_check import authenticate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from models import Puppy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['JWT_SECRET_KEY'] = 'my_jwt_secret_key'  # used by flask_jwt_extended
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


api = Api(app)
jwt = JWTManager(app)


# Login endpoint to get JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username, password)
    if not user:
        return jsonify({'msg': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

class PuppyNames(Resource):

    def get(self, name):            # all methods get, post, delete should have the same parameters        
        pup = Puppy.query.filter_by(name = name).first()
        if pup:
            return pup.json()
        else:
            return {'name' : None}, 404 
    
    def post(self, name):
        pup = Puppy(name = name)
        db.session.add(pup)
        db.session.commit()

        return pup.json
    

    def delete(self, name):
        pup = Puppy.query.filter_by(name = name).first()
        if pup:
            db.session.delete(pup)
            db.session.commit()
            return {'note' : 'delete_successful'}
        return f'puppy "{name}" not found'

class AllNames(Resource):

    @jwt_required()           # this decorator will help in applying authentication    
    def get(self):
        puppies = Puppy.query.all()

        return [pup.json() for pup in puppies]
    
api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')

if __name__ == '__main__':
    app.run(debug=True)
