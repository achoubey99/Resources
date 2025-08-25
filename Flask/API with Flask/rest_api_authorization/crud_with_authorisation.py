from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from security_check import authenticate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['JWT_SECRET_KEY'] = 'my_jwt_secret_key'  # used by flask_jwt_extended

api = Api(app)
jwt = JWTManager(app)

puppies = []    # format inside the list {'name' : 'actual_puppy_name'}

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
        for pup in puppies:
            if pup['name'] == name:
                return pup
        return {'name': None}
    
    def post(self, name):
        pup = {'name' : name}
        puppies.append(pup)
        return {'name' : name}

    def delete(self, name):
        for pup in puppies:
            if pup['name'] == name:
                puppies.remove(pup)
                return {'note' : 'delete_successful'}
        return f'puppy "{name}" not found'

class AllNames(Resource):

    @jwt_required()           # this decorator will help in applying authentication    
    def get(self):
        return {'puppies' : puppies}
    
api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')

if __name__ == '__main__':
    app.run(debug=True)
