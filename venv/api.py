from flask import Flask #'Flask' is a class of 'flask' module
#'Flask' handles the api routes and logic
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is ORM
#Object Relational Mapper is used to interact with db using python
#objects instead of sql queries 

from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model): #This class defines a database table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable = False)
    email = db.Column(db.String(80), unique=True, nullable = False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'email' : fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name = args['name'], email = args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, 'User not found')
        return user


    @marshal_with(userFields)
    def patch(self, id): #Patch is used to update existing
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, 'User not found')
        user.name = args['name']
        user.email = args['email']
        db.session.commit()
        return user
    
    
    @marshal_with(userFields)
    def delete(self, id): 
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, 'User not found')
        db.session.delete(user)
        db.session.commit()
        user = UserModel.query.all()
        return user


api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)