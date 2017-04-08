from models.user import UserModel


def authenticate(username, password):
    user = UserModel.get_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.get_by_userid(user_id)


# first authenticate by username and password, then the server return a JSON Werb Token,
# use this JWT, the client's request will be sererved as it's already logged in
