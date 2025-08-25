from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

puppies = []    # format inside the list {'name' : 'actual_puppy_name'}

class PuppyNames(Resource):

    def get(self, name):            # all methods get, post, delete should have the same parameters        
        for pup in puppies:
            if pup['name'] == name:
                return pup
        return pup['name' : None]
    
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
    
    def get(self):
        return {'puppies' : puppies}
    
api.add_resource(PuppyNames,'/puppy/<string:name>')
api.add_resource(AllNames,'/puppies')

if __name__ == '__main__':
    app.run(debug = True)