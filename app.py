import logging
from flask_cors import CORS
from server.server import app
from flask_restful import Api
from bot_page.resources import (CarList, UsedCarList, NewCarList, CarDetail, LineChart, PieChart, BarChart, TodoCreate,
                                TodoList, TodoUpdate, TodoSave, LineChartAdv, UserLocation, PromotionList, PromotionCreate,
                                PromotionDelete, PromotionUpdate, BotConfigurationCreate, BotConfigurationUpdate,
                                BotConfigurationPublish, BotConfigurationDelete, BotConfigurationDetail)
from auth.models import RevokedTokenModel
from flask_jwt_extended import JWTManager
import views
from auth.resources import (BotRegistration, BotVerification, UserRegistration, UpdateUser, UserRegistrationV2,
                            UserLogin, UserLogoutAccess, UserLogoutRefresh, TokenRefresh, AllUsers, ChangePassword,
                            SingleUser, DeleteUser, Test, GetUserIP, UpdateUserPageView)
from chatbot.resources import (MessageDetail, MessageList, ChatDetail, ChatList, LiveChatList, LiveChatUpdate,
                               LeadDetail, LeadListV2, LeadCreate, LiveMessageList, ChatUpdate)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# CORS(app)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

api = Api(app)

jwt = JWTManager(app)


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'roles': user.roles, 'departments': user.departments}


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    print(jti)
    return RevokedTokenModel.is_jti_blacklisted(jti)


api.add_resource(CarList, '/cars/')
api.add_resource(CarDetail, '/cars/<vin>')
api.add_resource(NewCarList, '/cars/new/')
api.add_resource(UsedCarList, '/cars/used/')

# bot auth api
api.add_resource(BotRegistration, '/bots/registration')
api.add_resource(BotVerification, '/bots/authentication')

# user auth api
api.add_resource(UserRegistration, '/api/user/registration')
api.add_resource(UserLogin, '/api/user/login')
api.add_resource(UserLogoutAccess, '/api/user/logout')
api.add_resource(UserLogoutRefresh, '/api/user/logout_refresh')
api.add_resource(TokenRefresh, '/api/user/refresh')
api.add_resource(AllUsers, '/api/user/all/')
api.add_resource(SingleUser, '/api/user/info')
api.add_resource(DeleteUser, '/api/user/delete/')
api.add_resource(UpdateUser, '/api/user/update/')
api.add_resource(UserRegistrationV2, '/api/user/add/')
api.add_resource(Test, '/api/user/test/')
api.add_resource(GetUserIP, '/api/user/ip')
api.add_resource(UpdateUserPageView, '/api/user/pageview')
api.add_resource(ChangePassword, '/api/user/password')


# chat history api
api.add_resource(MessageDetail, '/api/messages/<id>')
api.add_resource(MessageList, '/api/messages')
api.add_resource(ChatDetail, '/api/chats/<session_id>')
api.add_resource(ChatList, '/api/chats')
api.add_resource(LeadDetail, '/api/leads/detail')
api.add_resource(LeadListV2, '/api/leads')
api.add_resource(LeadCreate, '/api/leads/new')
api.add_resource(LiveMessageList, '/api/livechat/messages')
api.add_resource(LiveChatList, '/api/livechat/sessions')
api.add_resource(LiveChatUpdate, '/api/livechat/update')
api.add_resource(ChatUpdate, '/api/livechat/close')

# dashboard api
api.add_resource(LineChart, '/dashboard/linechart')
api.add_resource(LineChartAdv, '/dashboard/v2/linechart')
api.add_resource(BarChart, '/dashboard/barchart')
api.add_resource(PieChart, '/dashboard/piechart')
api.add_resource(TodoList, '/todo/list')
api.add_resource(TodoCreate, '/todo/new')
api.add_resource(TodoUpdate, '/todo/update')
api.add_resource(TodoSave, '/todo/save')
api.add_resource(UserLocation, '/dashboard/chat/location')
api.add_resource(PromotionList, '/promotion/list')
api.add_resource(PromotionCreate, '/promotion/new')
api.add_resource(PromotionUpdate, '/promotion/update')
api.add_resource(PromotionDelete, '/promotion/delete')

api.add_resource(BotConfigurationPublish, '/api/configuration/publish')
api.add_resource(BotConfigurationCreate, '/api/configuration/new')
api.add_resource(BotConfigurationUpdate, '/api/configuration/update')
api.add_resource(BotConfigurationDelete, '/api/configuration/delete')
api.add_resource(BotConfigurationDetail, '/api/configuration/detail')

if __name__ == '__main__':
    app.run(port='5003', debug=True)
