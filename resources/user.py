from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field username connot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field pw cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        # check the db to see if the username already exist
        if UserModel.get_by_username(data['username']):
            return {'msg': 'user already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'msg': "User created successfullly"}, 201
