from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.userauth import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity
from http import HTTPStatus


user_namespace = Namespace('userauth', description='user auth namespace')

signup_model = user_namespace.model('SIGNUPUSER', {
    'id': fields.Integer(),
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password'),
    'fullname': fields.String(required=False, description='user full name'),
})

login_model = user_namespace.model('LOGINUSER', {
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password'),
})

#endpoints
@user_namespace.route('/signup')
class SIGNUP(Resource):
    @user_namespace.expect(signup_model)
    @user_namespace.marshal_with(signup_model)
    def post(self):
        '''
            User signup
        '''
        data = request.get_json()
        email = data['email']
        password = data['password']
        fullname = data.get('fullname', None)

        user_exist = User.query.filter_by(email=email).first()
        if (user_exist is not None) and user_exist.password is not None:
            response = {
                'message': 'user already exist'
            }

            return response, HTTPStatus.UNAUTHORIZED
        else:
            new_user = User(email=email, password=generate_password_hash(password), fullname=fullname)
            new_user.save()

            return new_user, HTTPStatus.CREATED


@user_namespace.route('/login')
class LOGIN(Resource):
    @user_namespace.expect(login_model)
    def post(self):
        '''
            Login user
        '''

        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password, password):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.OK
        else:
            response = {
                "message": 'Invalid credentials submitted'
            }
            return response, HTTPStatus.UNAUTHORIZED

@user_namespace.route('/refresh')
class REFRESHTOKEN(Resource):
    @jwt_required(refresh=True)
    def get(self):
        '''
            Refresh user token
        '''
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        refresh_token = create_refresh_token(identity=current_user)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response, HTTPStatus.OK

@user_namespace.route('/me')
class GETUSER(Resource):
    @jwt_required()
    def get(self):
        '''
            Get user information
        '''
        current_user = get_jwt_identity()
        user_check = User.query.filter_by(email=current_user).first()

        if not user_check:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        response = {
            'email': user_check.email,
            'fullname': user_check.fullname,
        }

        return response, HTTPStatus.OK

