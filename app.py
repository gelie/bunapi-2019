from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bungeni:bungeni@localhost:3032/bungeni'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import User


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("login", "email", "title", 'first_name', 'last_name', '_links')
        ordered = True

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            '_self': ma.URLFor("user_detail", user_id="<user_id>", _external=True),
            '_collection': ma.URLFor("users", _external=True)
        }
    )


user_schema = UserSchema()

users_schema = UserSchema(many=True, only=('login', 'email', '_links'))


class UserList(Resource):
    def get(self):
        users = User.query.limit(10)
        return users_schema.jsonify(users)


class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.jsonify(user)


api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(UserDetail, '/users/<int:user_id>', endpoint='user_detail')

if __name__ == '__main__':
    app.run()
