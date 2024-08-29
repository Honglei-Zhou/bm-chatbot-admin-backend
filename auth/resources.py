from flask_restful import Resource, reqparse
from auth.models import User, RevokedTokenModel, BotAuth, IPModel
from flask_jwt_extended import \
    (create_access_token, create_refresh_token, jwt_required, get_jwt_claims,
     jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, verify_jwt_in_request_optional)
from flask import request, jsonify
import datetime
from .handler import get_all_users, get_user_detail, get_all_users_by_dealer_id, get_bot_by_dealer_id
from .utils import update_user, update_user_pageview, get_random_pwd, send_email


parser = reqparse.RequestParser()
parser.add_argument('email', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserObject:
    def __init__(self, email, roles, departments):
        self.email = email
        self.roles = roles
        self.departments = departments


class BotRegistration(Resource):
    @jwt_required
    def post(self):
        bot_id = request.form.get('botID')
        origin = request.form.get('origin')
        permission = request.form.get('permission')

        if BotAuth.find_by_username(bot_id):
            return {
                        'isError': False,
                        'message': 'Bot {} has already been registered.'.format(bot_id),
                        'statusCode': 200,
                        'data': {
                            'origin': origin,
                            'permission': permission
                        }
                    }, 200

        bot = BotAuth(
            bot_id=bot_id,
            origin=BotAuth.generate_hash(origin)
        )

        try:
            bot.save_to_db()
            return {
                        'isError': False,
                        'message': 'Bot {} was created'.format(bot_id),
                        'statusCode': 200,
                        'data': {
                            'origin': origin,
                            'permission': permission
                        }
                    }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class BotVerification(Resource):

    def post(self):
        bot_id = request.form.get('cId')

        origin = request.form.get('origin')
        print(bot_id)

        return get_bot_by_dealer_id(bot_id)
        # bot = BotAuth.find_by_bot_id(bot_id)

        # if bot and bot.permission != 'expired':
        #
        #     return {
        #                 'isError': False,
        #                 'message': 'Success',
        #                 'statusCode': 200,
        #                 'data': {'isAuthorized': True}
        #             }, 200
        # else:
        #     return {
        #                 'isError': False,
        #                 'message': 'Failed',
        #                 'statusCode': 200,
        #                 'isAuthorized': False,
        #                 'data': {'isAuthorized': False}
        #             }, 200

        # ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
        #
        # ip = IPModel(
        #     ip_addr=ip_addr,
        #     bot_id=bot_id
        # )
        # ip.save_to_db()
        #
        # bot = BotAuth.find_by_bot_id(bot_id)
        # if not bot:
        #     return jsonify(
        #         isError=False,
        #         message="Failed",
        #         statusCode=200,
        #         data={'isAuthorized': False}), 200
        #
        # if BotAuth.verify_hash(origin, bot.origin):
        #     access_token = create_access_token(identity=bot_id)
        #     refresh_token = create_refresh_token(identity=bot_id)
        #     return jsonify(
        #         isError=False,
        #         message="Failed",
        #         statusCode=200,
        #         access_token=access_token,
        #         refresh_token=refresh_token,
        #         data={'isAuthorized': False}), 200
        # else:
        #     return jsonify(
        #         isError=False,
        #         message="Failed",
        #         statusCode=200,
        #         data={'isAuthorized': False}), 200


class UserRegistrationV2(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']

        email = request.form.get('email', None)
        roles = request.form.get('role', 'user')
        departments = request.form.get('dept', 'sales')

        dealer_id = request.form.get('dealerId', '2019123456001')

        if User.find_by_email(email):
            return {
                'isError': True,
                'message': 'User {} already exists'.format(email),
                'statusCode': 200}, 200

        password = get_random_pwd()

        new_user = User(
            email=email,
            password=User.generate_hash(password),
            roles=roles,
            departments=departments,
            dealer_id=dealer_id,
            created=datetime.datetime.utcnow()
        )

        try:
            new_user.save_to_db()

            body = 'Your account has been created.\n Email: {}\n Password: {}\n'.format(email, password)

            send_email([email], 'New Account Created', body=body)

            return {
                       'isError': False,
                       'message': 'User {} has been created.'.format(email),
                       'statusCode': 200,
                   }, 200
        except Exception as e:
            return {'message': 'Internal Error. Please retry.'}, 500


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        roles = request.form.get('roles', 'user')
        departments = request.form.get('departments', 'sales')

        if User.find_by_email(data['email']):
            return {'message': 'User {} already exists'.format(data['email'])}

        new_user = User(
            email=data['email'],
            password=User.generate_hash(data['password']),
            roles=roles,
            departments=departments,
            created=datetime.datetime.utcnow()
        )

        try:
            new_user.save_to_db()

            user = UserObject(email=data['email'], roles=roles, departments=departments)
            access_token = create_access_token(identity=user)
            # refresh_token = create_refresh_token(identity=user)
            return {
                        'isError': False,
                        'message': 'Logged in as {}'.format(data['email']),
                        'statusCode': 200,
                        'data': {
                            'access_token': access_token,
                            'role': roles,
                            'department': departments
                            # 'refresh_token': refresh_token
                        }
                    }, 200
        except Exception as e:
            print(e)

            print(new_user)
            return {'message': 'Internal Error. Please retry.'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_email(data['email'])
        print(data)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}

        if User.verify_hash(data['password'], current_user.password):
            user = UserObject(email=data['email'], roles=current_user.roles, departments=current_user.departments)
            expires = datetime.timedelta(hours=8)
            access_token = create_access_token(identity=user, expires_delta=expires)
            # refresh_token = create_refresh_token(identity=user)
            resp = {
                        'isError': False,
                        'message': 'Logged in as {}'.format(current_user.email),
                        'statusCode': 200,
                        'data': {
                            'token': access_token,
                            'role': current_user.roles,
                            'department': current_user.departments,
                            'dealerId': current_user.dealer_id
                            # 'refresh_token': refresh_token
                        }
                    }, 200
            print(resp)
            return resp
        else:
            resp = {
                        'isError': True,
                        'message': 'Wrong Credential',
                        'statusCode': 200,
                        'data': None
                    }, 200
            print(resp)
            return resp


class UserLogoutAccess(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                        'isError': False,
                        'message': 'Access token has been revoked',
                        'statusCode': 202,
                        'data': None
                    }, 202
        except:
            return {'message': 'Internal Error. Please retry.'}, 500

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                       'isError': False,
                       'message': 'Access token has been revoked',
                       'statusCode': 202,
                       'data': None
                   }, 202
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                        'isError': False,
                        'message': 'Refresh token has been revoked',
                        'statusCode': 200,
                        'data': None
                    }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        email = get_jwt_identity()
        try:
            current_user = User.find_by_email(email)
            user = UserObject(email=email, roles=current_user.roles, departments=current_user.departments)
            access_token = create_access_token(identity=user)
            return {
                            'isError': False,
                            'message': 'Logged in as {}'.format(current_user.email),
                            'statusCode': 200,
                            'data': {
                                'access_token': access_token
                            }
                    }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

        current_user = User.find_by_email(data['email'])

        new_password = request.form.get('new_password')

        if not current_user:
            return {
                'isError': True,
                'message': 'User {} doesn\'t exist'.format(data['email'])}

        if User.verify_hash(data['password'], current_user.password):

            jti = get_raw_jwt()['jti']
            try:
                current_user.password = User.generate_hash(new_password)
                current_user.save_to_db()
                return {
                           'isError': False,
                           'message': 'Password has been changed.',
                           'statusCode': 202,
                           'data': None
                       }, 202
            except:
                return {'isError': True,
                        'message': 'Internal Error. Please retry.'}, 500
        else:
            return {'message': 'Old Password doesn\'t match'}, 200


class AllUsers(Resource):
    @jwt_required
    def get(self):
        dealer_id = request.args.get('dealerId')
        roles = get_jwt_claims()['roles']
        print(dealer_id)
        if dealer_id and dealer_id == '2019123456001':
            if 'admin' in roles:
                return get_all_users()
            else:
                return {
                            'isError': True,
                            'message': 'Permission denied.',
                            'statusCode': 200,
                            'data': None
                        }, 200
        elif dealer_id:
            if 'admin' in roles:
                return get_all_users_by_dealer_id(dealer_id)
            else:
                return {
                            'isError': True,
                            'message': 'Permission denied.',
                            'statusCode': 200,
                            'data': None
                        }, 200
        else:
            return {
                       'isError': True,
                       'message': 'Permission denied.',
                       'statusCode': 200,
                       'data': None
                   }, 200


class SingleUser(Resource):
    @jwt_required
    def post(self):
        roles = get_jwt_claims()['roles']
        current_user_email = get_jwt_identity()
        email = request.form.get('email', None)
        dealer_id = request.form.get('dealerId')
        print(dealer_id)
        if dealer_id and ('admin' in roles or current_user_email == email):
            ret = get_user_detail(email, dealer_id)
            print(ret)
            return ret
        else:
            return {
                        'isError': True,
                        'message': 'Permission denied.',
                        'statusCode': 200,
                        'data': None
                    }, 200


class DeleteUser(Resource):
    @jwt_required
    def get(self):
        user = request.args.get('email', None)
        roles = get_jwt_claims()['roles']
        if 'admin' in roles:
            result = User.delete(user)
            return {
                        'isError': False,
                        'message': 'user: {} has been deleted'.format(user),
                        'statusCode': 200,
                        'data': result
                    }, 200
        else:
            return {
                        'isError': True,
                        'message': 'Permission denied.',
                        'statusCode': 200,
                        'data': None
                    }, 200


class UpdateUser(Resource):
    @jwt_required
    def post(self):
        user_email = request.form.get('email', None)
        user_role = request.form.get('role', 'user')
        user_department = request.form.get('dept', 'sales')
        current_user = User.find_by_email(user_email)

        if not current_user:
            return {
                'isError': True,
                'message': 'User {} doesn\'t exist'.format(user_email),
                'statusCode': 200
            }, 200

        roles = get_jwt_claims()['roles']
        if 'admin' in roles:
            try:
                current_user.roles = user_role
                current_user.departments = user_department
                current_user.save_to_db()
                return {
                            'isError': False,
                            'message': 'user: {} has been updated'.format(user_email),
                            'statusCode': 200,
                        }, 200
            except:
                return {'message': 'Internal Error. Please retry.'}, 500
        else:
            return {
                        'isError': True,
                        'message': 'Permission denied.',
                        'statusCode': 200,
                        'data': None
                    }, 200


class UpdateProfile(Resource):
    @jwt_required
    def post(self):
        user_email = request.form.get('email', None)
        first_name = request.form.get('firstName', None)
        last_name = request.form.get('lastName', None)
        current_user = User.find_by_email(user_email)

        if not current_user:
            return {
                       'isError': True,
                       'message': 'User {} doesn\'t exist'.format(user_email),
                       'statusCode': 200
                   }, 200

        else:
            try:
                if first_name:
                    current_user.first_name = first_name
                if last_name:
                    current_user.last_name = last_name
                current_user.save_to_db()
                return {
                           'isError': False,
                           'message': 'user: {} has been updated'.format(user_email),
                           'statusCode': 200,
                       }, 200
            except:
                return {'message': 'Internal Error. Please retry.'}, 500


class Test(Resource):
    @jwt_required
    def get(self):
        roles = get_jwt_claims()['roles']
        print(roles)
        return {'message': 'Test roles: {}'.format(roles)}, 200


class GetUserIP(Resource):

    def get(self):
        device_type = request.args.get('deviceType', 'Desktop')
        device_detail = request.args.get('deviceDetail', 'Desktop')
        session_id = request.args.get('sessionId', '')

        dealer_id = request.args.get('dealerId', '2019123456001')
        dealer_name = request.args.get('dealerName', 'dthonda')

        ip_addr = request.remote_addr

        message = {
            'deviceType': device_type,
            'deviceDetail': device_detail,
            'sessionId': session_id,
            'dealerId': dealer_id,
            'dealerName': dealer_name,
            'ip_addr': ip_addr
        }

        return update_user(message)


class UpdateUserPageView(Resource):

    def post(self):
        ip_addr = request.remote_addr
        session_id = request.form.get('sessionId')
        page = request.form.get('page')
        dealer_id = request.form.get('dealerId', '2019123456001')
        bot_clicked = request.form.get('botClicked', '0')

        message = {
            'sessionId': session_id,
            'dealerId': dealer_id,
            'ip_addr': ip_addr,
            'page': page,
            'bot_clicked': int(bot_clicked)
        }

        if session_id is None or len(session_id) < 3 or page is None or len(page) < 5:
            return {
                    'isError': True,
                    'message': 'Empty message',
                    'statusCode': 200,
                    }, 200

        return update_user_pageview(message)
